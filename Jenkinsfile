pipeline {
    agent any

    environment {
        VENV = 'env'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Michael-hanyy/visa_payment.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv $VENV
                source $VENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Lint Code') {
            steps {
                sh '''
                source $VENV/bin/activate
                flake8 .
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                source $VENV/bin/activate
                python manage.py test
                '''
            }
        }
    }
}
