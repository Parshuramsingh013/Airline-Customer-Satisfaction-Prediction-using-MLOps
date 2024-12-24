pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }
    
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

        stage('Setup virtual environment') {
            steps {
                script {
                    // Setup virtual environment
                    echo 'Setup virtual environment....'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Linting code') {
            steps {
                script {
                    // Linting code
                    echo 'Linting code....'
                    sh '''
                        set -e
                        . ${VENV_DIR}/bin/activate

                        pylint application.py main.py --output=pylint-report.txt --exit-zero || echo " Pylint stage completed"
                        flake8 application.py main.py --ignore=E501, E302 --output-file=flake8-report.txt || echo "Flake8 stage completed"
                        black application.py main.py || echo "Black stage completed"

                        
                    '''
                    
                }
            }
        }

        stage('Trivy Scanning') {
            steps {
                script {
                    // Trivy Scanning
                    echo 'Trivy Scanning....'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"
                }
            }
        }
    }
}