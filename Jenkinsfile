pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
                // Add your build commands here (e.g., for Django, Node.js, etc.)
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // e.g., sh 'pytest' or sh 'npm test'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                // e.g., call deployment scripts or use SCP/SFTP
            }
        }
    }
}
