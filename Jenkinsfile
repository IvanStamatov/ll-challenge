// Pipeline name
pipeline {
    // Set agent name (Node name)
    // ADO equal: [pool]
    agent any

    // Define parameters
    parameters {
        string(name: 'repo_source', defaultValue: '', description: 'Source Git Repository URL')
        string(name: 'repo_target', defaultValue: '', description: 'Target Git Repository URL')
    }

    // Section for stages
    stages {
        stage('Validate Parameters') {
            steps {
                sh '''
                    #!/bin/bash
                    ls -lah 
                    py_script_path=$(find . -name "simple_python_file.py" -type f)
                    echo $py_script_path
                    
                    python3 $py_script_path "${params.REPO_SOURCE}" "${params.REPO_TARGET}"
                '''
            }
        }
    }
}