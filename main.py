import io
import socket
import struct
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2

import NeuralNetwork


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
print "[INFO] camera connect"


start = time.time()
number = 0

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # get image from camera
        image = frame.array
        # predict angle
        angle = NeuralNetwork.predict_angle(image)
        print 'Angle:', angle
        with open("angle.txt", 'w') as file:
            file.write(str(angle))
        
        # FPS
        number += 1
        if (time.time() - start) > 5:
            print "FPS: ", number/(time.time() - start)
            number = 0
            start = time.time()
        rawCapture.truncate(0)

finally:
    pass
