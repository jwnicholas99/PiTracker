# Raspberry Pi Rover (rpi-rover)
This Github repository contains the code used to:
1. Drive a rover using a Raspberry Pi
2. Detect objects using Tensorflow Lite (tflite)
3. Track a specified object class (eg. person or bird) using a pan-tilt camera with Proportional Integral Derivative (PID) process control

This project came into being simply because my dog is obsessed with biting her feet. As she's smart enough to hide while committing this heinuous crime, I wanted to build a rover that could track her.

Credits to:
* [EdjeElectronic's repo on using Tensorflow Lite for object detection](https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi) - I modified his `TFLite_detection_webcam.py` to fit into the rpi-rover code
* [Adrian Rosebrock's guide on pan-tilt face tracking](https://www.pyimagesearch.com/2019/04/01/pan-tilt-face-tracking-with-a-raspberry-pi-and-opencv/) - his code formed the base for using PID processes for controlling the pan-tilt camera

## Required Hardware
* Raspberry Pi 4B (at least 2GB recommended)
* [Robot Car Chassis](https://sg.cytron.io/p-2wd-smart-robot-car-chassis?src=us.special.c)
  * TT Motor + Wheel  X 2
  * 4xAA battery holder
  * Acrylic board to hold everything together
* [L298N Motor Driver](https://sg.cytron.io/p-2amp-7v-30v-l298n-motor-driver-stepper-driver-2-channels?src=us.special) (Used to control the motors)
* [5MP Camera for Raspberry Pi](https://sg.cytron.io/p-5mp-camera-board-for-raspberry-pi?search=camera&description=1&src=search.list)
* [FFC Cable longer than 20cm](https://sg.cytron.io/p-raspberry-pi-15-pin-camera-ffc-cable-50cm?search=FFC%20cable&description=1&src=search.list) (as you will need to move your camera around)
* [SG90 Micro Servo](https://sg.cytron.io/p-sg90-micro-servo?search=servo&description=1&src=search.list) X 2 (to pan/tilt camera)

## How to setup and run

Summary of steps:
1. Enable camera on the Raspberry Pi
2. Clone Github repository
3. Create a new virtual environment and install necessary packages
4. Run `python main.py`

### 1. Enable camera on the Raspberry Pi
In the terminal of your rpi, issue:
```
$ sudo raspi-config
```
Go -> Interfacing Options -> P1 Camera -> Yes 

### 2. Clone this Github repository
```
$ git clone https://github.com/jwnicholas99/rpi_rover.git
$ cd rpi_rover/
```

### 3. Create a new venv and install packages

First, create and activate a new virtual environment by issuing:
```
$ python3 -m venv rpi-rover
$ source rpi-rover/bin/activate
```

Second, install required packages for OpenCV
```
$ sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
$ sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
$ sudo apt-get -y install libxvidcore-dev libx264-dev
$ sudo apt-get -y install qt4-dev-tools libatlas-base-dev
$ pip3 install opencv-python==3.4.6.27
```

Third, install Tensorflow Lite. If your Python is version 3.5:
```
$ pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp35-cp35m-linux_armv7l.whl
```

If version 3.7:
```
$ pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
```

Fourth, install other python packages:
```
$ pip3 install -r requirements.txt
```

### 4. Run main.py
You can start the main program using:
```
$ python3 main.py
``` 
This should produce a view from your rpi camera with bounding boxes of objects.