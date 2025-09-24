import json

# import requests


def lambda_handler(event, context):

    print("Template test successful!")
    print(f"Event received: {json.dumps(event, indent=2)}")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Template test passed!',
            'event_received': event
        }),
    }
