# About
- Repository for Jenkins pipeline as an exercise

# Task
- Task is to have a Jenkins pipeline with Python code, that compares two repositories/directories.
- The pipeline should generate an artifact, which should be stored in an S3 bucket.

# TODO
- Parsing the input
    - If the a git repo URL is given without https/http
- Reset cloned remote repositories by tag (currently it is only possible by branch and commit)
- Visualize output for humans
- Search S3 bucket for previous matching comparison

# How to use pipeline
- Log into the Jenkins console
- Go to the pipeline "Compare two directories"
- Click on "Build with Parameters"
- Fill in the parameters with the required information:
    - SOURCE_REPO_URL - Enter the URL or path of the directory/repository you want to compare to.
    - SOURCE_REPO_BRANCH - Enter the name of the branch you want to compare. Leave empty to use the default branch.
    - SOURCE_REPO_COMMIT - Enter the commit ID, where to reset the repository to.
    - TARGET_REPO_URL - Enter the URL or path of the directory/repository you want to compare with.
    - TARGET_REPO_BRANCH - Enter the name of the branch you want to compare. Leave empty to use the default branch.
    - TARGET_REPO_COMMIT - Enter the commit ID, where to reset the repository to.
    - S3_BUCKET - Enter the name of the S3 bucket.

# Infrastructure and Architecture
- Hosted in AWS Cloud
    - Application Server:
        - Type: EC2 Instance
        - OS: Ubuntu 24.04
        - AWS Region: eu-central-1
        - Size: 30GB
- Linux: Ubuntu 24.04
- Docker:
    - Docker: 28.3.3, build 980b856
    - Docker Compose: v2.18.1
- Python: 3.12.3
- Jenkins: 
    - Hosted in a Docker container
    - Version: 2.516.1
- AWS CLI: 2.28.11

# Operational
- Commit message to include "TXXX", where X would be the imaginary service ticket
- Separate ticket per functionality/task

| Ticket | Description |
|--------|-------------|
| T001   | For updating README and documentation |
| T002   | For testing setup |
| T003   | For adding base Python script and a valid Jenkinsfile |
| T004   | For working on the Python comparison file |
| T005   | For updating the Jenkins file to work with T004 Python script |
| T006   | For adding requirements for the Python script |
| T007   | For cleaning up code and comments |
| T008   | Improve error handling and exit codes |
| T009   | For handing artifact upload to S3 |

# Sources
| Resource | Links |
|----------|-------|
| DSL | [Jenkins Job DSL Pipeline Steps](https://www.jenkins.io/doc/pipeline/steps/job-dsl/)<br>[EPAM article on Jenkins DSL options](https://medium.com/epam-delivery-platform/jenkins-job-dsl-pipeline-dsl-declarative-pipeline-scripted-pipeline-groovy-libraries-aaaaab9250e6) |
| Jenkins Images | [Jenkins Download Page](https://www.jenkins.io/download/) |
| Jenkins in Docker | [Jenkins in Docker Installation Guide](https://www.jenkins.io/doc/book/installing/docker/) |
| Jenkins Pipeline | [Jenkins Pipelines Official Guide](https://www.jenkins.io/doc/book/pipeline/) |
| Compare dirs in Python | [fimecmp package](https://docs.python.org/3/library/filecmp.html) |
| Argparse in Python | [argparse](https://docs.python.org/2/library/argparse.html) |
| Uploading to S3 with Python | [AWS SDK for Python](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html) |