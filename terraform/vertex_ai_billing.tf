module "vertex_ai_billing" {
  source = "./cloud_run/vertex_ai_billing"
  count  = var.vertex_ai_billing_service_image == "" ? 0 : 1

  gcp_project_id = var.gcp_project_id
  location       = var.gcp_region

  name  = "vertex-ai-billing"
  image = var.vertex_ai_billing_service_image

  max_instance_request_concurrency = 80

  resources_limits_cpu    = "1000m"
  resources_limits_memory = "1000Mi"

  scaling_max_instance_count = 1
  scaling_min_instance_count = 1

  bigquery_dataset = var.vertex_ai_billing_service_bigquery_dataset

  depends_on = [
    google_project_service.services["aiplatform.googleapis.com"],
    google_project_service.services["bigquery.googleapis.com"],
    google_project_service.services["bigqueryconnection.googleapis.com"],
    google_project_service.services["logging.googleapis.com"],
    google_project_service.services["run.googleapis.com"],
  ]
}
