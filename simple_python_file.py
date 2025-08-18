#!/usr/bin/env python3

import sys # For working with arguments

# Function to check a single URL, to be called for each one
def validate_input(repo_url):
    if not repo_url:
        return False
    # If the variable is not empty, return True to parent
    return True

def main():
    # Set a list of repos for testing
    # Set repos as a list of all provided arguments to the python script
    repos = sys.argv[1:]
    #   repos = [
    #       "https://github.com/IvanStamatov/ll-challenge.git", ""
    #   ]

    # Check if the repos list is empty
    if not repos:
        print("[Error] No repository URLs provided.")
        return

    for repo in repos:
        # Call the validate_input function for each repository URL
        if not validate_input(repo):
            print(f"[Error] Invalid repository URL: '{repo}'")
        else:
            print(f"[Success] Valid repository URL: '{repo}'")

    print("[Summary] All validations passed.")


if __name__ == "__main__":
    main()