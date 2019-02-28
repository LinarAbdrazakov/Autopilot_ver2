import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)


class Motor(object):

    def __init__(self):
        self.SpeedPin = 12
        self.ForwardPin = 6
        self.AgoPin = 5
        GPIO.setup(self.SpeedPin, GPIO.OUT)
        GPIO.setup(self.ForwardPin, GPIO.OUT)
        GPIO.setup(self.AgoPin, GPIO.OUT)
        self.Speed = GPIO.PWM(self.SpeedPin, 500)
        self.Speed.start(0)

    def go(self, speed):
        forward = False
        if speed > 0:
            forward = True 
        GPIO.output(self.ForwardPin, forward)        
        GPIO.output(self.AgoPin, not forward)
        self.Speed.ChangeDutyCycle(abs(speed))

    def clean(self):
        self.Speed.ChangeDutyCycle(0)
        self.Speed.stop()

        
class Helm(object):

    def __init__(self):
        self.RightPin = 11 
        self.LeftPin = 9
        GPIO.setup(self.RightPin, GPIO.OUT)
        GPIO.setup(self.LeftPin, GPIO.OUT)

    def forward(self):
        GPIO.output(self.RightPin, 0)
        GPIO.output(self.LeftPin, 0)

    def right(self):
        GPIO.output(self.RightPin, 1)
        GPIO.output(self.LeftPin, 0)
    
    def left(self):
        GPIO.output(self.RightPin, 0)
        GPIO.output(self.LeftPin, 1)


# for test
if __name__ == '__main__':
    try:
        """motor = Motor()
        while True:
            for i in range(-100, 101):
                motor.go(i)
                time.sleep(0.025)
            for i in range(100, -101, -1):
                motor.go(i)
                time.sleep(0.025)"""
        helm = Helm()
        while True:
            helm.right()
            print('right')
            time.sleep(5)
            helm.left()
            print('left')
            time.sleep(5)

    finally:
        motor.clean()
        GPIO.cleanup()

