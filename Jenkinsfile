// Pipeline name
pipeline {
    // Set agent name (Node name)
    // ADO equal: [pool]
    agent any

    // Section for stages
    stages {
        stage('Hello') {
            steps {
                sh '''
                    if [ -z "$params.repository_source" ] || [ -z "$params.repository_target" ]; then
                        echo "Error: Empty params"
                        exit 1
                    fi
                    
                    pwd
                    ls -lah
                    mkdir -p source_repo target_repo
                
                    git clone ${params.repository_source} source_repo
                    git clone ${params.repository_target} target_repo

                    ls -lah source_repo target_repo
                '''
            }
        }
    }
}