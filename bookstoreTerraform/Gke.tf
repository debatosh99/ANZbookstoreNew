variable "gke_username" {
  default     = ""
  description = "gke username"
}

variable "gke_password" {
  default     = ""
  description = "gke password"
}

# GKE cluster
resource "google_container_cluster" "primary" {
  name     = "playground-s-11-787290ee-gke"
  location = "us-central1"

#  network    = google_compute_network.vpc.name
#  subnetwork = google_compute_subnetwork.subnet.name
  network    = "default"
  subnetwork = "default"

# Enabling Autopilot for this cluster
  enable_autopilot = true
}