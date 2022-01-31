# URL of the web server hosting `app.py`
WEB_SERVER = 'http://127.0.0.1:5000'

# Amount of litter items to wait for before sending SMS notification
LITTER_NOTIFICATION_THRESHOLD = 3

# Seconds to wait between capturing pictures
CAMERA_INTERVAL = 60

# Seconds to wait before marking a camera as disconnected
TIME_TO_CAMERA_EXPIRY = 70

# ARN of Rekognition instance
REKOGNITION_ARN = 'arn:aws:rekognition:us-east-1:126728685550:project/Garbage-Detect-v1/version/Garbage-Detect-v1.2022-01-28T11.33.27/1643340807701'

# ARN of SNS topic
SNS_ARN = 'arn:aws:sns:us-east-1:126728685550:garbage-detect'
