# Task is to have a script that compares:
# - directories and the files within them.
# - compare commits and tags in Git repos
# ===============
# This means that we needs to validate:
# 1) If the input is not empty 
# 2) If the repo URL exists and is accessible(permission)
# ? Check if it is a local dir or URL to remote repo
# ===============
# Output
# There are no specific requirements for the output format, but it should be clear, structured and convenient for processing by another script or program.
# First though is JSON - it can be used to make an HTML report for humans, while being perfect for scripts/pipelines
# ===============
# Decisions:
# - Input would be limited to only two directories
#   - Can be done with a dictionary of repo_url:argument (commit/tag/path)

import requests # Needed to check if the remote repository is accessible
import os # Needed to navigate/check local directories
import filecmp # Needed to compare directories - Will try homemade approach as well
import subprocess # To run commands with external packages/git/aws
import json # For capturing the comparison results


def is_remote_repository(repo_url):
    # Check if the input is empty
    if not repo_url:
        print("[Error] Provided value for repository is empty ")
        return None
    
    # Check if the input is a local directory or a URL
    if repo_url.startswith("http://") or repo_url.startswith("https://"):
        print(f"[Info] Detected remote repository URL: [{repo_url}]")
        return True
    else:
        print(f"[Info] Detected local directory: [{repo_url}]")
        return False


def initiate_remote_directory(repo_url, path):
    try:
        response = requests.get(repo_url)
        if response.status_code != 200:
            print(f"[Error] Remote repository: [{repo_url}] is not accessible (HTTP {response.status_code})")
            return None
        else:
            print(f"[Success] Remote repository: [{repo_url}] is accessible")
    except requests.RequestException as e:
        print(f"[Error] Invalid Repository URL: [{repo_url}]")
        return None

    print(f"[Info] Cloning the remote repo: [{repo_url}]")

    # Remove the folder if it exists already - Could be a better way to ensure important files/paths do not get deleted (case: if path name matches another folder)
    if os.path.exists(path):
        print(f"[Info] Removing existing directory: [{path}]")
        subprocess.run(["rm", "-rf", path], check=True)
    
    try:
        subprocess.run(["git", "clone", repo_url, path], check=True)
        print(f"[Success] Cloned {repo_url} into {path}")
        return path
    except subprocess.CalledProcessError:
        print(f"[Error] Failed to clone {repo_url}")
        return None


def initiate_local_directory(repo_url, path):
    # Check if the local directory exists
    if not os.path.isdir(repo_url):
        print(f"[Error] Local directory: [{repo_url}] does not exist")
        return None
    else:
        print(f"[Success] Local directory: [{repo_url}] is valid")
        path = repo_url
        return path

# Function to compare two directories
def compare_directories(source_directory, target_directory):
    # Compare the two directories
    directory_comparison_object = filecmp.dircmp(source_directory, target_directory)

    # Populate JSON with the results from the filecmp
    comparison_result = {
        "source_directory": source_directory,
        "target_directory": target_directory,
        "comparison": {
            "common_files": directory_comparison_object.common_files,
            "source_only": directory_comparison_object.left_only,
            "target_only": directory_comparison_object.right_only,
            "different_files": directory_comparison_object.diff_files,
            "identical_files": len(directory_comparison_object.left_only) == 0 
                        and len(directory_comparison_object.right_only) == 0 
                        and len(directory_comparison_object.diff_files) == 0
        }
    }
    print(json.dumps(comparison_result, indent=2))
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
            print("[Info] No branch specified, checking default branch ...")
            # Get default branch if none specified
            default_branch = subprocess.check_output(
                ["git", "symbolic-ref", "--short", "HEAD"], 
                stderr=subprocess.STDOUT,
                text=True
            ).strip()
            branch = default_branch
            print(f"[Info] Using default branch: {branch}")
        else:
            # Run fetch to make sure the branch is okay
            subprocess.run(["git", "fetch"], check=True)

        # If the branch input is not empty, the if above will not run and the value will remain what the initial input was
        subprocess.run(["git", "checkout", branch], check=True)
        print(f"[Success] Checked out branch: {branch}")

        # If a commit value was provided, check if it exists in the current branch. If it does, then reset to it
        if commit:
            try:
                subprocess.run(["git", "rev-parse", "--verify", commit], check=True)
                # If the check passed, reset to the commit
                subprocess.run(["git", "reset", "--hard", commit], check=True)
                print(f"[Success] Reset to commit: {commit}")
            except subprocess.CalledProcessError:
                print(f"[Error] Commit {commit} does not exist in branch {branch}")
                # Reset back to the original directory
                os.chdir(original_dir)
                return False

            # Reset back to the original directory
            os.chdir(original_dir)
            return True
    except Exception as e:
        print(f"[Error] Git operation failed: {str(e)}")
        # Reset back to the original directory
        os.chdir(original_dir)
        return False

def main():
    # Group variables by source and target - This blocks development for comparing more than 2 dirs
    # Temporary section, input might be a list
    # https://github.com/rust-lang/rustlings
    source_directory = "https://github.com/inancgumus/learngo"
    target_directory = "https://github.com/inancgumus/learngo"
    
    # Now to check commits, but branch?
    # Can be like if branch is not provided, then use main/master/default
    # Check for commit in that branch
    # "Main" Branches can be either main/master - differs from repo to repo
    source_branch = ""
    source_commit = "33333333"
    target_branch = ""
    target_commit = "1111111111111111"

    # Establish the repo/dir and return a path to be checked. If remote, the path is a custom folder, if local, the path is the input
    # Code for source
    if is_remote_repository(source_directory):
        source_repo_path = initiate_remote_directory(source_directory, "source_repo")
    else:
        source_repo_path = initiate_local_directory(source_directory, "source_repo")
    if source_repo_path is None:
        print(f"[Error] Directory [{source_directory}] could not be initialized.")
        return
    print(f"[Info] Source repo path: {source_repo_path}")
    # Code for target
    if is_remote_repository(target_directory):
        target_repo_path = initiate_remote_directory(target_directory, "target_repo")
    else:
        target_repo_path = initiate_local_directory(target_directory, "target_repo")
    if target_repo_path is None:
        print(f"[Error] Directory [{target_directory}] could not be initialized.")
        return
    print(f"[Info] Target repo path: {target_repo_path}")

    # If the function returns false, print error and return to main - need to see how to print errors to users in Jenkins for UX
    if not checkout_repo(source_repo_path, source_branch, source_commit):
        print(f"[Error] Failed to checkout source repo. Please check the logs.")
        return
    if not checkout_repo(target_repo_path, target_branch, target_commit):
        print(f"[Error] Failed to checkout target repo. Please check the logs.")
        return

    # Compare the two directories/repos. Returns a JSON object
    compare_directories(source_repo_path, target_repo_path)


if __name__ == "__main__":
    main()