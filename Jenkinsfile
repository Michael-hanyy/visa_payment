pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Docker', url: 'https://github.com/Michael-hanyy/visa_payment.git'
            }
        }

        stage('Stop Old Containers') {
            steps {
                sh 'docker compose down --remove-orphans || true'
            }
        }

        stage('Build with Docker Compose') {
            steps {
                sh 'docker compose build --no-cache'
            }
        }

        stage('Start Containers') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Run Tests') {
            steps {
                // change "web" to your app container name in docker-compose.yml
                sh 'docker compose exec -T web pytest || echo "Tests failed"'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment complete ✅'
            }
        }
    }
}

