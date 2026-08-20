# Creates the four public Docker Hub images required by k8s/deploy.yaml.
param(
  [string]$DockerUser = "shekhar013",
  [string]$Tag = "1.0.0"
)

$ErrorActionPreference = "Stop"
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  throw "Docker Desktop/Engine is required to build and push the images."
}

docker login -u $DockerUser
if ($LASTEXITCODE -ne 0) { throw "Docker Hub login failed." }

foreach ($service in "frontend", "car-service", "booking-service", "contact-service") {
  $image = "docker.io/$DockerUser/carshop-$service`:$Tag"
  docker build --pull --tag $image "services/$service"
  if ($LASTEXITCODE -ne 0) { throw "Build failed for $service." }
  docker push $image
  if ($LASTEXITCODE -ne 0) { throw "Push failed for $service." }
}

Write-Host "Published all images with tag $Tag. Deploy with: helm upgrade --install ridego ./helm/ridego -n ridego --create-namespace --set frontend.image.repository=docker.io/$DockerUser/carshop-frontend --set frontend.image.tag=$Tag --set rideService.image.repository=docker.io/$DockerUser/carshop-car-service --set rideService.image.tag=$Tag --set bookingService.image.repository=docker.io/$DockerUser/carshop-booking-service --set bookingService.image.tag=$Tag --set contactService.image.repository=docker.io/$DockerUser/carshop-contact-service --set contactService.image.tag=$Tag"
