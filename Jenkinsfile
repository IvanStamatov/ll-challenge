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
                sh '''
                    ls -lah 
                    py_script_path=$(find . -name "simple_python_file.py" -type f)
                    echo $py_script_path
                    python3 $py_script_path "${params.repository_source}" "${params.repository_target}"
                '''
            }
        }
    }
}