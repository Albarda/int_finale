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


        stage('Run Pylint') {
    steps {
        script {
            def pylint_output = sh(script: 'pylint **/*.py || true', returnStdout: true).trim()
            def pylint_score = 0

            // Extract the pylint score from the output
            def matcher = (pylint_output =~ /Your code has been rated at ([\-0-9.]+)/)
            if (matcher.matches()) {
                pylint_score = Float.parseFloat(matcher[0][1])
            }

            println "Pylint score: ${pylint_score}"

            if (pylint_score < 0) {
                error "Pylint score is under 5. Exiting build."
            }
        }
    }
}


        stage('Build DB_APP Docker Image') {
        steps {
            script {
                def version = sh(script: 'cat version.txt', returnStdout: true).trim()
                sh "sudo docker build -f /home/ec2-user/int_finale/Dockerfile -t ${DOCKER_REGISTRY_DB_APP}:${version}.${BUILD_NUMBER} ."
                sh "sudo docker tag ${DOCKER_REGISTRY_DB_APP}:${version}.${BUILD_NUMBER} ${DOCKER_REGISTRY_DB_APP}:latest"
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
                       sudo docker push ${DOCKER_REGISTRY_DB_APP}:latest
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
