import json
import os
import pandas as pd
import boto3
from urllib.parse import unquote_plus
from datetime import datetime

import orders_analytics

def get_s3_path_from_event(event: dict) -> tuple:
    """Returns the bucket and key from the lambda event record"""
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = unquote_plus(record['s3']['object']['key'])
    return bucket, key

def lambda_handler(event, context):
    """Lambda function to process S3 events and perform analytics on orders data"""
    
    s3_client = boto3.client('s3')
    
    # Get S3 details from event
    input_bucket, input_key = get_s3_path_from_event(event)
    output_bucket = os.environ['OUTPUT_BUCKET']
    
    try:
        # Read CSV from S3
        response = s3_client.get_object(Bucket=input_bucket, Key=input_key)
        df = pd.read_csv(response['Body'])
        
        # Generate analytics
        analytics = orders_analytics.generate_analytics(df)
        
        # Upload results to output bucket with partitioning by date
        timestamp = datetime.now().strftime('%Y/%m/%d')
        
        for report_name, report_df in analytics.items():
            output_key = f"analytics/{timestamp}/{report_name}.csv"
            csv_buffer = report_df.to_csv(index=False)
            
            s3_client.put_object(
                Bucket=output_bucket,
                Key=output_key,
                Body=csv_buffer,
                ContentType='text/csv'
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed {input_key} and generated analytics reports')
        }
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing file: {str(e)}')
        }

