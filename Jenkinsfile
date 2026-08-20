pipeline {
  agent { label 'aws-agent' }
  options { skipDefaultCheckout(true); timestamps(); disableConcurrentBuilds() }
  parameters {
    booleanParam(name: 'PUSH_IMAGES', defaultValue: true, description: 'Push images to Docker Hub')
    booleanParam(name: 'DEPLOY_GKE', defaultValue: true, description: 'Deploy to GKE')
  }
  environment { IMAGE_TAG = "${BUILD_NUMBER}"; PREFIX = "carshop" }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Validate') { steps { sh '''
      set -eu
      docker --version
      docker info >/dev/null
      kubectl version --client
      echo "Agent: $(hostname)"
    ''' } }
    stage('Build') { steps { sh '''
      set -eu
      for s in frontend car-service booking-service contact-service; do
        docker build --pull -t "$PREFIX-$s:$IMAGE_TAG" "services/$s"
      done
    ''' } }
    stage('Trivy') { steps { sh '''
      set -eu
      if command -v trivy >/dev/null 2>&1; then
        for s in frontend car-service booking-service contact-service; do
          trivy image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed "$PREFIX-$s:$IMAGE_TAG"
        done
      else
        echo "Trivy is not installed; install it on the AWS agent."
      fi
    ''' } }
    stage('Push') {
      when { expression { params.PUSH_IMAGES } }
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_TOKEN')]) {
          sh '''
            set -eu
            echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
            for s in frontend car-service booking-service contact-service; do
              docker tag "$PREFIX-$s:$IMAGE_TAG" "$DOCKER_USER/$PREFIX-$s:$IMAGE_TAG"
              docker push "$DOCKER_USER/$PREFIX-$s:$IMAGE_TAG"
            done
            docker logout
          '''
        }
      }
    }
    stage('Deploy GKE') {
      when { expression { params.DEPLOY_GKE } }
      steps {
        withCredentials([
          file(credentialsId: 'gke-kubeconfig', variable: 'KUBECONFIG_FILE'),
          usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_TOKEN')
        ]) {
          sh '''
            set -eu
            export KUBECONFIG="$KUBECONFIG_FILE"
            kubectl apply -k k8s/
            for s in frontend car-service booking-service contact-service; do
              kubectl -n carshop set image deployment/$s $s="docker.io/$DOCKER_USER/$PREFIX-$s:$IMAGE_TAG"
            done
            for s in frontend car-service booking-service contact-service; do
              kubectl -n carshop rollout status deployment/$s --timeout=180s
            done
            kubectl get pods -n carshop -o wide
            kubectl get svc -n carshop
          '''
        }
      }
    }
  }
  post { always { sh 'docker logout >/dev/null 2>&1 || true'; cleanWs() } }
}
