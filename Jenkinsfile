// Pipeline name
pipeline {
    // Set agent name (Node name)
    // ADO equal: [pool]
    agent any

    // Parameters section
    parameters {
        string(name: 'SOURCE_REPO_URL', defaultValue: '', description: 'Source Git Repository URL')
        string(name: 'SOURCE_REPO_BRANCH', defaultValue: '', description: 'Source Git Repository Branch')
        string(name: 'SOURCE_REPO_COMMIT', defaultValue: '', description: 'Source Git Repository Commit')
        string(name: 'TARGET_REPO_URL', defaultValue: '', description: 'Target Git Repository URL')
        string(name: 'TARGET_REPO_BRANCH', defaultValue: '', description: 'Target Git Repository Branch')
        string(name: 'TARGET_REPO_COMMIT', defaultValue: '', description: 'Target Git Repository Commit')
        string(name: 'S3_BUCKET', defaultValue: '', description: 'S3 Bucket Name')
    }

    // Section for stages
    stages {
        stage('Validate Python') {
            steps {
                sh "python3 --version"
            }
        }

        // Passing parameters as string in case they are empty - only URL args are required
        stage('Compare Directories') {
            steps {
                sh """python3 compare_directories.py \
                    --source-repo-url '${params.SOURCE_REPO_URL}' \
                    --source-repo-branch '${params.SOURCE_REPO_BRANCH}' \
                    --source-repo-commit '${params.SOURCE_REPO_COMMIT}' \
                    --target-repo-url '${params.TARGET_REPO_URL}' \
                    --target-repo-branch '${params.TARGET_REPO_BRANCH}' \
                    --target-repo-commit '${params.TARGET_REPO_COMMIT}' \
                    --s3-bucket '${params.S3_BUCKET}'"""
            }
        }
        stage('Update Build Description') {
            steps {
                script {
                    // Read the JSON result and update build description
                    def jsonContent = readFile('comparison_*.json')
                    def result = readJSON text: jsonContent
                    def stats = result.comparison.statistics

                    currentBuild.description = """
                    📊 Comparison Results:
                    • Identical: ${stats.identical_files}
                    • Different: ${stats.different_files}  
                    • Source Only: ${stats.source_only}
                    • Target Only: ${stats.target_only}
                    • Status: ${result.comparison.repos_identical ? 'Identical' : 'Different'}
                    """
                }
            }
        }
    }
}