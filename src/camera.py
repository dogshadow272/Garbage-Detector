import json
import cv2
from time import time, sleep #imports

def photo_capture():
    
    cam = cv2.VideoCapture(0)
    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        k = cv2.waitKey(1)
        if k%256 == 27:                         # quits program it escape key is pressed
            # ESC pressed
            print("Escape hit, closing...")
            break
        
        while True:
            sleep(60 - time() % 60)             
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter) #saves photo in the directory
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
    
    cam.release()
    
    cv2.destroyAllWindows()
        

photo_capture()