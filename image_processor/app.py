import json
import boto3
from PIL import Image
import io
import os 

endpoint = os.environ.get("S3_ENDPOINT_URL", None)

s3 = boto3.client(
    "s3",
    endpoint_url=endpoint,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_DEFAULT_REGION")
)


def lambda_handler(event, context):
    print("Environment variables hihi:")
    print(f"AWS_ACCESS_KEY_ID: {os.environ.get('AWS_ACCESS_KEY_ID', 'NOT SET')}")
    print(f"AWS_SECRET_ACCESS_KEY: {os.environ.get('AWS_SECRET_ACCESS_KEY', 'NOT SET')}")
    print(f"AWS_DEFAULT_REGION: {os.environ.get('AWS_DEFAULT_REGION', 'NOT SET')}")
    print(f"S3_ENDPOINT_URL: {os.environ.get('S3_ENDPOINT_URL', 'NOT SET')}")

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

    image = Image.open(io.BytesIO(image_data)) # Open image with Pillow
    image.thumbnail((800, 800)) # Resize image
    output_buffer = io.BytesIO()
    image.save(output_buffer, format=image.format) # Save resized image to bytes
    output_buffer.seek(0) # Reset buffer position

    # Upload the processed image to a different S3 bucket
    processed_bucket = "processed-bucket"  
    new_key = f"processed/{key}"
    
    s3.put_object(
        Bucket=processed_bucket,
        Key=new_key,
        Body=output_buffer,
        ContentType=f'image/{image.format.lower()}'
    )


    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'S3 event received and image downloaded ',
            'bucket': bucket,
            'key': key,
            'size': len(image_data),
            'image_format': image.format,
            'dimensions': f"{image.width}x{image.height}",
            'processed_size': len(output_buffer.getvalue()),
            'new_dimensions': f"{image.width}x{image.height}",
            'processed_bucket': processed_bucket,
            'processed_key': new_key

        }),
    }
