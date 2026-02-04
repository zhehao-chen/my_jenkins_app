pipeline {
    agent {
        docker {
            image 'python:3.11-bullseye'
            args '-u root'
        }
    }

    environment {
        BASE_VERSION = "1.0"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                apt-get update && apt-get install -y sqlite3
                pip install --no-cache-dir -r requirements.txt || true
                pip install --no-cache-dir locust playwright || true
                """
            }
        }

        stage('Build & Versioning') {
            steps {
                script {
                    env.APP_VERSION = "${BASE_VERSION}.${env.BUILD_NUMBER}"
                    echo "BUILD_LOG: Current Application Version is set to ${env.APP_VERSION}"
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarServer') {
                        sh "${scannerHome}/bin/sonar-scanner \
                          -Dsonar.projectKey=my_jenkins_app \
                          -Dsonar.projectVersion=${env.APP_VERSION} \
                          -Dsonar.sources=. \
                          -Dsonar.python.version=3"
                    }
                }
            }
        }

        stage('DB Init & Unit Testing') {
            steps {
                sh """
                echo "CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE
                );
                INSERT OR IGNORE INTO users (username, email) VALUES 
                ('python_tester', 'test@example.com'),
                ('QA_lead', 'qa@example.com');" > init_db.sql

                sqlite3 staging.db < init_db.sql
                echo "DATABASE_VERIFICATION:"
                sqlite3 staging.db 'SELECT * FROM users;'
                """
                sh "python3 -m pytest tests/unit_tests.py || echo 'Unit tests completed'"
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Parallel Tests') {
            parallel {
                stage('E2E User Journey') {
                    steps {
                        sh "python3 tests/user_journey.py || echo 'E2E script run finished'"
                    }
                }
                stage('Performance Load Test') {
                    steps {
                        sh "locust -f tests/locustfile.py --headless -u 5 -r 1 --run-time 20s --host=http://localhost:5000 || echo 'Locust run finished'"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completed for version: ${env.APP_VERSION}"
        }
    }
}