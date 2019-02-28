import time
import RPi.GPIO as GPIO


class HC_SR04(object):

    def __init__(self):
        self.TRIG = 3
        self.ECHO = 2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)        

        
    def get_dist(self):
        start = time.time()
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)
        while GPIO.input(self.ECHO) == False:
            pass
        start = time.time()
        while GPIO.input(self.ECHO) == True:
            pass
        stop = time.time()
        distance = round((stop - start) * 17000, 2)    

        return distance



if __name__ == "__main__":
    Rangefinder = HC_SR04()
    file_name = 'distance.txt'
    while True:
        time.sleep(0.05)
        distance = Rangefinder.get_dist()
        print(distance)
        with open(file_name, 'w') as file:
            file.write(str(distance))

