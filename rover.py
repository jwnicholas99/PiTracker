import RPi.GPIO as GPIO
from time import sleep

class Rover():
    def __init__(self, in1, in2, en1, in3, in4, en2):
        self.in1 = in1
        self.in2 = in2
        self.en1 = en1
        self.in3 = in3
        self.in4 = in4
        self.en2 = en2

        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(en1, GPIO.OUT)
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)
        GPIO.setup(en2, GPIO.OUT)
        self.motors_low()

        self.motor_right = GPIO.PWM(en1, 1000)
        self.motor_right.start(75)
        self.motor_left = GPIO.PWM(en2, 1000)
        self.motor_left.start(75)
    
    def motors_low(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
        exit()

    def forward(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
        
    def backward(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)

    def left(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)

    def right(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)
