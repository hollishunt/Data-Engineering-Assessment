resource "aws_s3_bucket" "input_s3" {
  bucket = "${var.app_name}-input-bucket"
  tags = merge({
        Name        = "${var.app_name}-input-bucket"
        Environment = var.env
    }, var.default_tags
  )
  force_destroy = true
}

resource "aws_s3_bucket" "output_s3" {
  bucket = "${var.app_name}-output-bucket"
  tags = merge({
        Name        = "${var.app_name}-output-bucket"
        Environment = var.env
    }, var.default_tags
  )
  force_destroy = true
}

resource "aws_s3_bucket_notification" "s3_notification" {
  bucket = aws_s3_bucket.input_s3.id
  lambda_function {
    lambda_function_arn = var.lambda_arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "*"
    filter_suffix       = ".csv"
  }
}