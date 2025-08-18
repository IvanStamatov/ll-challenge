# Task is to have a script that compares:
# - directories and the files within them.
# - compare commits and tags in Git repos

# This means that we needs to validate:
# 1) If the input is not empty 
# 2) If the repo URL exists and is accessible(permission)
# ? Check if it is a local dir or URL to remote repo


import requests # Needed to check if the remote repository is accessible

def validate_input(repo_url):
    if not repo_url:
        print("Provided value for repository is empty ")
        return False

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
    
    # If there are no errors in the checks above, return that the input is valid
    return True

def main():
    repo_url = "https://github.com/IvanStamatov/ll-challenge"
    if validate_input(repo_url):
        print("[Success] Repository URL is valid")
    else:
        print("[Error] Repository URL is invalid")

if __name__ == "__main__":
    main()