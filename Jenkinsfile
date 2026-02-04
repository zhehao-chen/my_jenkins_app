pipeline {
    agent { label 'testing' } 

    environment {
        APP_VERSION = "1.0"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build & Versioning') {
            steps {
                script {
                    env.FULL_VERSION = "${APP_VERSION}.${env.BUILD_NUMBER}"
                    echo "Current Build Version: ${env.FULL_VERSION}"
                }
            }
        }
    }
}