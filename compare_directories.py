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
    # TODO check if the path exists
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


def main():
    # Group variables by source and target - This blocks development for comparing more than 2 dirs
    # Temporary section, input might be a list
    source_directory = "https://github.com/rust-lang/rustlings"
    target_directory = "https://github.com/inancgumus/learngo"
    
    # Now to check commits, but branch?
    # Can be like if branch is not provided, then use main/master/default
    # Check for commit in that branch
    # "Main" Branches can be either main/master - differs from repo to repo
    source_branch = "main"
    source_commit = ""
    target_branch = "main"
    target_commit = ""

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


    # Compare the two directories/repos. Returns a JSON object
    compare_directories(source_repo_path, target_repo_path)


if __name__ == "__main__":
    main()