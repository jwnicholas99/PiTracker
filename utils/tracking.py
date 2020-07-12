from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from utils.pid import PID
from utils.obj_detector import ObjDetector
import signal
import time
import sys
import cv2

servoRange = (-90, 90)

def signal_handler(sig, frame):
    print("You pressed ctrl-c! Exiting...")

    # disable servos and clean things up

    sys.exit()

def obj_center(args, objX, objY, centerX, centerY):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    obj_detector = ObjDetector(model_dir="Sample_TFLite_model",
                               graph="detect.tflite",
                               labelmap="labelmap.txt",
                               threshold=0.5,
                               resolution="640x640",
                               obj_idxs=[0])

    obj_detector.start(objX, objY)

def pid_process(output, p, i, d, objCoord, centerCoord):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # create and init PID
    p = PID(p.value, i.value, d.value)
    p.initialize()

    while True:
        error = centerCoord.value - objCoord.value
        output.value = p.update(error)

def set_wheels(rover, period):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        # set wheels
        is_left = period.value > 0
        # Take note that if I'm to the left on the feed, it's to the rover's right
        if period.value == 0:
            continue
        elif is_left:
            rover.right()
        else:
            rover.left()
        time.sleep(abs(period.value))
        rover.motors_low()

def start_manager(rover):
    with Manager() as manager:
        centerX = manager.Value("i", 0)
        centerY = manager.Value("i", 0)

        objX = manager.Value("i", 0)
        objY = manager.Value("i", 0)

        # set PID values for wheels
        wheelP = manager.Value("f", 0.00025)
        wheelI = manager.Value("f", 0)
        wheelD = manager.Value("f", 0)

        # wheel value managed by independent PIDs
        wheel = manager.Value("i", 0)

        # There are 3 independent processes
        # 1. objectCenter - finds the object center
        # 2. wheel        - PID control loops for turning wheel
        # 3. set_wheels   - turns wheels according to PID control loops

        args = {
            "cascade": "haarcascade_frontalface_default.xml"
        }
        proc_objectCenter = Process(target=obj_center, args=(args,
                                                             objX,
                                                             objY,
                                                             centerX,
                                                             centerY))
        proc_wheel = Process(target=pid_process, args=(wheel,
                                                       wheelP,
                                                       wheelI,
                                                       wheelD,
                                                       objX,
                                                       centerX))
        proc_set_wheel = Process(target=set_wheels, args=(rover,
                                                          wheel))

        proc_objectCenter.start()
        proc_wheel.start()
        proc_set_wheel.start()

        proc_objectCenter.join()
        proc_wheel.join()
        proc_set_wheel.join()





