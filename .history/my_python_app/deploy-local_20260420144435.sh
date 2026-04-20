#!/usr/bin/env bash
# -------------------------------------------------------
# Quick-start: build & deploy to Minikube
# Usage:  ./deploy-local.sh
# -------------------------------------------------------
set -euo pipefail

APP_NAME="my-app"
APP_VERSION="1.0.0"
NAMESPACE="dijato"

# ---- pre-flight checks --------------------------------
for cmd in minikube kubectl docker; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "ERROR: '$cmd' is not installed. Please install it first."
    exit 1
  fi
done

# ---- start minikube if not running --------------------
if ! minikube status --format='{{.Host}}' 2>/dev/null | grep -q Running; then
  echo "Starting Minikube..."
  minikube start --driver=docker
fi

# ---- point Docker CLI at Minikube's daemon -------------
echo "Configuring Docker to use Minikube's daemon..."
eval $(minikube docker-env)

# ---- build the image -----------------------------------
echo "Building ${APP_NAME}:${APP_VERSION} ..."
docker build -t "${APP_NAME}:${APP_VERSION}" .

# ---- deploy to Kubernetes ------------------------------
echo "Applying Kubernetes manifests..."
kubectl apply -f namespace.yaml
kubectl apply -f Deployment.yaml
kubectl apply -f Service.yaml

# ---- wait for rollout ----------------------------------
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/myapp-deployment -n "${NAMESPACE}" --timeout=120s

# ---- open in browser -----------------------------------
echo ""
echo "=============================="
echo " Deployment complete!"
echo "=============================="
echo ""
echo "Run the following to open the app in your browser:"
echo "  minikube service myapp-service -n ${NAMESPACE}"
echo ""
echo "Useful commands:"
echo "  kubectl get pods -n ${NAMESPACE}"
echo "  kubectl logs -f deployment/myapp-deployment -n ${NAMESPACE}"
echo "  kubectl port-forward svc/myapp-service 8080:80 -n ${NAMESPACE}"
