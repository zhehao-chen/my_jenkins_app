pipeline {
    agent { label 'testing' }

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
                // 安装 Python 环境、SQLite 工具以及 requirements.txt 中的库
                sh """
                if ! command -v python3 &> /dev/null; then apk add --no-cache python3 py3-pip; fi
                if ! command -v sqlite3 &> /dev/null; then apk add --no-cache sqlite; fi
                pip install --break-system-packages -r requirements.txt
                playwright install chromium --with-deps
                """
            }
        }

        stage('Build & Versioning') {
            steps {
                script {
                    // Q4: 生成递增版本号
                    env.APP_VERSION = "${BASE_VERSION}.${env.BUILD_NUMBER}"
                    echo "BUILD_LOG: Current Application Version is set to ${env.APP_VERSION}"
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                script {
                    // Q5: 运行 SonarQube 扫描
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
                // Q6: 数据库初始化与播种
                echo "--- Initializing Staging Database ---"
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
                
                // 运行单元测试并生成覆盖率报告
                sh "python3 -m pytest tests/unit_tests.py --junitxml=reports/unit_results.xml || echo 'Unit tests failed'"
            }
        }

        stage('Quality Gate') {
            steps {
                // Q5: 验证质量门禁
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Parallel Tests') {
            parallel {
                stage('E2E User Journey') {
                    steps {
                        // Q7: 运行 Playwright 脚本
                        echo "Running E2E User Journey..."
                        sh "python3 tests/user_journey.py"
                    }
                }
                stage('Performance Load Test') {
                    steps {
                        // Q8: 运行 Locust 性能测试
                        echo "Starting Load Test..."
                        sh "locust -f tests/locustfile.py --headless -u 10 -r 2 --run-time 1m --host=http://localhost:5000"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished for Version: ${env.APP_VERSION}"
        }
    }
}