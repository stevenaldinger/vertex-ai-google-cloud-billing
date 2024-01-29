# Vertex AI x GCP Billing (BigQuery Exports)

This is the companion repository for my [Vertex AI and BigQuery for Natural Language Exploration of GCP Billing Data](https://medium.com/teamsnap-engineering/vertex-ai-and-bigquery-for-natural-language-exploration-of-gcp-billing-data-7f96b13c7a7e) article and contains a service that can be deployed to Cloud Run to integrate Vertex AI's Gemini Pro model with Google Cloud Billing Exports in BigQuery to enable you to ask natural language questions about your billing data.

If you already have billing set up to be exported to BigQuery, everything you need to run this service is in this repository.

Instructions for getting the service built and deployed can be found at [docs/quick_start.md](docs/quick_start.md).

The automation and documentation in this repo is based on my [Generative AI](https://github.com/stevenaldinger/generative-ai) repo.

## WARNING

This is a proof of concept setup and is not securely deployed. The Cloud Run service will be publicly available, so if you try the demo, make sure to delete the service when you're done. You can do that with the `make terraform_destroy_vertex_ai_billing_service` command.

![Vertex AI Billing Demo](docs/images/01_vertex-ai-billing-demo.png)
