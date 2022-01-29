import cv2
import boto3
from time import sleep, time
from requests import post
from base64 import b64encode

# Start camera
cam = cv2.VideoCapture(0)
# Set this to the relevant camera ID
CAMERA_ID = '5ce12d'

# URL of the web server
WEB_SERVER = 'http://127.0.0.1:5000'

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
            ProjectVersionArn='arn:aws:rekognition:us-east-1:126728685550:project/Garbage-Detect-v1/version/Garbage-Detect-v1.2022-01-28T11.33.27/1643340807701',
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

        # Capture images in one-minute intervals
        sleep(60)
finally:
    cam.release()
