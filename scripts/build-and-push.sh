#!/usr/bin/env bash
# Creates the four public Docker Hub images required by k8s/deploy.yaml.
set -euo pipefail

DOCKER_USER="${DOCKER_USER:-shekhar013}"
TAG="${TAG:-1.0.0}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker Engine/Desktop is required to build and push the images." >&2
  exit 1
fi

docker login -u "$DOCKER_USER"
for service in frontend car-service booking-service contact-service; do
  image="docker.io/$DOCKER_USER/carshop-$service:$TAG"
  docker build --pull --tag "$image" "services/$service"
  docker push "$image"
done

echo "Published all images with tag $TAG. Deploy with Helm: helm upgrade --install ridego ./helm/ridego -n ridego --create-namespace (set each service image tag to $TAG)"
