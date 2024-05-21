output "gke_cluster_id" {
  value = google_container_cluster.main_cluster.id
}

output "gke_cluster_name" {
  value = google_container_cluster.main_cluster.name
}

output "gke_cluster_endpoint" {
  value = google_container_cluster.main_cluster.endpoint
}
