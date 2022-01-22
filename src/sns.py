import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY_ID')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')
TOPIC_ARN = '' # add TopicArn here

client = boto3.client(
    'sns',
    AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN=AWS_SESSION_TOKEN,
    region_name='us-east-1'
)

def send_message(message):
    response = client.publish(
        TopicArn=TOPIC_ARN,
        Message=message
    )
    return response

if __name__ == '__main__':
    pass