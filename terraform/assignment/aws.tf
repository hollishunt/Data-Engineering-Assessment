# You will need to modify the key value in the backend block to a unique value for your assignment.

data "aws_caller_identity" "current" {}


provider "aws" {
  region = var.region_name
  profile = var.aws_profile
}


terraform {
  backend "s3" {
  bucket         = "nmd-training-tf-states-<REPLACE-WITH-ACCOUNTID>"
  # update the key value to a unique value for your assignment
  # key            = "assignment/update-the-name-here-nmd-assignment.tfstate"
  region         = "us-west-2"
  dynamodb_table = "nmd-training-tf-state-lock-table"
  encrypt        = true # Encrypts the state file at rest
  }
}
