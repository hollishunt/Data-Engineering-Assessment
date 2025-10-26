# Outputs
output "lambda_arn" {
  value = aws_lambda_function.lambda_function.arn
}

output "lambda_exec_role_name" {
  value = aws_iam_role.lambda_exec_role.name
}
