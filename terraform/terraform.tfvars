location            = "Australia East"
resource_group_name = "koalatech-week08-rg"

# Globally unique name for your Azure Container Registry
acr_name             = "berlweek08acr"

# Globally unique name for your Azure Storage Account
storage_account_name = "berlweek08storage"

# AKS cluster name and DNS prefix
aks_cluster_name = "berlweek08aks"
aks_dns_prefix   = "berlweek08"

# Week08 requires 3 nodes: staging + production both run persistent Postgres workloads
aks_node_count   = 3
aks_node_vm_size = "Standard_D2s_v3"

environment = "development"

tags = {
    Project     = "KoalaTech Course Platform"
    ManagedBy   = "Terraform"
    Practical   = "Week08"
    Environment = "Development"
}
