# Task is to have a script that compares:
# - directories and the files within them.
# - compare commits and tags in Git repos

# This means that we needs to validate:
# 1) If the input is not empty 
# 2) If the repo URL exists and is accessible(permission)
# ? Check if it is a local dir or URL to remote repo

# Decisions:
# - Input would be limited to only two directories
#   - Can be done with a dictionary of repo_url:argument (commit/tag/path)

import requests # Needed to check if the remote repository is accessible
import os # Needed to navigate/check local directories
import filecmp # Needed to compare directories - Will try homemade approach as well
import subprocess # To run commands with external packages/git/aws


def initiate_directory(repo_url, path):
    if not repo_url:
        print("Provided value for repository is empty ")
        return False

    # Check if the input is a local directory or a URL
    if repo_url.startswith("http://") or repo_url.startswith("https://"):
        print(f"[Info] Detected remote repository URL: [{repo_url}]")
        # Check if the URL is accessible
        try:
            response = requests.head(repo_url)
            if response.status_code != 200:
                print(f"[Error] Remote repository: [{repo_url}] is not accessible")
                return False
            else:
                print(f"[Success] Remote repository: [{repo_url}] is accessible")
        except requests.RequestException as e:
            print(f"[Error] Invalid Repository URL: [{repo_url}]")
            return False
        # Now that the URL is accessible, clone the remote repo
        print(f"[Info] Cloning the remote repo: [{repo_url}]")
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
            return
        else:
            print(f"[Success] Local directory: [{repo_url}] is valid")
            path = repo_url
            return path



def compare_directories(directory_1, directory_2):
    # Compare the two directories
    directory_comparison_list = filecmp.dircmp(directory_1, directory_2)
    # Print if they are identical
    if not directory_comparison_list.left_only and not directory_comparison_list.right_only and not directory_comparison_list.diff_files:
        print(f"[Info] Directories are identical: {directory_1} <=> {directory_2}")
    # Report differences
    if directory_comparison_list.left_only:
        print(f"[Info] Files only in {directory_1}: {directory_comparison_list.left_only}")
    if directory_comparison_list.right_only:
        print(f"[Info] Files only in {directory_2}: {directory_comparison_list.right_only}")
    if directory_comparison_list.diff_files:
        print(f"[Info] Different files: {directory_comparison_list.diff_files}")


def main():
    # Temporary section, input might be a list
    directory_1 = "https://github.com/IvanStamatov/ll-challenge"
    directory_2 = "/home/stamy/lucidlink"

    # Make a list from the two variables
    directories = [directory_1, directory_2]
    # Validate each directory/repo
    source_repo_path = initiate_directory(directories[0], "source_repo")
    target_repo_path = initiate_directory(directories[1], "target_repo")
    print(f"[Info] Source repo path: {source_repo_path}")
    print(f"[Info] Target repo path: {target_repo_path}")

    # Compare the two directories/repos
    compare_directories(source_repo_path, target_repo_path)


if __name__ == "__main__":
    main()