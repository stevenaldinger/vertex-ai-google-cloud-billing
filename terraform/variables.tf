variable "gcp_project_id" {
  description = "The GCP Project ID to create resources in."
  type        = string
}

variable "gcp_region" {
  description = "The GCP region to create resources in."
  type        = string
  default     = "us-central1"
}

variable "vertex_ai_billing_service_image" {
  description = "If a docker image is set, the vertex-ai-billing service will be deployed."
  type        = string
  default     = ""
}

variable "vertex_ai_billing_service_bigquery_dataset" {
  description = "The BigQuery dataset to retrieve billing data from."
  type        = string
}
