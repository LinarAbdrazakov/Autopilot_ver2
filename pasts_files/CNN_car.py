from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import time
from keras.models import Sequential
from keras.layers import Dense, Flatten, Activation
from keras.layers import Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
from reciver import Reciver
from motor import Motor
from Arduino import Arduino


camera = PiCamera()
camera.resolution = (64, 48)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(64, 48))
time.sleep(0.1)
print "Camera connect"
 
print "[INFO] loading model..."
model = Sequential()
model.add(Convolution2D(32, (3, 3), padding='same', input_shape=(32, 64, 3), activation='relu'))
model.add(Convolution2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 3, 3, border_mode='same', activation='relu'))
model.add(Convolution2D(64, 3, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(10, activation='relu'))
model.add(Dense(1))

model.load_weights("road_model_new.h5")
print "[INFO] ok."

model.compile(optimizer=Adam(0.0001), loss="mse")

#reciver = Reciver()
#reciver.read()
arduino = Arduino()
motor = Motor()

auto = False

number = 0
start = time.time()
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        tu = time.time()
        image = frame.array
        road = image[-32:,:].copy()
        #road = cv2.resize(road, (road.shape[1]//10, road.shape[0]//10), interpolation=cv2.INTER_AREA)
        print time.time() - tu, 1
        #road = cv2.cvtColor(road, cv2.COLOR_BGR2GRAY)
        #reciver.get_ch3()
        #reciver.get_ch6()
        #if not auto: reciver.get_ch4()
        impulses = [1500, 1500, 1500, 1500, 1500, 2000]#reciver.get_impulses()
     
        # Speed        
        speed = 50 # (impulses[2] - 1500)/5
        if speed > 100: speed = 100
        elif speed < -100: speed = -100
        # Autopilot
        if (impulses[5] > 1500) and (not auto):
            auto = True
            print "Autopilot started!"
        elif (impulses[5] < 1500) and auto:
            auto = False
            print "Autopilot stoped!"
        # Helm
        if auto:
            tu = time.time()
            road = np.array(road, "float").reshape(1, 32, 64, 3)
            #road.astype("float32")
            road /= 255
            pos = model.predict(road)[0][0]
            print time.time() - tu, 2 
        else:
            thresh = 60 
            pos = 90
            impulse = (impulses[3] - 1500)/5
            if impulse > thresh: pos = 90
            elif impulse < -thresh: pos = 90
        print pos

        # Control
        motor.go(speed)
        arduino.angle = int(pos)
        arduino.servo_write()
        # FPS
        number += 1
        if (time.time() - start) > 5: 
            print "FPS: ", number/(time.time() - start)
            number = 0
            start = time.time() 
        rawCapture.truncate(0)

finally:
    motor.clean()
    rawCapture.truncate(0)
