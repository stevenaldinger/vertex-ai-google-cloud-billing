# Terraform

This directory contains the Terraform configuration for the project. It's used to set up the Google Cloud project and resources needed to run the examples.

**NOTE:** all the environment variables outside of `GCP_PROJECT` are configured automatically if you followed the steps in the [Quick Start](../docs/quick_start.md) instructions (the `make` commands for local config setup).

The following environment variables are configured in the [docker-compose.yml](./docker-compose.yml) file:
- `GCP_PROJECT` environment variable gets mapped to `TF_VAR_gcp_project_id` - the Google Cloud project id to configure and create resources in
- `GCP_REGION` environment variable gets mapped to `TF_VAR_gcp_region` - the Google Cloud region to create resources in
- `VERTEX_AI_BILLING_SERVICE_IMAGE` environment variable gets mapped to `TF_VAR_vertex_ai_billing_service_image` - the Docker image to use for the vertex-ai-billing service. if this is an empty string (default), the vertex-ai-billing service will not be deployed.
- `VERTEX_AI_BILLING_SERVICE_BIGQUERY_DATASET` environment variable gets mapped to `TF_VAR_vertex_ai_billing_service_bigquery_dataset` - the BigQuery dataset to use for the vertex-ai-billing service. if this is an empty string (default), the vertex-ai-billing service will not be deployed.
