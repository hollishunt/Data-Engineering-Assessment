variable "app_name" {
  description = "Application name for resource naming"
  type        = string
}

variable "env" {
  description = "Environment name"
  type        = string
}

variable "lambda_arn" {
  description = "Lambda function ARN for S3 notification"
  type        = string
}

variable "default_tags" {
  type        = map(string)
  description = "Default tags to apply to all resources"
}