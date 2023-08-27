pipeline {
    agent any

    environment {
        DOCKER_REGISTRY_NGINX = '019273956931.dkr.ecr.eu-west-1.amazonaws.com/soulwhisper-nginx'
        DOCKER_REGISTRY_NODE = '019273956931.dkr.ecr.eu-west-1.amazonaws.com/soulwhisper-node'
        APP_NAME = 'soulwhisper'
        HELM_CHART_PATH = 'soulwhisper-chart'
        AWS_REGION = 'eu-west-1' // Set your AWS region to Ireland
        EKS_CLUSTER_NAME = 'devops-int-2023' // Set your EKS cluster name
        NAMESPACE_JENKINS = 'ben-jenkins'
        NAMESPACE_POLLYAPP = 'ben-pollyapp'
        NAMESPACE_ARGO = 'ben-argo'
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
                sh "docker build -f Dockerfile-nginx -t ${DOCKER_REGISTRY_NGINX}:${version}.${BUILD_NUMBER} ."
            }
        }
    }

    stage('Build Node.js Docker Image') {
        steps {
            script {
                def version = sh(script: 'cat version.txt', returnStdout: true).trim()
                sh "docker build -f Dockerfile-node -t ${DOCKER_REGISTRY_NODE}:${version}.${BUILD_NUMBER} ."
            }
        }
    }

    stage('Push Nginx Docker Image') {
        steps {
            withCredentials([usernamePassword(credentialsId: 'AWS-Credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                script {
                    def version = sh(script: 'cat version.txt', returnStdout: true).trim()
                    sh """
                       aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ${DOCKER_REGISTRY_NGINX}
                       docker push ${DOCKER_REGISTRY_NGINX}:${version}.${BUILD_NUMBER}
                    """
                }
            }
        }
    }

    stage('Push Node.js Docker Image') {
        steps {
            withCredentials([usernamePassword(credentialsId: 'AWS-Credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                script {
                    def version = sh(script: 'cat version.txt', returnStdout: true).trim()
                    sh """
                       aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ${DOCKER_REGISTRY_NODE}
                       docker push ${DOCKER_REGISTRY_NODE}:${version}.${BUILD_NUMBER}
                    """
                }
            }
        }
    }


 stage('Update Version') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'git-credentials', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASSWORD')]) {
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

stage('Deploying to Kubernetes using Helm') {
    steps {
        withCredentials([
            file(credentialsId: 'soulwhisper-kubeconfig', variable: 'KUBECONFIG_FILE'),
            usernamePassword(credentialsId: 'AWS-Credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')
        ]) {
            script {
                env.KUBECONFIG_PATH = sh(returnStdout: true, script: 'mktemp').trim()
                sh "cp '${KUBECONFIG_FILE}' \"${env.KUBECONFIG_PATH}\""
                sh "aws eks update-kubeconfig --region eu-west-1 --name devops-int-2023 --kubeconfig=\"${env.KUBECONFIG_PATH}\""

                // Get the chart version from the chart metadata
                env.CHART_VERSION = sh(returnStdout: true, script: "helm show chart ${HELM_CHART_PATH} | grep version | cut -d ' ' -f 2").trim()

                // Namespaces to deploy to
                def namespaces = [NAMESPACE_JENKINS, NAMESPACE_POLLYAPP]

                // Add the Jenkins Helm chart repo
                sh "helm repo add jenkinsci https://charts.jenkins.io"
                sh "helm repo update"

                for (namespace in namespaces) {
                    if (namespace == NAMESPACE_JENKINS) {
                        // Print Jenkins values for debugging
                        sh "cat jenkins-values.yaml"
                        
                        // Deploy Jenkins to the 'ben-jenkins' namespace using updated values
                        sh "helm upgrade --install jenkins jenkinsci/jenkins --namespace ${namespace} --create-namespace --kubeconfig=\"${env.KUBECONFIG_PATH}\" -f jenkins-values.yaml"
                    } else if (namespace == NAMESPACE_POLLYAPP) {
                        // Remove existing resources
                        sh "helm delete ${APP_NAME} --namespace ${namespace} --kubeconfig=\"${env.KUBECONFIG_PATH}\" || true"

                        // Packages and redeploy the helm chart
                        sh "helm package ${HELM_CHART_PATH}"
                        sh "helm upgrade --install --namespace ${namespace} --create-namespace --kubeconfig=\"${env.KUBECONFIG_PATH}\" -f soulwhisper-chart/values.yaml ${APP_NAME} ./soulwhisper-${env.CHART_VERSION}.tgz"
                    }
                }
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
