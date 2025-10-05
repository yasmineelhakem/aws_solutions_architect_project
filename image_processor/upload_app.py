import json
import boto3
import os
import time

def lambda_handler(event, context):
    s3 = boto3.client("s3", endpoint_url=os.environ.get("AWS_ENDPOINT_URL"))
    bucket_name = os.environ.get("UPLOAD_BUCKET", "original-bucket") # reads s3 bucket name set in the env var from the template
    file_name = f"user-upload-{int(time.time())}.png"  # creates unique file name

    # Generate presigned URL (valid for 5 min) to let someone directly upload to s3 bucket
    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket_name,
                 'Key': file_name, 
                 'ContentType': 'image/png'
        },
        ExpiresIn=300
    )

    presigned_url = presigned_url.replace("host.docker.internal", "localhost")

    dynamodb = boto3.resource("dynamodb", endpoint_url=os.environ.get("AWS_ENDPOINT_URL"))
    table_name = os.environ.get("METADATA_TABLE", "image-metadata")
    table = dynamodb.Table(table_name)

    timestamp = int(time.time())
    table.put_item(
    Item={
        "imageId": file_name,
        "uploadTimestamp": timestamp,
        "status": "PENDING",
    }
    )

    return {
        # this is sent to the api gateway => client
        "statusCode": 200,
        "body": json.dumps({
            "upload_url": presigned_url,
            "file_key": file_name
        })
    }
