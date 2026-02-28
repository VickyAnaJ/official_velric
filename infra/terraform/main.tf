terraform {
  required_version = ">= 1.6.0"
}

# Module skeletons for Step 3.0 baseline. Concrete provider wiring lands in active slices/foundation tasks.
module "network" {
  source = "./modules/network"
}

module "cicd" {
  source = "./modules/cicd"
}

module "security_roles" {
  source = "./modules/security_roles"
}
