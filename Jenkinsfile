// Pipeline name
pipeline {
    // Set agent name (Node name)
    // ADO equal: [pool]
    agent any

    // Section for stages
    stages {
        stage('Hello') {
            steps {
                sh 'echo "Hello, this is a message from instance: [$(hostname -i)]"'
                sh 'echo "Current user: [$(whoami)]"'
            }
        }
    }
}