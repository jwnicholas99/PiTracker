import RPi.GPIO as GPIO
from time import sleep

class Rover():
    def __init__(self, in1, in2, in3, in4):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4

        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)
    
    def motors_low(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()

    def forward(self, period):
        self.motors_low()
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.HIGH)
        sleep(period)
        self.motors_low()
        
    def backward(self, period):
        self.motors_low()
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        sleep(period)
        self.motors_low()

    def left(self, period):
        self.motors_low()
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        sleep(period)
        self.motors_low()

    def right(self, period):
        self.motors_low()
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.HIGH)
        sleep(period)
        self.motors_low()
