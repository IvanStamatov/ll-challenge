# About
- Repository for Jenkins pipeline as an exercise

# Repository content
- Bash and Python scripts 
- Jenkinsfile
- README.md
- Diagram of project
- User guide

# How to use pipeline
- To be added later on

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

# Sources
| Resource | Links |
|----------|-------|
| DSL | [Jenkins Job DSL Pipeline Steps](https://www.jenkins.io/doc/pipeline/steps/job-dsl/)<br>[EPAM article on Jenkins DSL options](https://medium.com/epam-delivery-platform/jenkins-job-dsl-pipeline-dsl-declarative-pipeline-scripted-pipeline-groovy-libraries-aaaaab9250e6) |
| Jenkins Images | [Jenkins Download Page](https://www.jenkins.io/download/) |
| Jenkins in Docker | [Jenkins in Docker Installation Guide](https://www.jenkins.io/doc/book/installing/docker/) |
| Jenkins Pipeline | [Jenkins Pipelines Official Guide](https://www.jenkins.io/doc/book/pipeline/) |
| Compare dirs in Python | [fimecmp package](https://docs.python.org/3/library/filecmp.html) |
| Argparse in Python | [argparse](https://docs.python.org/2/library/argparse.html) |