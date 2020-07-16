from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from utils.pid import PID
from utils.obj_detector import ObjDetector
import signal
import time
import sys
import cv2
import pigpio

# pulse width range for SG90 servos
servoRange = (500, 2500)

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
                               threshold=0.45,
                               resolution="640x640",
                               obj_idxs=[0])
    centerX.value = obj_detector.img_width // 2
    centerY.value = obj_detector.img_height // 2
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

def in_range(val, start, end):
    return val >= start and val <= end

def set_servos(rover, pan_delta, tilt_delta):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    time.sleep(3)
    while True:
        pan_change = pan_delta.value * -1
        pan_pulse_width = rover.pi.get_servo_pulsewidth(rover.pan) + pan_change 
        if in_range(pan_pulse_width, servoRange[0], servoRange[1]):
            print(pan_change)
            rover.pi.set_servo_pulsewidth(rover.pan, pan_pulse_width)

        tilt_change = tilt_delta.value * -1
        tilt_pulse_width = rover.pi.get_servo_pulsewidth(rover.tilt) + tilt_change
        if in_range(tilt_pulse_width, servoRange[0], servoRange[1]):
            rover.pi.set_servo_pulsewidth(rover.tilt, tilt_pulse_width)
        time.sleep(0.06)

def start_manager(rover):
    with Manager() as manager:
        centerX = manager.Value("i", 0)
        centerY = manager.Value("i", 0)

        objX = manager.Value("i", 0)
        objY = manager.Value("i", 0)

        # set PID values for pan
        panP = manager.Value("f", 0.1)
        panI = manager.Value("f", 0.027)
        panD = manager.Value("f", 0.03)

        # set PID values for tilt
        tiltP = manager.Value("f", 0)
        tiltI = manager.Value("f", 0)
        tiltD = manager.Value("f", 0)

        # wheel value managed by independent PIDs
        pan_delta = manager.Value("f", 0.0)
        tilt_delta = manager.Value("f", 0.0)

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
        proc_pan = Process(target=pid_process, args=(pan_delta,
                                                       panP,
                                                       panI,
                                                       panD,
                                                       objX,
                                                       centerX))
        proc_tilt = Process(target=pid_process, args=(tilt_delta,
                                                       tiltP,
                                                       tiltI,
                                                       tiltD,
                                                       objY,
                                                       centerY))
        proc_set_servos = Process(target=set_servos, args=(rover,
                                                           pan_delta,
                                                           tilt_delta))
        proc_objectCenter.start()
        proc_pan.start()
        #proc_tilt.start()
        proc_set_servos.start()

        proc_objectCenter.join()
        proc_pan.join()
        #proc_tilt.join()
        proc_set_servos.join()

