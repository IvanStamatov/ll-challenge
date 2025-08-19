import requests # Needed to check if the remote repository is accessible
import os # Needed to navigate/check local directories
import filecmp # Needed to compare directories - Will try homemade approach as well
import subprocess # To run commands with external packages/git/aws
import json # For capturing the comparison results
import argparse # For getting arguments from the Jenkins pipeline
import sys # For exiting the script with an error code
import logging # To replace print statements and provide proper logging

# Setting up the logging messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setting up raise options
class ValidationError(Exception):
    """Exception raised when input validation fails"""
    pass

# Function to check if the input is for a remote repo or a local dir
def is_remote_repository(repo_url):
    # Check if the input is empty
    if not repo_url:
        logging.info("[Error] Provided value for repository is empty ")
        raise ValidationError("Provided value for repository is empty")
    
    # Check if the input is a local directory or a URL
    if repo_url.startswith("http://") or repo_url.startswith("https://"):
        logging.info(f"[Info] Detected remote repository URL: [{repo_url}]")
        return True
    else:
        logging.info(f"[Info] Detected local directory: [{repo_url}]")
        return False


# Split into two functions based on if the repo is remote or local
def initiate_remote_directory(repo_url, path):
    try:
        response = requests.get(repo_url)
        if response.status_code != 200:
            logging.info(f"[Error] Remote repository: [{repo_url}] is not accessible (HTTP {response.status_code})")
            return None
        else:
            logging.info(f"[Success] Remote repository: [{repo_url}] is accessible")
    except requests.RequestException as e:
        logging.info(f"[Error] Invalid Repository URL: [{repo_url}]")
        return None

    logging.info(f"[Info] Cloning the remote repo: [{repo_url}]")

    # Remove the folder if it exists already - Could be a better way to ensure important files/paths do not get deleted (case: if path name matches another folder)
    if os.path.exists(path):
        logging.info(f"[Info] Removing existing directory: [{path}]")
        subprocess.run(["rm", "-rf", path], check=True)
    
    try:
        subprocess.run(["git", "clone", repo_url, path], check=True)
        logging.info(f"[Success] Cloned {repo_url} into {path}")
        return path
    except subprocess.CalledProcessError:
        logging.info(f"[Error] Failed to clone {repo_url}")
        return None
    

def initiate_local_directory(repo_url, path):
    # Check if the local directory exists
    if not os.path.isdir(repo_url):
        logging.info(f"[Error] Local directory: [{repo_url}] does not exist")
        return None
    else:
        logging.info(f"[Success] Local directory: [{repo_url}] is valid")
        path = repo_url
        return path


# Function to compare two directories
def compare_directories(source_directory, target_directory, source_url, target_url):
    # ISSUE - filecmp does compare the content - it did not show actual changes when testing
    # Google, Reddit and Stackoverflow point to combining filecmp with os.walk 

    def get_all_files(directory):
        file_paths = []
        for root, dirs, files in os.walk(directory):
            # Remove any .git paths as we do not want to check/compare those yet
            if '.git' in dirs:
                dirs.remove('.git')
                
            for file in files:
                # Get path relative to the base directory
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, directory)
                file_paths.append(rel_path)
        return sorted(file_paths)
        # Now we have an array of file paths that we can compare to eachother
    
    # Create an array of all files in each local repo
    source_repo_files = get_all_files(source_directory)
    target_repo_files = get_all_files(target_directory)
    
    # Set up empty arrays beforehand
    common_identical_files = []
    different_content_files = []
    
    source_only_files_array = [f for f in source_repo_files if f not in target_repo_files]
    target_only_files_array = [f for f in target_repo_files if f not in source_repo_files]
    
    # For each file path in each local repo - add the original dir at the start so that the script can reach the file
    for file in set(source_repo_files) & set(target_repo_files):
        source_file = os.path.join(source_directory, file)
        target_file = os.path.join(target_directory, file)
        
        # Now compare the files with filecmp - Add to each array based on if they are the same of not
        if filecmp.cmp(source_file, target_file, shallow=False):
            common_identical_files.append(file)
        else:
            different_content_files.append(file)
    
    # Append the result in a structured JSON format
    comparison_result = {
        "source_directory": source_directory,
        "target_directory": target_directory,
        "source_directory_name": source_url,
        "target_directory_name": target_url,
        "comparison": {
            "common_identical_files": common_identical_files,
            "different_content_files": different_content_files,
            "source_only_files": source_only_files_array,
            "target_only_files": target_only_files_array,
            "repos_identical": len(source_only_files_array) == 0 and len(target_only_files_array) == 0 and len(different_content_files) == 0,
            "statistics": {
                "total_files_source": len(source_repo_files),
                "total_files_target": len(target_repo_files),
                "identical_files": len(common_identical_files),
                "different_files": len(different_content_files),
                "source_only": len(source_only_files_array),
                "target_only": len(target_only_files_array)
            }
        }
    }
    
    logging.info(json.dumps(comparison_result, indent=2))
    return comparison_result


def checkout_repo(path, branch, commit):
    # Here, we have all local repos - the remotes ones are downloaded already
    # We need to go to the local path, checkout the given branch and reset to the specified commit

    # Get current dir on server so that we can go back after the checkout
    original_dir = os.getcwd()

    # Go into the repo folder
    os.chdir(path)

    try:
        # If the branch input is empty, we should use the default branch
        if not branch:
            logging.info("[Info] No branch specified, checking default branch ...")
            # Get default branch if none specified
            default_branch = subprocess.check_output(
                ["git", "symbolic-ref", "--short", "HEAD"], 
                stderr=subprocess.STDOUT,
                text=True
            ).strip()
            branch = default_branch
            logging.info(f"[Info] Using default branch: {branch}")
        else:
            # Run fetch to make sure the branch is okay
            subprocess.run(["git", "fetch"], check=True)

        # If the branch input is not empty, the if above will not run and the value will remain what the initial input was
        subprocess.run(["git", "checkout", branch], check=True)
        logging.info(f"[Success] Checked out branch: {branch}")

        # If a commit value was provided, check if it exists in the current branch. If it does, then reset to it
        if commit:
            try:
                subprocess.run(["git", "rev-parse", "--verify", commit], check=True)
                # If the check passed, reset to the commit
                subprocess.run(["git", "reset", "--hard", commit], check=True)
                logging.info(f"[Success] Reset to commit: {commit}")
            except subprocess.CalledProcessError:
                logging.info(f"[Error] Commit {commit} does not exist in branch {branch}")
                # Reset back to the original directory
                os.chdir(original_dir)
                return False

        # If there is no commit value provided, we can assume the user wants the latest commit
        # Reset back to the original directory
        os.chdir(original_dir)
        return True
    except Exception as e:
        logging.info(f"[Error] Git operation failed: {str(e)}")
        # Reset back to the original directory
        os.chdir(original_dir)
        return False


def main():
    # Set up argument parser - Avoiding using sys.argv
    parser = argparse.ArgumentParser(description='Compare directories')
    
    # Source section
    parser.add_argument('--source-repo-url', required=True, help='URL or path to source repository')
    parser.add_argument('--source-repo-branch', default='', help='Branch to checkout in source repository')
    parser.add_argument('--source-repo-commit', default='', help='Commit to checkout in source repository')

    # Target section
    parser.add_argument('--target-repo-url', required=True, help='URL or path to target repository')
    parser.add_argument('--target-repo-branch', default='', help='Branch to checkout in target repository')
    parser.add_argument('--target-repo-commit', default='', help='Commit to checkout in target repository')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Use arguments instead of hardcoded values
    source_url = args.source_repo_url
    source_branch = args.source_repo_branch
    source_commit = args.source_repo_commit
    
    target_url = args.target_repo_url
    target_branch = args.target_repo_branch
    target_commit = args.target_repo_commit

    # Establish the repo/dir and return a path to be checked. If remote, the path is a custom folder, if local, the path is the input
    # Code for source
    if is_remote_repository(source_url):
        source_repo_path = initiate_remote_directory(source_url, "source_repo")
    else:
        source_repo_path = initiate_local_directory(source_url, "source_repo")
    if source_repo_path is None:
        logging.info(f"[Error] Directory [{source_url}] could not be initialized.")
        return
    logging.info(f"[Info] Source repo path: {source_repo_path}")
    # Code for target
    if is_remote_repository(target_url):
        target_repo_path = initiate_remote_directory(target_url, "target_repo")
    else:
        target_repo_path = initiate_local_directory(target_url, "target_repo")
    if target_repo_path is None:
        logging.info(f"[Error] Directory [{target_url}] could not be initialized.")
        return
    logging.info(f"[Info] Target repo path: {target_repo_path}")

    # If the function returns false, print error and return to main - need to see how to print errors to users in Jenkins for UX
    if not checkout_repo(source_repo_path, source_branch, source_commit):
        logging.info(f"[Error] Failed to checkout source repo. Please check the logs.")
        return
    if not checkout_repo(target_repo_path, target_branch, target_commit):
        logging.info(f"[Error] Failed to checkout target repo. Please check the logs.")
        return

    # Compare the two directories/repos. Returns a JSON object
    compare_directories(source_repo_path, target_repo_path, source_url, target_url)


if __name__ == "__main__":
    main()