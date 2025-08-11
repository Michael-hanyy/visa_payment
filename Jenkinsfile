pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Docker', url: 'https://github.com/Michael-hanyy/visa_payment.git'
            }
        }

        stage('Build with Docker Compose') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose build --no-cache'
                sh 'docker compose up -d'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker compose exec -T web pytest'  // change "web" to your app service name
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment steps go here'
            }
        }
    }
}
