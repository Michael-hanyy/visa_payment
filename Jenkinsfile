pipeline {
    agent any

    environment {
        IMAGE_NAME = 'visa_payment_app'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Run Tests in Docker') {
            steps {
                script {
                    sh 'docker run --rm $IMAGE_NAME python manage.py test'
                }
            }
        }
        
        // Optional: Push to Docker registry or other stages here
    }
}
