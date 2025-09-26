import json
import boto3
# import requests

s3 = boto3.client('s3')

def lambda_handler(event, context):

    record = event['Records'][0] # Get the 1st record
    bucket = record['s3']['bucket']['name'] # Get bucket name
    key = record['s3']['object']['key'] # get the file name of the image

    # the file should be an image
    if not key.lower().endswith(('.jpg', '.jpeg', '.png')):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Not an image file'})
        }

    # Download the image from the S3 bucket
    response = s3.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'S3 event received and image downloaded ',
            'bucket': bucket,
            'key': key,
            'size': len(image_data)

        }),
    }
