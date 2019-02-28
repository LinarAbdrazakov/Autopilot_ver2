import serial

class Arduino(object):

    def __init__(self):
        self.port = serial.Serial('/dev/ttyUSB0', 115200)
        self.angle = 90
        self.voltage = None

    def write(self, data):
        self.port.write(data.encode('utf-8'))

    def read(self):
        data = self.port.readline().decode('utf-8')
        return data

    def servo_write(self, angle=90):
        self.angle = angle
        self.write('S'+'0'*(3-len(str(self.angle)))+str(self.angle))

    def get_acc(self):
        text = self.read()
        data = text.split('\n')[-1]
        self.voltage = float(data)
        return self.voltage
