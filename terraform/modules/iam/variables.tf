variable "input_bucket_arn" {
  description = "ARN of the input S3 bucket"
  type        = string
}

variable "output_bucket_arn" {
  description = "ARN of the output S3 bucket"
  type        = string
}

variable "default_tags" {
  type        = map(string)
  description = "Default tags to apply to all resources"
}

variable "lambda_role_name" {
  description = "Name of the lambda role"
  type        = string
}