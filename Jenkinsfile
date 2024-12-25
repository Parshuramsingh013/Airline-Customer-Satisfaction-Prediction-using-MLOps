pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        DOCKERHUB_CREDENTIAL_ID = 'mlops-dockerhub'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'parshuramsingh013/airline-customer-satisfaction-prediction-using-mlops'
        AWS_REGION = 'eu-north-1' // Define AWS Region here
    }
    
    stages {
        stage('Cloning from GitHub Repo') {
            steps {
                script {
                    // Cloning GitHub repo
                    echo 'Cloning from GitHub Repo....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-tokens', url: 'https://github.com/Parshuramsingh013/Airline-Customer-Satisfaction-Prediction-using-MLOps']])
                }
            }
        }

        stage('Setup virtual environment') {
            steps {
                script {
                    // Setup virtual environment
                    echo 'Setting up virtual environment....'
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
                        pylint application.py main.py --output=pylint-report.txt --exit-zero || echo "Pylint stage completed"
                        flake8 application.py main.py --ignore=E501,E302 --output-file=flake8-report.txt || echo "Flake8 stage completed"
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

        stage('Building Docker Image') {
            steps {
                script {
                    // Building Docker Image
                    echo 'Building Docker Image....'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }

        stage('Scanning Docker Image') {
            steps {
                script {
                    // Scanning Docker Image
                    echo 'Scanning Docker Image....'
                    sh "trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-scan-report.html"
                }
            }
        }

        stage('Pushing Docker Image') {
            steps {
                script {
                    // Pushing Docker Image
                    echo 'Pushing Docker Image....'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('AWS Deployment') {
            steps {
                // Inject AWS credentials securely
                withCredentials([usernamePassword(credentialsId: 'aws-credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        // AWS Deployment
                        echo 'AWS Deployment....'
                        sh '''
                            export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                            export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                            aws ecs update-service --cluster parshurams_ecs --service parshurams_service --force-new-deployment --region ${AWS_REGION}
                        '''
                    }
                }
            }
        }
    }
}
