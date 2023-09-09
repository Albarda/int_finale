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
                       aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ${DOCKER_REGISTRY_DB_APP}
                       sudo docker push ${DOCKER_REGISTRY_DB_APP}:${version}.${BUILD_NUMBER}
                    """
                }
            }
        }
    }


 stage('Update Version') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'alon_github', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASSWORD')]) {
                    script {
                        def version = sh(script: 'cat version.txt', returnStdout: true).trim()
                        println "Current version: ${version}"
                        def (major, minor, patch) = version.tokenize('.')
                        patch = patch.toInteger() + 1
                        def newVersion = "${major}.${minor}.${patch}"
                        
                        sh """
                            git stash
                            git checkout main
                            echo "echo \${GIT_PASSWORD}" > askpass.sh
                            chmod +x askpass.sh
                            export GIT_ASKPASS=\$(pwd)/askpass.sh
                            git pull --rebase origin main
                            git stash apply
                            echo ${newVersion} > version.txt
                            echo "New version:"
                            cat version.txt
                            git add version.txt
                            GIT_DIFF=\$(git diff --staged --quiet || echo 'Changes')
                            if [[ \${GIT_DIFF} == 'Changes' ]]; then
                                git commit -m 'Increment version to ${newVersion}'
                                git push origin main
                            else
                                echo "No changes to commit"
                            fi
                        """
                    }
                }
            }
        }


        stage('Cleanup Jenkins Server') {
            // change test
            steps {
                sh 'docker system prune -a -f'
            }
        }
    }
}
