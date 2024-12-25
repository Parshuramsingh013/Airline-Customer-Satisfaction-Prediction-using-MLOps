# Airline Customer Satisfaction Prediction using MLOps

![Project Banner](https://github.com/Parshuramsingh013/Airline-Customer-Satisfaction-Prediction-using-MLOps/blob/main/banner.png) <!-- Add a banner image if available -->

## Project Overview
This project aims to predict airline customer satisfaction using MLOps practices for streamlined model development, deployment, and monitoring. By leveraging tools such as GitHub, Jenkins, Docker, Docker Hub, and AWS, we have automated and containerized the deployment of a machine learning model that evaluates customer satisfaction levels.

## Features
- End-to-end machine learning pipeline using MLOps practices.
- Continuous Integration/Continuous Deployment (CI/CD) with Jenkins.
- Dockerized application for platform independence.
- Hosted on AWS with a publicly accessible deployment.
- Data version control managed using DVC.

## Tech Stack
- **Programming Language**: Python
- **Version Control**: GitHub
- **Pipeline Automation**: Jenkins
- **Containerization**: Docker, Docker Hub
- **Cloud Hosting**: AWS Elastic Load Balancer (ELB)
- **Data Versioning**: DVC

## Deployment
The deployed application is live and can be accessed at:
[Airline Customer Satisfaction Prediction](http://parshurams-lb-944068628.eu-north-1.elb.amazonaws.com)

## Project Directory Structure
```
MLOPS-PROJECT
|-- .dvc                # DVC cache and configuration
|-- artifacts           # Generated files during pipeline execution
|   |-- engineered_data
|   |-- ingested_data
|   |-- model
|   |-- processed_data
|   |-- raw
|-- config              # Configuration files
|   |-- db_config.py    # Database configuration
|   |-- params.json     # Model parameters
|   |-- paths_config.py # Paths used in the pipeline
|-- custom_jenkins      # Jenkins-related files
|-- logs                # Logs generated during execution
|-- mlruns              # MLflow logs
|-- src                 # Source code
|   |-- data_ingestion.py
|   |-- data_processing.py
|   |-- database_extraction.py
|   |-- feature_engineering.py
|   |-- logger.py       # Logging setup
|   |-- model_selection.py
|   |-- model_training.py
|-- static              # CSS and static assets
|-- templates           # HTML templates
|-- utils               # Helper utilities
|-- venv                # Virtual environment setup
|-- application.py      # Entry point for Flask application
|-- Dockerfile          # Docker configuration
|-- Jenkinsfile         # Jenkins pipeline configuration
|-- dvc.yaml            # DVC pipeline configuration
|-- requirements.txt    # Python dependencies
|-- README.md           # Project documentation
```

## Setup Instructions
### Prerequisites
1. Install Python 3.8 or above.
2. Install Docker.
3. Set up Jenkins and connect it to your GitHub repository.
4. AWS account with necessary permissions for hosting.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Parshuramsingh013/Airline-Customer-Satisfaction-Prediction-using-MLOps.git
   cd Airline-Customer-Satisfaction-Prediction-using-MLOps
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application locally:
   ```bash
   python application.py
   ```
4. Build and run Docker container:
   ```bash
   docker build -t airline-satisfaction-app .
   docker run -p 5000:5000 airline-satisfaction-app
   ```
5. Deploy to AWS using the pre-configured Jenkins pipeline.

## CI/CD Pipeline
The project uses Jenkins for automating the following tasks:
- Pull the latest changes from GitHub.
- Build Docker images and push them to Docker Hub.
- Deploy the containerized application to AWS.

## Key Components
### 1. Data Ingestion
- Extracts and preprocesses data for training and inference.
- Uses **database_extraction.py** for data extraction.

### 2. Feature Engineering
- Performs feature transformations and data cleaning.

### 3. Model Training
- Trains machine learning models and saves the best one for deployment.

### 4. Deployment
- Uses Flask for the web interface.
- Dockerized and hosted on AWS.

## Live Monitoring
TensorBoard logs are available for model performance monitoring.

## Future Work
- Add real-time data ingestion.
- Integrate advanced monitoring and alerting tools.
- Improve model accuracy and add more features.

## Author
[Parshuram Singh](https://github.com/Parshuramsingh013)

---
Feel free to raise issues or contribute to the repository!
