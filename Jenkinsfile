// Pipeline name
pipeline {
    // Set agent name (Node name)
    // ADO equal: [pool]
    agent any

    // Define parameters
    parameters {
        string(name: 'SOURCE', defaultValue: '', description: 'Source Git Repository URL')
        string(name: 'TARGET', defaultValue: '', description: 'Target Git Repository URL')
    }

    // Section for stages
    stages {
        stage('Validate Parameters') {
            steps {
                sh "python3 simple_python_file.py ${params.SOURCE} ${params.TARGET}"
            }
        }
    }
}