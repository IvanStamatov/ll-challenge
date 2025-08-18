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

def initiate_directory(repo_url, path):
    # Check if the input is empty
    if not repo_url:
        print("[Error] Provided value for repository is empty ")
        return None

    # Check if the input is a local directory or a URL
    if repo_url.startswith("http://") or repo_url.startswith("https://"):
        print(f"[Info] Detected remote repository URL: [{repo_url}]")
        # Check if the URL is accessible
        try:
            response = requests.head(repo_url)
            if response.status_code != 200:
                print(f"[Error] Remote repository: [{repo_url}] is not accessible")
                return None
            else:
                print(f"[Success] Remote repository: [{repo_url}] is accessible")
        except requests.RequestException as e:
            print(f"[Error] Invalid Repository URL: [{repo_url}]")
            return None
        # Now that the URL is accessible, clone the remote repo
        print(f"[Info] Cloning the remote repo: [{repo_url}]")
        # TODO check if the path exists
        try:
            subprocess.run(["git", "clone", repo_url, path], check=True)
            print(f"[Success] Cloned {repo_url} into {path}")
            return path
        except subprocess.CalledProcessError:
            print(f"[Error] Failed to clone {repo_url}")
    else:
        print(f"[Info] Detected local directory: [{repo_url}]")
        # Check if the local directory exists
        if not os.path.isdir(repo_url):
            print(f"[Error] Local directory: [{repo_url}] does not exist")
            return None
        else:
            print(f"[Success] Local directory: [{repo_url}] is valid")
            path = repo_url
            return path


# Function to compare two directories
def compare_directories(directory_1, directory_2):
    # Compare the two directories
    directory_comparison_object = filecmp.dircmp(directory_1, directory_2)

    # Populate JSON with the results from the filecmp
    comparison_result = {
        "source_directory": directory_1,
        "target_directory": directory_2,
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


def main():
    # Temporary section, input might be a list
    directory_1 = "https://github.com/IvanStamatov/ll-challenge"
    directory_2 = "https://github.com/IvanStamatov/ll-challenge"

    # Make a list from the two variables
    directories = [directory_1, directory_2]
    # Validate each directory/repo
    source_repo_path = initiate_directory(directories[0], "source_repo")
    target_repo_path = initiate_directory(directories[1], "target_repo")

    if source_repo_path is None:
        print(f"[Error] Directory [{directories[0]}] could not be initialized.")
        return
    if target_repo_path is None:
        print(f"[Error] Directory [{directories[1]}] could not be initialized.")
        return
    
    print(f"[Info] Source repo path: {source_repo_path}")
    print(f"[Info] Target repo path: {target_repo_path}")

    # Compare the two directories/repos. Returns a JSON object
    compare_directories(source_repo_path, target_repo_path)


if __name__ == "__main__":
    main()