import cv2  # imports
from time import sleep
import os
import requests
from datetime import date, datetime
import boto3


cam = cv2.VideoCapture(0) # start camera
today = date.today()

img_counter = 0
camera_id = 1  # IMPORTANT: SET ID TO RELEVENT CAMERA
s3 = boto3.resource('s3')
client = boto3.client('rekognition',region_name='us-east-1')

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    sleep(600)

    timenow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    img_name = f"{timenow.year}/{timenow.month}/{timenow.day}_{timenow.hour}:{timenow.minute}.png"
    cv2.imwrite(img_name, frame)
    s3.Bucket(f'images-1553').upload_file(img_name, f'{camera_id}/{img_name}')
    os.system(f'rm {img_name}')

    response = client.detect_custom_labels(  # Custom Label Detection
    ProjectVersionArn='arn:aws:rekognition:us-east-1:338430903861:project/AWSAcceleratorProject/version/AWSAcceleratorProject.2021-12-18T13.23.11/1639804992696',
    Image={
        # 'Bytes': b'bytes',
        'S3Object': {
            'Bucket': f'images-1553/{camera_id}',
            'Name': 'img_name',
        }
    },
    MaxResults=123,
    # MinConfidence=... (Ammend if required)
    )
    plasticBags = len(response['CustomLabels'])

    url = f'https://ide-37415cdf43eb4b2aa570be45f9eb632e-8080.cs50.ws/{camera_id}'
    myobj = {'PlasticCount': f'{plasticBags}'}
    x = requests.post(url, data = myobj)

cam.release()