import cv2
import boto3
from time import sleep, time
from requests import post
from base64 import b64encode
from config import REKOGNITION_ARN, WEB_SERVER, CAMERA_INTERVAL

# Start camera
cam = cv2.VideoCapture(0)
# Set this to the relevant camera ID
CAMERA_ID = '5ce12d'

client = boto3.client('rekognition', region_name='us-east-1')

try:
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
            ProjectVersionArn=REKOGNITION_ARN,
            Image={
                'Bytes': img,
            },
            # MinConfidence=70
        )

        output = {
            'image': f'data:image/png;base64,{str(b64encode(img))[2:-1]}',
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

        # Wait for some time between image captures
        sleep(CAMERA_INTERVAL)
finally:
    cam.release()
