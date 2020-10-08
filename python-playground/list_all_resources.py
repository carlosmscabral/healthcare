import argparse
import json
import os

from google.auth.transport import requests
from google.oauth2 import service_account

_BASE_URL="https://healthcare.googleapis.com/v1"
PROJECT_ID="cabral-healthcare"
CLOUD_REGION="southamerica-east1"
DATASET_ID="cabral-dataset"
FHIR_STORE="cabral-fhir"


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

def search_resources_get(
    base_url, project_id, cloud_region, dataset_id, fhir_store_id, resource_type,
):
    """
    Searches resources in the given FHIR store.
    It uses the searchResources GET method.
    """
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}".format(
        url, dataset_id, fhir_store_id, resource_type
    )

    # Make an authenticated API request
    session = get_session()

    response = session.get(resource_path)
    response.raise_for_status()

    resources = response.json()

    print(
        "Using GET request, found a total of {} {} resources:".format(
            resources["total"], resource_type
        )
    )
    print(json.dumps(resources, indent=2))

    return resources

def main():

    for resource in "Patient", "Practitioner", "PractitionerRole", "Encounter":
        results = search_resources_get(_BASE_URL,PROJECT_ID, CLOUD_REGION, DATASET_ID, FHIR_STORE, resource)
        print("RESOURCE --- " + resource)
        for p in results["entry"]:
            print(json.dumps(p["resource"], indent=2))
            print("------------")


if __name__ == "__main__":
    main()