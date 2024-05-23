#!/bin/bash

# Set environement variables for Google Cloud
export GCP_PROJECT_ID="helical-ion-423904-u2"
export GCP_SERVICE_ACCOUNT_NAME="grad-proj@$GCP_PROJECT_ID.iam.gserviceaccount.com"
export GCP_SERVICE_ACCOUNT_KEYFILE="/home/dusdjhyeon/grad-proj.json"
export BASE64ENCODED_GCP_PROVIDER_CREDS=$(base64 $GCP_SERVICE_ACCOUNT_KEYFILE | tr -d "\n") # base64 encode the GCP credentials

export GKE_CLUSTER_NAME="dh-gke"
export GKE_CLUSTER_ZONE="asia-northeast3-c"

# Set environment vars for Crossplane installation
export CROSSPLANE_VERSION="1.16.0"
export CROSSPLANE_NS="crossplane"