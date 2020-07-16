import os
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util

class VideoStream:
    # Camera object that controls video streaming from Picamera
    def __init__(self, resolution=(640,480), framerate=30):
        # init PiCamera and image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])

        # Read first frame from the stream
        self.grabbed, self.frame = self.stream.read()

        # var for checking if camera is stopped
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                self.stream.release()
                return

            (self.grabbed, cur_frame) = self.stream.read()
            self.frame = cv2.flip(cur_frame, 0)

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

class ObjDetector:
    def __init__(self, model_dir, graph, labelmap, threshold, resolution, obj_idxs):
        self.model_dir = model_dir
        self.graph = graph
        self.labelmap = labelmap
        self.threshold = threshold
        resW, resH = resolution.split('x')
        self.img_width = int(resW)
        self.img_height = int(resH)
        self.obj_idxs = obj_idxs
        
        # import tensorflow libraries
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime.interpreter import Interpreter
        else:
            from tensorflow.lite.python.interpreter import Interpreter

        with open(os.path.join(model_dir, labelmap), 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        if self.labels[0] == '???':
            del(self.labels[0])
        
        # load tensorflow lite model
        self.interpreter = Interpreter(model_path=os.path.join(model_dir, graph))
        self.interpreter.allocate_tensors()

    def start(self, objX, objY):
        # get model details
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        model_height = input_details[0]['shape'][1]
        model_width = input_details[0]['shape'][2]

        floating_model = (input_details[0]['dtype'] == np.float32)

        input_mean = 127.5
        input_std = 127.5

        # init frame rate calculation
        frame_rate_calc = 1
        freq = cv2.getTickFrequency()
        
        # init vid stream
        vid_stream = VideoStream(resolution=(self.img_width, self.img_height)).start()
        time.sleep(1)

        while True:
            # start timer for calculating frame rate
            t1 = cv2.getTickCount()

            # grab frame from video stream
            frame1 = vid_stream.read()

            # modify frame to expected shape [1xHxWx3]
            frame = frame1.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (model_width, model_height))
            input_data = np.expand_dims(frame_resized, axis=0)

            # normalize pixel values if using a floating model (non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # perform detection
            self.interpreter.set_tensor(input_details[0]['index'], input_data)
            self.interpreter.invoke()

            # Retrieve detection results
            boxes = self.interpreter.get_tensor(output_details[0]['index'])[0]
            classes = self.interpreter.get_tensor(output_details[1]['index'])[0]
            scores = self.interpreter.get_tensor(output_details[2]['index'])[0]

            objX.value = int(self.img_width // 2)
            objY.value = int(self.img_height // 2)

            # loop over all detection and draw boxes if fulfill:
            #   1. Score is above minimum threshold
            #   2. Class is one of the specified obj_idx
            for i in range(len(scores)):
                if ((scores[i] > self.threshold) and (scores[i] <= 1.0) and classes[i] in self.obj_idxs):
                    ymin = int(max(1,(boxes[i][0] * self.img_height)))
                    xmin = int(max(1,(boxes[i][1] * self.img_width)))
                    ymax = int(min(self.img_height, (boxes[i][2] * self.img_height)))
                    xmax = int(min(self.img_width, (boxes[i][3] * self.img_width)))

                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

                    # draw label
                    obj_name = self.labels[int(classes[i])]
                    label = '%s: %d%%' % (obj_name, int(scores[i]*100))
                    label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    label_ymin = max(ymin, label_size[1] + 10)
                    cv2.rectangle(frame, (xmin, label_ymin-label_size[1]-10), (xmin+label_size[0], label_ymin+base_line-10), (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                    # update obj center coords
                    objX.value = int((xmin + xmax) / 2)
                    objY.value = int((ymin + ymax) / 2)

            cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Object detector', frame)

            # calculate framerate
            t2 = cv2.getTickCount()
            time1 = (t2-t1)/freq
            frame_rate_calc = 1/time1

            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()
        vid_stream.stop()














