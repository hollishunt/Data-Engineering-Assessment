
# Variables
variable "repo_name" {
  type = string
  description = "Name of the repo"
}

variable "default_tags" {
  type = map(string)
  description = "Default tags to apply to all resources"
}