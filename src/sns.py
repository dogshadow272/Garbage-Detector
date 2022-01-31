import boto3
from config import SNS_ARN

client = boto3.client('sns', region_name='us-east-1')


def send_message(message):
    client.publish(
        TopicArn=SNS_ARN,
        Message=message
    )
