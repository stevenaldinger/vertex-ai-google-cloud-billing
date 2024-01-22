resource "google_project_service" "services" {
  for_each = toset([
    # for vertex ai
    "aiplatform.googleapis.com",
    # for artifact registry
    "artifactregistry.googleapis.com",
    # for bigquery api
    "bigquery.googleapis.com",
    # for bigquery connection api
    "bigqueryconnection.googleapis.com",
    # for building docker images
    "cloudbuild.googleapis.com",
    # for deploying cloud functions and bigquery remote functions
    "cloudfunctions.googleapis.com",
    # for interacting with google developers console api
    "cloudresourcemanager.googleapis.com",
    # for supervised learning pipeline
    # "compute.googleapis.com",
    # for deploying chatbot cloud run service
    "containerregistry.googleapis.com",
    # for generative language api
    "generativelanguage.googleapis.com",
    # necessary for service account management
    "iam.googleapis.com",
    # for logging
    "logging.googleapis.com",
    # for deploying chatbot cloud run service
    "run.googleapis.com",
    # for listing project services so we can edit and enable them
    "serviceusage.googleapis.com",
  ])

  service = each.key
}
