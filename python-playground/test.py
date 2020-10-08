import fhirclient.models.patient as p
import fhirclient.models.humanname as hn
import argparse
import json
import os

from google.auth.transport import requests
from google.oauth2 import service_account

_BASE_URL = "https://healthcare.googleapis.com/v1"
PROJECT_ID = "cabral-healthcare"
CLOUD_REGION = "southamerica-east1"
DATASET_ID = "cabral-dataset"
FHIR_STORE = "cabral-fhir"

# [START healthcare_get_session]
def get_session():
    """Creates an authorized Requests Session."""

    # Pass in the credentials and project ID. If none supplied, get them
    # from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    return session
# [END healthcare_get_session]

def create_patient(base_url, project_id, cloud_region, dataset_id, fhir_store_id):
    """Creates a new Patient resource in a FHIR store."""
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    fhir_store_path = "{}/datasets/{}/fhirStores/{}/fhir/Patient".format(
        url, dataset_id, fhir_store_id
    )

    # Make an authenticated API request
    session = get_session()

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    patient = p.Patient({'id': 'patient-1'})

    # body = {
    #     "name": [{"use": "official", "family": "Smith", "given": ["Darcy"]}],
    #     "gender": "female",
    #     "birthDate": "1970-01-01",
    #     "resourceType": "Patient",
    # } 

    body = patient.as_json()

    response = session.post(fhir_store_path, headers=headers, json=body)
    response.raise_for_status()

    resource = response.json()

    print("Created Patient resource with ID {}".format(resource["id"]))

    return response


patient = p.Patient({'id': 'patient-1'})
print(patient.as_json())

create_patient(_BASE_URL, PROJECT_ID, CLOUD_REGION, DATASET_ID, FHIR_STORE)

