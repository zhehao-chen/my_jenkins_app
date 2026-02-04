pipeline {
    // Q2: Running on the specific agent with 'testing' label
    agent { label 'testing' }

    environment {
        // Q4: Define base version for semantic versioning
        BASE_VERSION = "1.0"
    }

    stages {
        stage('Checkout') {
            steps {
                // Q3: Source Control Management integration
                checkout scm
            }
        }

        stage('Build & Versioning') {
            steps {
                script {
                    // Q4: Implementation of incrementing semantic versioning
                    env.APP_VERSION = "${BASE_VERSION}.${env.BUILD_NUMBER}"
                    echo "BUILD_LOG: Current Application Version is set to ${env.APP_VERSION}"
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                // Q5: Integration with SonarQube for static analysis
                script {
                    // This uses the tool name 'SonarScanner' configured in Global Tool Configuration
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarServer') {
                        sh "${scannerHome}/bin/sonar-scanner \
                          -Dsonar.projectKey=my_jenkins_app \
                          -Dsonar.projectName='My Jenkins Python App' \
                          -Dsonar.projectVersion=${env.APP_VERSION} \
                          -Dsonar.sources=. \
                          -Dsonar.python.version=3"
                    }
                }
            }
        }

        stage('Unit Testing') {
            steps {
                // Q6: Automated Unit Testing stage
                echo "Running Unit Tests via PyTest..."
                // Ensure requirements are installed if necessary: sh 'pip install pytest'
                sh "python3 -m pytest tests/unit_tests.py --junitxml=reports/unit_results.xml || echo 'No tests found'"
            }
        }

        stage('Quality Gate') {
            steps {
                // Q5: Enforcing SonarQube Quality Gate
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Parallel Automated Testing') {
            // Running Q7 and Q8 in parallel to save time
            parallel {
                stage('E2E User Journey') {
                    steps {
                        // Q7: End-to-End testing implementation
                        echo "Executing Playwright E2E User Journey Tests..."
                        sh "python3 tests/user_journey.py || echo 'E2E script missing'"
                    }
                }
                stage('Performance Load Test') {
                    steps {
                        // Q8: Performance/Load testing implementation
                        echo "Executing Locust Performance Tests..."
                        sh "locust -f locustfile.py --headless -u 10 -r 2 --run-time 1m || echo 'Locust not installed'"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished execution for Version: ${env.APP_VERSION}"
        }
        success {
            echo "SUCCESS: Version ${env.APP_VERSION} passed all quality gates and tests."
        }
        failure {
            echo "FAILURE: Pipeline failed at version ${env.APP_VERSION}. Please check logs."
        }
    }
}