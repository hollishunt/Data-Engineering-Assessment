# IAM policy for Lambda to read from input S3 bucket
resource "aws_iam_policy" "lambda_s3_read_policy" {
  name = "${var.lambda_role_name}-s3-read-policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject"
        ]
        Resource = "${var.input_bucket_arn}/*"
      }
    ]
  })

  tags = var.default_tags
}

# IAM policy for Lambda to write to output S3 bucket
resource "aws_iam_policy" "lambda_s3_write_policy" {
  name = "${var.lambda_role_name}-s3-write-policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ]
        Resource = "${var.output_bucket_arn}/*"
      }
    ]
  })

  tags = var.default_tags
}

# Attach S3 read policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_s3_read_attachment" {
  role       = var.lambda_role_name
  policy_arn = aws_iam_policy.lambda_s3_read_policy.arn
}

# Attach S3 write policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_s3_write_attachment" {
  role       = var.lambda_role_name
  policy_arn = aws_iam_policy.lambda_s3_write_policy.arn
}