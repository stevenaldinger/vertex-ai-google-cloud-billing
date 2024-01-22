# Deploying to Cloud Run

Make sure you've [authed with gcloud](gcloud_auth.md) and [set up your project and infrastructure](infrastructure_setup.md) before running these steps.

You can easily push a new version of the docker image to Google Container Registry at any time by running:

```sh
make push_image
```

The `push_image` target also configures your [.env](../.env) file with the `VERTEX_AI_BILLING_SERVICE_IMAGE` variable, which should look like `gcr.io/<project-name>/vertex-ai-billing:latest`

You'll need to manually configure the `VERTEX_AI_BILLING_SERVICE_BIGQUERY_DATASET` variable in your [.env](../.env) file to point to the BigQuery dataset you want to use.

Then, deploy the app to Cloud Run with Terraform:

```sh
make terraform_apply
```
