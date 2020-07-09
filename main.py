import RPi.GPIO as GPIO
from time import sleep
from rover import Rover
from utils.keyboard import getch
from utils.stream import start_stream, end_stream

# right motor
in1 = 13
in2 = 11
en1 = 15

# left motor
in3 = 16
in4 = 18
en2 = 22

GPIO.setmode(GPIO.BOARD)
rover = Rover(in1, in2, en1, in3, in4, en2)

proc = start_stream("../mjpg-streamer/mjpg-streamer-experimental/")
while True:
    key = getch()
    if key == "w":
        rover.forward()
    if key == "s":
        rover.backward()
    if key == "a":
        rover.left()
    if key == "d":
        rover.right()
    if key == "e":
        rover.cleanup()
        end_stream(proc)

    sleep(0.1)
    rover.motors_low()
    key = ""
