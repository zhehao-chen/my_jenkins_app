pipeline {
    agent { label 'testing' }

    environment {
        // Q4: Define the base semantic version
        BASE_VERSION = "1.0"
        // Setup environment variables for SonarQube and Tests
        SONAR_SCANNER_HOME = tool 'SonarScanner' 
    }

    stages {
        stage('Checkout') {
            steps {
                // Q3: Source Control Integration
                checkout scm
            }
        }

        stage('Build & Versioning') {
            steps {
                script {
                    // Q4: Implementation of semantic versioning using Build Number
                    env.APP_VERSION = "${BASE_VERSION}.${env.BUILD_NUMBER}"
                    echo "Successfully assigned Version: ${env.APP_VERSION}"
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                // Q5: Static Code Analysis with SonarQube
                echo "Initiating SonarQube Scan..."
                withSonarQubeEnv('SonarServer') {
                    sh """
                    ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                      -Dsonar.projectKey=my_jenkins_app \
                      -Dsonar.projectName='My Jenkins App' \
                      -Dsonar.projectVersion=${env.APP_VERSION} \
                      -Dsonar.sources=. \
                      -Dsonar.python.version=3
                    """
                }
            }
        }

        stage('Unit Testing') {
            steps {
                // Q6: Execution of automated unit tests
                echo "Running Python Unit Tests..."
                sh "python3 -m pytest tests/unit_tests.py --junitxml=reports/unit_results.xml"
            }
        }

        stage('Quality Gate') {
            steps {
                // Q5: Quality Gate requirement
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('E2E & Performance Tests') {
            parallel {
                stage('Playwright E2E') {
                    steps {
                        // Q7: End-to-End User Journey Testing
                        echo "Executing Playwright E2E Tests..."
                        sh "python3 tests/user_journey.py"
                    }
                }
                stage('Locust Performance') {
                    steps {
                        // Q8: Performance/Load Testing
                        echo "Executing Locust Load Tests..."
                        sh "locust -f locustfile.py --headless -u 10 -r 2 --run-time 1m"
                    }
                }
            }
        }
    }

    post {
        always {
            // Archive test results for visualization
            junit 'reports/**/*.xml'
            echo "Pipeline complete for version ${env.APP_VERSION}"
        }
        success {
            echo "Deployment to Staging successful."
        }
        failure {
            echo "Pipeline failed. Review SonarQube dashboard or test logs."
        }
    }
}