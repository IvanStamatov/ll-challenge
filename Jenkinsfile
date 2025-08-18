// Pipeline name
pipeline {
    // Set agent name (Node name)
    // ADO equal: [pool]
    agent any

    // Section for stages
    stages {
        stage('Hello') {
            steps {
                echo "Hello, this is a message from instance: [$(hostname -i)]"
                echo "Current user: [$(whoami)]"
            }
        }
    }
}