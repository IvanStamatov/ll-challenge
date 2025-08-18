// Pipeline name
pipeline {
    // Set agent name (Node name)
    // ADO equal: [pool]
    agent any

    // Section for stages
    stages {
        stage('Validate Python') {
            steps {
                sh 'python3 --version'
            }
        }
    }
}