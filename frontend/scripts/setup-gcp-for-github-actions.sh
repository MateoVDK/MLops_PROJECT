#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="sublime-lyceum-498409-j6"
REGION="europe-west1"
ZONELESS_LOCATION="europe-west1"
CLUSTER_NAME="blackjack-cluster"
ARTIFACT_REPOSITORY="blackjack"
BUCKET_NAME="kenneth-pierloz-mlops"
SA_NAME="github-actions-mlops"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "Using project: ${PROJECT_ID}"
gcloud config set project "${PROJECT_ID}"

echo "Enabling required Google Cloud APIs..."
gcloud services enable \
  iam.googleapis.com \
  iamcredentials.googleapis.com \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  artifactregistry.googleapis.com \
  container.googleapis.com \
  cloudresourcemanager.googleapis.com

echo "Creating GitHub Actions service account if needed..."
if ! gcloud iam service-accounts describe "${SA_EMAIL}" >/dev/null 2>&1; then
  gcloud iam service-accounts create "${SA_NAME}" \
    --display-name="GitHub Actions MLOps"
fi

echo "Granting project IAM roles to the GitHub Actions service account..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/container.admin"

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/iam.serviceAccountUser"

echo "Allowing the service account to act as itself for Vertex AI training jobs..."
gcloud iam service-accounts add-iam-policy-binding "${SA_EMAIL}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/iam.serviceAccountUser" || true

echo "Creating Artifact Registry Docker repository if needed..."
if ! gcloud artifacts repositories describe "${ARTIFACT_REPOSITORY}" --location="${REGION}" >/dev/null 2>&1; then
  gcloud artifacts repositories create "${ARTIFACT_REPOSITORY}" \
    --repository-format=docker \
    --location="${REGION}" \
    --description="Blackjack MLOps Docker images"
fi

echo "Creating Cloud Storage bucket if needed..."
if ! gcloud storage buckets describe "gs://${BUCKET_NAME}" >/dev/null 2>&1; then
  gcloud storage buckets create "gs://${BUCKET_NAME}" \
    --project="${PROJECT_ID}" \
    --location="${REGION}" \
    --uniform-bucket-level-access
fi

echo "Creating GKE Autopilot cluster if needed..."
if ! gcloud container clusters describe "${CLUSTER_NAME}" --region="${REGION}" >/dev/null 2>&1; then
  gcloud container clusters create-auto "${CLUSTER_NAME}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}"
fi

echo "Getting kubectl credentials..."
gcloud container clusters get-credentials "${CLUSTER_NAME}" \
  --region="${REGION}" \
  --project="${PROJECT_ID}"

echo "Creating Kubernetes namespace if needed..."
kubectl create namespace blackjack --dry-run=client -o yaml | kubectl apply -f -

echo "Creating a temporary model ConfigMap from the current backend policy, if the file exists..."
if [ -f "backend/app/predictor/policy.pkl" ]; then
  kubectl create configmap blackjack-policy \
    --namespace=blackjack \
    --from-file=policy.pkl=backend/app/predictor/policy.pkl \
    --dry-run=client \
    -o yaml | kubectl apply -f -
else
  echo "backend/app/predictor/policy.pkl not found in current folder. Skipping initial model ConfigMap."
fi

echo ""
echo "DONE."
echo ""
echo "Create these GitHub secrets:"
echo "GCP_PROJECT_ID = ${PROJECT_ID}"
echo "GKE_CLUSTER    = ${CLUSTER_NAME}"
echo ""
echo "Now create a service account JSON key:"
echo "gcloud iam service-accounts keys create github-actions-key.json --iam-account=\"${SA_EMAIL}\""
echo ""
echo "Then print the JSON secret value:"
echo "python3 -c 'import json; print(json.dumps(json.load(open(\"github-actions-key.json\"))))'"
echo ""
echo "Paste that full one-line JSON into GitHub secret:"
echo "GCP_SA_KEY"
