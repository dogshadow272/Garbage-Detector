import cv2
from tempfile import TemporaryFile
from numpy import save
from time import sleep, time
from requests import post
import boto3


# Start camera
cam = cv2.VideoCapture(0)
# Set this to the relevant camera ID
CAMERA_ID = '123456'

# URL of the web server
WEB_SERVER = 'http://localhost:5000'

s3 = boto3.resource('s3')
BUCKET_NAME = 'images-1553'
client = boto3.client('rekognition', region_name='us-east-1')


while True:
    # Take picture
    ret, frame = cam.read()

    if not ret:
        print('Failed to grab frame')
        break

    timestamp = int(time())
    img_name = f'{CAMERA_ID}/{timestamp}.png'

    # This is needed because s3.Bucket.upload_fileobj
    # requires a Fileobj that implements read
    img_obj = TemporaryFile()
    save(img_obj, cv2.imencode('.png', frame)[1])

    # Upload the image to S3
    s3.Bucket(BUCKET_NAME).upload_fileobj(img_obj, img_name)

    # Custom label detection
    response = client.detect_custom_labels(
        ProjectVersionArn='arn:aws:rekognition:us-east-1:338430903861:project/AWSAcceleratorProject/version/AWSAcceleratorProject.2021-12-18T13.23.11/1639804992696',
        Image={
            'S3Object': {
                'Bucket': BUCKET_NAME,
                'Name': img_name,
            }
        },
        # MinConfidence=70
    )

    output = {
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
