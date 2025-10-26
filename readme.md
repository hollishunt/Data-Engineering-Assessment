# Data Engineering Assessment - Order Analytics Pipeline

## Overview
This project implements a serverless data processing pipeline using AWS services to analyze order data and generate analytics reports.

## Architecture
- **Input S3 Bucket**: Stores incoming CSV order files
- **AWS Lambda**: Dockerized function that processes files and generates analytics
- **Output S3 Bucket**: Stores generated analytics reports
- **ECR**: Container registry for Lambda Docker image
- **IAM**: Least privilege policies for secure access

## Analytics Generated
1. **Most Profitable Region**: Calculates total profit by region
2. **Shipping Method by Category**: Most common shipping method for each product category
3. **Orders by Category/Sub-Category**: Count of orders grouped by category and sub-category

## Data Partitioning
Output files are partitioned by date using the pattern: `analytics/YYYY/MM/DD/report_name.csv`

## Deployment Instructions

### Prerequisites
- AWS CLI configured with appropriate credentials
- Docker installed
- Terraform installed

### Setup
1. Update `terraform/assignment/vars.tfvars` with your information:
   ```
   candidate_name="Your Name Here"
   aws_profile="your-aws-profile"
   ```

2. Initialize Terraform:
   ```bash
   cd terraform/assignment
   terraform init -backend-config="key=nmd-assignment-<candidate-name>.tfstate"
   ```

3. Deploy ECR repository first:
   ```bash
   terraform apply -target=module.ecr_repo -var-file="vars.tfvars"
   ```

4. Build and push Docker image:
   ```bash
   # Get ECR URI from Terraform output
   ECR_URI=$(terraform output -raw ecr_repository_url)
   LOCAL_IMAGE_NAME="order-processor"
   AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
   REGION="us-west-2"
   
   # Build and push
   docker build --platform linux/arm64 --no-cache -t "$LOCAL_IMAGE_NAME" ./app
   aws ecr get-login-password | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
   docker tag "$LOCAL_IMAGE_NAME" "$ECR_URI"
   docker push "$ECR_URI"
   ```

5. Deploy remaining infrastructure:
   ```bash
   terraform apply -var-file="vars.tfvars"
   ```

### Testing
Upload the sample file to test the pipeline:
```bash
aws s3 cp sample_orders.csv s3://<input-bucket-name>/
```

Check for generated reports:
```bash
aws s3 ls s3://<output-bucket-name>/analytics/ --recursive
```

## Security Features
- IAM policies follow least privilege principle
- Lambda can only read from input bucket and write to output bucket
- S3 buckets have force_destroy enabled for easy cleanup
- All resources are properly tagged

## File Structure
```
├── app/
│   ├── lambda.py              # Main Lambda handler
│   ├── orders_analytics.py    # Analytics logic
│   └── requirements.txt       # Python dependencies
├── terraform/
│   ├── assignment/            # Main Terraform configuration
│   └── modules/
│       ├── ecr-repo/         # ECR repository module
│       ├── lambda/           # Lambda function module
│       ├── s3/               # S3 buckets module
│       └── iam/              # IAM policies module
├── Dockerfile                # Lambda container definition
└── sample_orders.csv         # Test data
```