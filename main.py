import os
import sys
import RPi.GPIO as GPIO
from time import sleep
from rover import Rover
from utils.keyboard import getch
from utils.stream import start_stream, end_stream
from utils.tracking import start_manager
from multiprocessing import Process
import psutil

# right motor
in1 = 13
in2 = 11
en1 = 15

# left motor
in3 = 16
in4 = 18
en2 = 22

# servos are using pigpio, which uses BCM numbering
# while the motors are using BOARD numbering
pan = 12
tilt = 13

GPIO.setmode(GPIO.BOARD)
rover = Rover(in1, in2, en1, in3, in4, en2, pan, tilt)

def kill_procs(pid):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()

#proc = start_stream("../mjpg-streamer/mjpg-streamer-experimental/")
pid = os.getpid()
proc_tracking = Process(target=start_manager, args=(rover,))
proc_tracking.start()

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
        kill_procs(pid)
        sys.exit()
        #end_stream(proc)

    sleep(0.1)
    rover.motors_low()
    key = ""
