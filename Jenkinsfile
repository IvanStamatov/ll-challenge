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
                sh '''
                    #!/bin/bash
                    ls -lah 
                    py_script_path=$(find . -name "simple_python_file.py" -type f)
                    echo $py_script_path
                    echo ${params.SOURCE}
                    echo ${params.TARGET}
                    
                    python3 $py_script_path ${params.SOURCE} ${params.TARGET}
                '''
            }
        }
    }
}