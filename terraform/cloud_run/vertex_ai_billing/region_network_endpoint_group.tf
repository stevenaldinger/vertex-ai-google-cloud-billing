resource "google_compute_region_network_endpoint_group" "vertex_ai_billing" {
  name = var.name

  network_endpoint_type = "SERVERLESS"

  region = var.location

  cloud_run {
    service = google_cloud_run_v2_service.vertex_ai_billing.name
  }
}
