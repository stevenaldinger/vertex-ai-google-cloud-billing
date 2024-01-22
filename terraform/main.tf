provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region

  # required or else creating api keys throws this error:
  # │ Error: Error creating Key: failed to create a diff: failed to retrieve Key resource:
  # googleapi: Error 403: Your application is authenticating by using local Application Default Credentials.
  #  The apikeys.googleapis.com API requires a quota project, which is not set by default. To
  # learn how to set your quota project, see https://cloud.google.com/docs/authentication/adc-troubleshooting/user-creds .
  #
  billing_project       = var.gcp_project_id
  user_project_override = true
}

terraform {
  required_providers {
    # https://registry.terraform.io/providers/hashicorp/google/latest/docs
    google = {
      source  = "hashicorp/google"
      version = ">= 5"
    }
  }
}
