pipeline {
    agent any
    triggers { githubPush() }
    environment { COMPOSE_FILE = 'docker-compose.jenkins.yml' }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Syntax check in container') {
            steps {
                script {
                    docker.image('python:3.12-slim').inside {
                        sh '''python -c "import ast; ast.parse(open('app.py').read())"'''
                    }
                }
            }
        }
        stage('Build and Deploy') {
            steps {
                sh 'docker compose -f $COMPOSE_FILE down || true'
                sh 'docker compose -f $COMPOSE_FILE up -d'
            }
        }
        stage('Verify') {
            steps {
                sh '''
                    for i in $(seq 1 30); do
                        curl -sf http://localhost:8082/ && exit 0
                        sleep 5
                    done
                    docker compose -f $COMPOSE_FILE logs
                    exit 1
                '''
            }
        }
    }

    post {
        always {
            script {
                def author = sh(script: 'git log -1 --pretty=format:%ae', returnStdout: true).trim()
                def who = sh(script: 'git log -1 --pretty=format:%an', returnStdout: true).trim()
                emailext(
                    to: "${author}, cc:mohsin4worknow@gmail.com",
                    subject: "Build #${env.BUILD_NUMBER} ${currentBuild.currentResult}: ${env.JOB_NAME}",
                    body: "Push by: ${who} (${author})\nResult: ${currentBuild.currentResult}\nApp: http://16.192.32.155:8082/\nBuild log: ${env.BUILD_URL}console"
                )
            }
        }
    }
}
