
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.113" }
  }
}
provider "azurerm" { features {} }
# Example AKS (uncomment and set vars)
# resource "azurerm_kubernetes_cluster" "aks" {
#   name                = var.cluster_name
#   location            = var.location
#   resource_group_name = var.resource_group
#   dns_prefix          = var.cluster_name
#   default_node_pool {
#     name       = "default"
#     node_count = 2
#     vm_size    = "Standard_DS2_v2"
#   }
#   identity { type = "SystemAssigned" }
# }
