variable "project_id" {
  type = string
}

variable "prefix" {
  type = string
}

variable "region" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable "vpc_name" {
  type = string
}

variable "gke_num_nodes" {
  type    = number
  default = 3
}

variable "subnet_id" {
  type    = string
  default = "subnet"
}

variable "machine_type" {
  type = string
}