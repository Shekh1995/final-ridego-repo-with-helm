# RideGo Helm chart

This chart deploys all four RideGo services. It assumes the application images have already been published to an accessible container registry.

## Install

```bash
helm lint ./helm/ridego
helm upgrade --install ridego ./helm/ridego --namespace ridego --create-namespace
kubectl get pods,svc -n ridego
```

The default frontend service is a `LoadBalancer`. For a local cluster such as Minikube or Kind, use a safer local override:

```bash
helm upgrade --install ridego ./helm/ridego --namespace ridego --create-namespace \
  --set frontend.service.type=ClusterIP
kubectl port-forward -n ridego service/ridego-ridego-frontend 8080:80
```

## Customize an image release

```bash
helm upgrade --install ridego ./helm/ridego -n ridego --create-namespace \
  --set frontend.image.repository=ghcr.io/YOUR_USER/ridego-frontend \
  --set frontend.image.tag=1.1.0 \
  --set rideService.image.repository=ghcr.io/YOUR_USER/ridego-ride-service \
  --set bookingService.image.repository=ghcr.io/YOUR_USER/ridego-booking-service \
  --set contactService.image.repository=ghcr.io/YOUR_USER/ridego-contact-service
```

For repeatable environments, copy `values.yaml` to `values-dev.yaml` or `values-prod.yaml`, change images, replicas, service type, storage class and ingress settings there, then run `helm upgrade --install ... -f values-prod.yaml`.

## Important storage note

The booking and contact services use SQLite on persistent volumes. Each stays at one replica because a ReadWriteOnce PVC does not support multiple database writers. For multi-replica production workloads, move these services to PostgreSQL or Cloud SQL first.
