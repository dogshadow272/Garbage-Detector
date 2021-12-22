import cv2
import boto3
from time import sleep, time
from requests import post
from base64 import b64encode

# Start camera
cam = cv2.VideoCapture(0)
# Set this to the relevant camera ID
CAMERA_ID = '743003'

# URL of the web server
WEB_SERVER = 'http://localhost:5000'

client = boto3.client('rekognition', region_name='us-east-1')


while True:
    # Take picture
    ret, frame = cam.read()
    timestamp = int(time())

    if not ret:
        print('Failed to grab frame')
        break

    img = cv2.imencode('.png', frame)[1].tobytes()

    # Custom label detection
    response = client.detect_custom_labels(
        ProjectVersionArn='arn:aws:rekognition:us-east-1:338430903861:project/AWSAcceleratorProject/version/AWSAcceleratorProject.2021-12-18T13.23.11/1639804992696',
        Image={
            'Bytes': img,
        },
        # MinConfidence=70
    )

    output = {
        'image': f'data:image/png;base64,{b64encode(img)}',
        'timestamp': timestamp,
        'litterItems': []
    }

    # Transform Rekognition's response to fit the schema defined in app.py
    for item in response['CustomLabels']:
        bb = item['Geometry']['BoundingBox']

        output['litterItems'].append({
            'confidence': item['Confidence'],
            'width': bb['Width'],
            'height': bb['Height'],
            'left': bb['Left'],
            'top': bb['Top']
        })

    # Send results to webserver
    post(f'{WEB_SERVER}/b/{CAMERA_ID}', json=output)

    # Capture images in one-minute intervals
    sleep(600)

cam.release()
