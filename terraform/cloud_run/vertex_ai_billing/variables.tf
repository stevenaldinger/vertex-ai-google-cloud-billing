variable "bigquery_dataset" {
  description = "The BigQuery dataset to retrieve billing data from."
  type        = string
}

variable "image" {
  description = "The name of the image to deploy"
  type        = string
}

variable "gcp_project_id" {
  description = "The GCP Project ID to create resources in."
  type        = string
}

variable "location" {
  description = "The location in which to provision resources"
  type        = string
  default     = "us-central1"
}

variable "max_instance_request_concurrency" {
  description = "The maximum number of concurrent requests per instance"
  type        = number
  default     = 80
}

variable "name" {
  description = "The name of the deployment"
  type        = string
  default     = "vertex-ai-billing"
}

variable "resources_limits_cpu" {
  description = "The maximum CPU to allocate to a container. Must be 1 CPU or greater for concurrent requests."
  type        = string
  default     = "1000m"
}

variable "resources_limits_memory" {
  description = "The maximum memory to allocate to a container"
  type        = string
  default     = "1000Mi"
}

variable "scaling_max_instance_count" {
  description = "The maximum number of instances to run"
  type        = number
  default     = 1
}

variable "scaling_min_instance_count" {
  description = "The minimum number of instances to run"
  type        = number
  default     = 1
}
