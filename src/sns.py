import boto3

client = boto3.client('sns', region_name='us-east-1')


def send_message(message):
    client.publish(
        TopicArn='add topic arn here',
        Message=message
    )
