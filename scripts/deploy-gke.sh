#!/usr/bin/env bash
set -euo pipefail
USER="${1:?Usage: $0 DOCKERHUB_USERNAME [TAG]}"
TAG="${2:-latest}"
kubectl apply -k k8s/
for s in frontend car-service booking-service contact-service; do
  kubectl -n carshop set image deployment/$s $s="docker.io/$USER/carshop-$s:$TAG"
done
for s in frontend car-service booking-service contact-service; do
  kubectl -n carshop rollout status deployment/$s --timeout=180s
done
kubectl get pods -n carshop -o wide
kubectl get svc -n carshop
