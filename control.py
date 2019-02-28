import time
from subprocess import Popen, PIPE
 
import lights
from motor import Motor
from Arduino import Arduino


arduino = Arduino()
motor = Motor()         


def get_distance(distance, file_distance='distance.txt'):
    with open(file_distance) as file:
        line = file.readline()
        if len(line) > 0:
            distance = float(line)
    return distance


def servo(angle=90):
    angle = int(angle)
    arduino.servo_write(angle)    
    

def accumulate():    
    voltage = arduino.get_acc()
    return voltage


def get_angle(angle, file_angle='angle.txt'):
    with open(file_angle) as file:
        line = file.readline()
        if len(line) > 0:
            angle = int(line)
    return angle

        
try:
    lights.forward(1)
    distance = 0
    angle = 90
    past_angle = 90
    tek = True
    while True:
        distance = get_distance(distance)
        angle = get_angle(angle)
        if(angle != past_angle):
            servo(angle)
            past_angle = angle
        if distance > 40 and tek:
             motor.go(50)
             lights.ago(0)
             tek = False
        elif distance < 40 and not tek:
             motor.go(-40)
             lights.ago(1)
             time.sleep(1)
             motor.go(0)
             tek = True

finally:
     motor.clean()
     lights.forward(0)
     lights.ago(0)
     lights.clean()
