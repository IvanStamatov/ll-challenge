# Task is to have a script that compares:
# - directories and the files within them.
# - compare commits and tags in Git repos

# This means that we needs to validate:
# 1) If the input is not empty 
# 2) If the repo URL exists and is accessible(permission)
# ? Check if it is a local dir or URL to remote repo


import requests # Needed to check if the remote repository is accessible
import os # Needed to navigate/check local directories

def validate_input(repo_url):
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
    else:
        print(f"[Info] Detected local directory: [{repo_url}]")
        # Check if the local directory exists
        if not os.path.isdir(repo_url):
            print(f"[Error] Local directory: [{repo_url}] does not exist")
            return False
        else:
            print(f"[Success] Local directory: [{repo_url}] is valid")

    # If there are no errors in the checks above, return that the input is valid
    return True

def main():
    # Tested with local paths as well
    repo_url = "https://github.com/IvanStamatov/ll-challenge"

    # Temporary section, input might be a list
    directory_1 = "https://github.com/IvanStamatov/ll-challenge"
    directory_2 = "https://github.com/IvanStamatov/ll-challenge"

    # Make a list from the two variables
    directories = [directory_1, directory_2]

    for directory in directories:
        if validate_input(directory):
            print(f"[Success] Directory URL is valid: {directory}")
        else:
            print(f"[Error] Directory URL is invalid: {directory}")

if __name__ == "__main__":
    main()