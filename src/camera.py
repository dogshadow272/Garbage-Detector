import cv2
from time import sleep
import requests
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0
camera_number = 1


while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    sleep(6)
    img_name = f"{camera_number}.png"
    cv2.imwrite(img_name, frame)
    # img_counter += 1

cam.release()

cv2.destroyAllWindows()


data = {"img_name": f"{camera_number}.png"}
url = f"https://ide-37415cdf43eb4b2aa570be45f9eb632e-8080.cs50.ws/{camera_number}"
response = requests.post(url, data)
print(response)