terraform {
  backend "gcs" {
    bucket = "dh-bucket-0813"
    prefix = "terraform/state"
  }
}

data "google_client_config" "provider" {}

locals {
  project_id = var.project_id
  gcp_region = var.region
  prefix     = var.prefix
}

provider "google" {
  project = local.project_id
  region  = local.gcp_region
}

module "gcp-network" {
  source = "./module-network"

  project_id  = local.project_id
  region      = local.gcp_region
  vpc_name    = "adas-vpc"
  subnet_cidr = "10.10.0.0/24"
  prefix      = local.prefix
}

module "gcp-gke" {
  source = "./module-gke"

  project_id   = local.project_id
  region       = local.gcp_region
  cluster_name = "dh-grad-cluster"
  vpc_name     = module.gcp-network.vpc_network
  subnet_id    = module.gcp-network.subnet_id
  machine_type = "e2-medium"
  prefix       = local.prefix
}