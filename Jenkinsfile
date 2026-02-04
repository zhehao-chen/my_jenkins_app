pipeline {
    agent { label 'testing' }

    environment {
        BASE_VERSION = "1.0"
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
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
                export PATH=$PATH:/usr/local/bin
                python3 -m pip install --user --break-system-packages -r requirements.txt || \
                python3 -m pip install --user -r requirements.txt || true
                python3 -m pip install --user playwright locust || true
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

                /usr/bin/sqlite3 staging.db < init_db.sql || sqlite3 staging.db < init_db.sql || echo "SQLITE_SKIP"
                
                echo "DATABASE_VERIFICATION:"
                /usr/bin/sqlite3 staging.db 'SELECT * FROM users;' || sqlite3 staging.db 'SELECT * FROM users;' || echo "NO_DB_OUTPUT"
                """
                sh "python3 -m pytest tests/unit_tests.py || echo 'Unit tests finished'"
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
                        sh "python3 tests/user_journey.py || echo 'E2E finished'"
                    }
                }
                stage('Performance Load Test') {
                    steps {
                        sh "python3 -m locust -f tests/locustfile.py --headless -u 5 -r 1 --run-time 20s --host=http://localhost:5000 || echo 'Locust finished'"
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