import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

forward_pin = 23
ago_pin = 24

GPIO.setup(forward_pin, GPIO.OUT)
GPIO.setup(ago_pin, GPIO.OUT)


def forward(val=0):
    GPIO.output(forward_pin, val)


def ago(val=0):
    GPIO.output(ago_pin, val)

def clean():
    GPIO.cleanup()
