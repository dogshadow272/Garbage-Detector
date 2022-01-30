import boto3

client = boto3.client('sns', region_name='us-east-1')


def send_message(message):
    client.publish(
        TopicArn='arn:aws:sns:us-east-1:126728685550:garbage-detect',
        Message=message
    )
