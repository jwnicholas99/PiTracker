import RPi.GPIO as GPIO
from time import sleep
from rover import Rover

in1 = 11
in2 = 13
in3 = 16
in4 = 18

GPIO.setmode(GPIO.BOARD)
rover = Rover(in1, in2, in3, in4)
rover.backward(0.5)
rover.forward(0.5)
rover.left(0.5)
rover.right(0.5)
rover.cleanup()
