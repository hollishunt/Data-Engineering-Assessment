## Terraform Code calling each module to deploy the S3 --> Lambda --> S3 Pipeline

module "s3_buckets" {
  source = "../modules/s3"
  app_name = local.app_name
  env = var.env
  lambda_arn = module.lambda_function.lambda_arn
  lambda_permission_id = module.lambda_function.lambda_permission_id
  default_tags = local.default_tags
}

module "lambda_function" {
  source                  = "../modules/lambda"
  lambda_name             = "${local.app_name}-file-processor"
  role_name               = "${local.app_name}-file-processor-role" 
  log_retention_in_days   = 14
  image_uri               = "${module.ecr_repo.repository_url}:latest"
  timeout                 = 15
  memory_size             = 256
  environment_variables   = {
    INPUT_BUCKET = module.s3_buckets.input_bucket_name
    OUTPUT_BUCKET = module.s3_buckets.output_bucket_name
  }
  input_bucket_arn = module.s3_buckets.input_bucket_arn

  default_tags = local.default_tags
}

module "ecr_repo" {
  source    = "../modules/ecr-repo"
  repo_name = "${local.app_name}-ecr"
  default_tags = local.default_tags
}

module "iam_policies" {
  source = "../modules/iam"
  lambda_role_name = module.lambda_function.lambda_exec_role_name
  input_bucket_arn = module.s3_buckets.input_bucket_arn
  output_bucket_arn = module.s3_buckets.output_bucket_arn
  default_tags = local.default_tags
}


