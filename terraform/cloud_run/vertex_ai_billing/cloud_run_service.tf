resource "google_cloud_run_v2_service" "vertex_ai_billing" {
  name     = var.name
  location = var.location

  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = module.vertex_ai_billing_service_account.email

    labels = {
      app = var.name
    }

    scaling {
      min_instance_count = var.scaling_min_instance_count
      max_instance_count = var.scaling_max_instance_count
    }

    max_instance_request_concurrency = var.max_instance_request_concurrency

    containers {
      image = var.image

      env {
        name  = "BIGQUERY_DATASET"
        value = var.bigquery_dataset
      }

      env {
        name  = "GCP_PROJECT"
        value = var.gcp_project_id
      }

      env {
        name  = "GCP_REGION"
        value = var.location
      }

      startup_probe {
        initial_delay_seconds = 3
        timeout_seconds       = 3
        period_seconds        = 5
        failure_threshold     = 3
        tcp_socket {
          port = 8080
        }
      }

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = var.resources_limits_cpu
          memory = var.resources_limits_memory
        }

        # might save some money if we set this to true
        cpu_idle = true

        startup_cpu_boost = true
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "vertex-ai-billing-public-access" {
  project  = google_cloud_run_v2_service.vertex_ai_billing.project
  location = google_cloud_run_v2_service.vertex_ai_billing.location
  name     = google_cloud_run_v2_service.vertex_ai_billing.name

  role   = "roles/run.invoker"
  member = "allUsers"
}
