# main control을 위한 기본 spec 수준의 gke 구성

resource "google_container_cluster" "main_cluster" {
  name                     = "${var.prefix}-gke"
  project                  = var.project_id
  location                 = var.region
  min_master_version       = "1.29"
  remove_default_node_pool = true
  initial_node_count       = 1
  network                  = var.vpc_name
  subnetwork               = var.subnet_id
}

resource "google_container_node_pool" "node_pool" {
  project    = var.project_id
  name       = "${google_container_cluster.main_cluster.name}-node-pool"
  location   = var.region
  cluster    = google_container_cluster.main_cluster.name
  node_count = var.gke_num_nodes
  node_config {
    machine_type = var.machine_type

    oauth_scopes = [
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}