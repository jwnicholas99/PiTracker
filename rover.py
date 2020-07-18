import RPi.GPIO as GPIO
import pigpio
from time import sleep
import sys

class Rover():
    def __init__(self, in1, in2, en1, in3, in4, en2, pan, tilt):
        self.in1 = in1
        self.in2 = in2
        self.en1 = en1
        self.in3 = in3
        self.in4 = in4
        self.en2 = en2
        self.pan = pan
        self.tilt = tilt

        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(en1, GPIO.OUT)
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)
        GPIO.setup(en2, GPIO.OUT)
        GPIO.setup(pan, GPIO.OUT)
        GPIO.setup(tilt, GPIO.OUT)
        self.motors_low()

        self.motor_right = GPIO.PWM(en1, 1000)
        self.motor_right.start(80)
        self.motor_left = GPIO.PWM(en2, 1000)
        self.motor_left.start(80)

        self.pi = pigpio.pi()
        self.pi.set_servo_pulsewidth(pan, 1500)
        self.pi.set_servo_pulsewidth(tilt, 1500)
        sleep(0.3)
    
    def motors_low(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def cleanup(self):
        self.pi.set_servo_pulsewidth(self.pan, 1500)
        self.pi.set_servo_pulsewidth(self.tilt, 1500)
        sleep(0.3)
        self.pi.set_servo_pulsewidth(self.pan, 0)
        self.pi.set_servo_pulsewidth(self.tilt, 0)
        self.pi.stop()
        GPIO.cleanup()

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
