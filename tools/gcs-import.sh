#/bin/bash

source ./config.sh

gcloud healthcare fhir-stores import gcs $FHIR_STORE --dataset=$DATASET_ID --location=$CLOUD_REGION --gcs-uri=gs://cabral-healthcare/fhir-json-samples/files.ndjson --content-structure=RESOURCE
