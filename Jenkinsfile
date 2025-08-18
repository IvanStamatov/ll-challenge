// Pipeline name
pipeline {
    // Set agent name (Node name)
    // ADO equal: [pool]
    agent any

    // Define parameters
    parameters {
        string(name: 'repository_source', defaultValue: '', description: 'Source Git Repository URL')
        string(name: 'repository_target', defaultValue: '', description: 'Target Git Repository URL')
    }

    // Section for stages
    stages {
        stage('Validate Parameters') {
            steps {
                script {
                    def repoValidation = sh(
                        script: """
                            ${WORKSPACE}/simple_python_file.py "${params.repository_source}" "${params.repository_target}"
                        """,
                        returnStatus: true
                    )
                }
            }
        }
    }
}