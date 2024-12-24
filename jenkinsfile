pipeline {
    agent any
    
    stages {
        stage('Cloning from GitHub Repo') {
            steps {
                script {
                    // Cloning git hub repo
                    echo 'Cloning from GitHub Repo....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-tokens', url: 'https://github.com/Parshuramsingh013/Airline-Customer-Satisfaction-Prediction-using-MLOps']])
                }
            }
        }
    }
}