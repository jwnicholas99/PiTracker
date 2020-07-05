import RPi.GPIO as GPIO
from time import sleep

in1 = 11
in2 = 13
in3 = 16
in4 = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)


def motors_low():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def forward(period):
    motors_low()
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)
    sleep(period)
    motors_low()
    
def backward(period):
    motors_low()
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    sleep(period)
    motors_low()

motors_low()
backward(1)
GPIO.cleanup()
