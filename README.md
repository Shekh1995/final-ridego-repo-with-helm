# RideGo — Cloud-Native Ride Booking Demo

RideGo is a Rapido-inspired, full-stack ride-booking application built to demonstrate a practical microservices deployment on Docker, Kubernetes, Jenkins, and GKE.

> This is an independent demo project. It is not affiliated with Rapido.

## What it does

- Lets riders book a Bike, Auto, or Cab ride
- Shows an INR fare estimate based on selected ride and distance
- Captures pickup, destination, rider name, and mobile number
- Persists confirmed bookings and support messages in SQLite volumes
- Provides health and readiness endpoints for Kubernetes
- Includes Docker Compose for local use and Kubernetes/Jenkins manifests for deployment

## Architecture

| Service | Port | Responsibility |
| --- | ---: | --- |
| `frontend` | 8080 | Responsive website and API gateway |
| `car-service` | 5001 | Ride fleet and fare-estimate API (legacy directory name retained) |
| `booking-service` | 5002 | Booking validation and persistence |
| `contact-service` | 5003 | Support message persistence |

## Run locally

Prerequisite: Docker Desktop or Docker Engine.

```bash
docker compose up --build
```

Open [http://localhost:8080](http://localhost:8080). Stop the stack with `docker compose down`; named volumes preserve demo data.

## APIs

```text
GET  /api/rides
GET  /api/estimate?ride_type=bike&distance_km=5
POST /api/bookings
POST /api/contact
GET  /health
GET  /ready
```

Example booking request:

```json
{
  "name": "Asha", "phone": "9876543210", "pickup": "MG Road",
  "destination": "Indiranagar", "ride_type": "bike",
  "distance_km": 5, "estimated_fare": 65
}
```

## Deploy to GKE

Build and publish the images with `scripts/build-and-push.sh` (or `scripts/build-and-push.ps1` on Windows), then configure your cluster credentials and apply the self-contained manifest:

```bash
kubectl apply -f k8s/deploy.yaml
kubectl get pods,svc -n carshop
```

The manifests retain their original `carshop` namespace and image names so existing CI/CD configuration continues to work. For production, replace SQLite with a managed database, use Secret Manager, add HTTPS ingress, autoscaling, observability, and a real dispatch/driver service.

## Deploy with Helm (recommended)

The reusable chart is in [`helm/ridego`](helm/ridego). Helm turns a set of Kubernetes templates and configurable values into a named, versioned release. Install all RideGo services with:

```bash
helm lint ./helm/ridego
helm upgrade --install ridego ./helm/ridego --namespace ridego --create-namespace
```

See the [chart guide](helm/ridego/README.md) for image overrides, local-cluster access, ingress, storage, upgrades, and production notes.

## Test

```bash
pytest
```
