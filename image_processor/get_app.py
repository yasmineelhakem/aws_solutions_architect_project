import json, boto3, os

def lambda_handler(event, context):
    s3 = boto3.client("s3", endpoint_url=os.environ.get("AWS_ENDPOINT_URL"))
    bucket = os.environ["PROCESSED_BUCKET"]
    key = event["pathParameters"]["key"] # reads the key from api path

    # generates presigned url for the user to download the image
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=300
    )

    url = url.replace("host.docker.internal", "localhost")
    
    return {
        # Returns the JSON response to API Gateway which sends it to the client
        "statusCode": 200,
        "body": json.dumps({"download_url": url})
    }
