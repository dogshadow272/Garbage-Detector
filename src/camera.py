import json
import cv2
from time import time, sleep


def photo_capture():
    cam = cv2.VideoCapture(0)
    img_counter = 0

    while True:
        ret, frame = cam.read()

        if not ret:
            print('failed to grab frame')
            break

        # Save photo in the directory
        img_path = f'opencv_frame_{img_counter}.png'
        cv2.imwrite(img_path, frame)
        print(f'{img_path} written!')
        img_counter += 1

        # Take a picture every minute, ignoring the
        # time it takes to execute the rest of the code
        sleep(60 - time() % 60)

    cam.release()
    cv2.destroyAllWindows()


photo_capture()
