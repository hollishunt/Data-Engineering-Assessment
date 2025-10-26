output "input_bucket_name" {
  value = aws_s3_bucket.input_s3.bucket
}

output "output_bucket_name" {
  value = aws_s3_bucket.output_s3.bucket
}

output "input_bucket_arn" {
  value = aws_s3_bucket.input_s3.arn
}

output "output_bucket_arn" {
  value = aws_s3_bucket.output_s3.arn
}

output "input_bucket_id" {
  value = aws_s3_bucket.input_s3.id
}