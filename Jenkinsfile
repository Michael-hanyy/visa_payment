pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = "docker-compose"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out code..."
                checkout scm
            }
        }

        stage('Build Docker Containers') {
            steps {
                echo "Building Docker containers..."
                sh "${DOCKER_COMPOSE} build"
            }
        }

        stage('Run Migrations') {
            steps {
                echo "Applying Django migrations..."
                sh "${DOCKER_COMPOSE} run --rm app python manage.py migrate"
            }
        }

        stage('Run Mock Tests') {
            steps {
                echo "Running mock tests..."
                sh "${DOCKER_COMPOSE} run --rm app python manage.py test tests"
            }
        }

        stage('Cleanup') {
            steps {
                echo "Stopping containers..."
                sh "${DOCKER_COMPOSE} down"
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
        success {
            echo "All tests passed ✅"
        }
        failure {
            echo "Some tests failed ❌"
        }
    }
}
