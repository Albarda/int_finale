pipeline {
    agent any

    environment {
        DOCKER_REGISTRY_DB_APP = '704059047372.dkr.ecr.eu-west-1.amazonaws.com/db_app'
        APP_NAME = 'db_app'
        AWS_REGION = 'eu-west-1' // Set your AWS region to Ireland
        EKS_CLUSTER_NAME = 'devops-int-2023' // Set your EKS cluster name
        BUILD_NUMBER = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -la' // this will list all files in the current directory
            }
        }

          stage('Install Pylint') {
            steps {
                sh 'pip install pylint' // Or use any method to install pylint
            }
        }

        stage('Run Pylint') {
            steps {
                sh 'pylint **/*.py || exit 0' // This will run pylint on all .py files and will not fail the build
            }
        }


        stage('Build Nginx Docker Image') {
        steps {
            script {
                def version = sh(script: 'cat version.txt', returnStdout: true).trim()
                sh "sudo docker build -f /home/ec2-user/int_finale/Dockerfile -t ${DOCKER_REGISTRY_DB_APP}:${version}.${BUILD_NUMBER} ."
            }
        }
    }


    stage('Push DB_APP Docker Image') {
        steps {
            withCredentials([usernamePassword(credentialsId: 'AWS-Credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                script {
                    def version = sh(script: 'cat version.txt', returnStdout: true).trim()
                    sh """
                       aws ecr get-login-password --region eu-west-1 | sudo docker login --username AWS --password-stdin ${DOCKER_REGISTRY_DB_APP}
                       sudo docker push ${DOCKER_REGISTRY_DB_APP}:${version}.${BUILD_NUMBER}
                    """
                }
            }
        }
    }


        stage('Cleanup Jenkins Server') {
            // change test
            steps {
                sh 'sudo docker system prune -a -f'
            }
        }
    }
}
