# Variables
variable "lambda_name" {
  description = "Name of the lambda function"
  type        = string
}

variable "role_name" {
  description = "Name of the role"
  type        = string
}

variable "log_retention_in_days" { 
  default = 14 
  description = "Log retention in days"
}

variable "image_uri" {}

variable "timeout" { 
  default = 15
}

variable "memory_size" { 
  default = 256 
}

variable "environment_variables" { 
    type = map(string) 
    default = {} 
}

variable "default_tags" {
  type = map(string)
  description = "Default tags to apply to all resources"
}

variable "input_bucket_arn" {
  description = "ARN of the input S3 bucket for Lambda permission"
  type        = string
}