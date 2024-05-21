provider "google" {
  version = "~> 5.7.0"
  project = var.project_id
  region  = var.region
}

# Google VPC 정의
resource "google_compute_network" "vpc" {
  name                    = "${var.prefix}-vpc"
  auto_create_subnetworks = false #서브넷 자동 생성 해제
}

# 서브넷 정의
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.prefix}-subnet-a"
  network       = google_compute_network.vpc.name
  ip_cidr_range = var.subnet_cidr
  region        = var.region
}