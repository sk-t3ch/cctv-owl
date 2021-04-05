from threading import Thread
import threading
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import datetime as dt
import imutils
import os
import argparse
import sys
import time
from threading import Thread
import importlib.util
from PIL import Image
from io import BytesIO


WIDTH = 300
HEIGHT = 300

modeldir = "Sample_TFLite_model"
graph = 'detect.tflite'
labels = 'labelmap.txt'
threshold = 0.5
resolution = '1280x720'
edgetpu = 'store_true'

MODEL_NAME = modeldir
GRAPH_NAME = graph
LABELMAP_NAME = labels
min_conf_threshold = float(threshold)
resW, resH = resolution.split('x')
imW, imH = int(resW), int(resH)
use_TPU = edgetpu

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# First label is '???', which has to be removed.
if labels[0] == '???':
    del (labels[0])

if use_TPU:
    interpreter = Interpreter(
        model_path=PATH_TO_CKPT,
        experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

class BroadcastThread(Thread):
    def __init__(self, camera, output, websocket_server):
        super(BroadcastThread, self).__init__()
        self.camera = camera
        self.output = output
        self.websocket_server = websocket_server

    def run(self):
        try:
            self.camera.start_recording(self.output, 'h264', profile="baseline")
            while True:
                with self.output.condition:
                    self.output.condition.wait()
                    frame = self.output.frame
                    print("FRAME: ", frame)
                    cv2.CV_LOAD_IMAGE_COLOR = 1  # set flag to 1 to give colour image
                    npframe = np.fromstring(frame, dtype=np.uint8)
                    pil_frame = cv2.imdecode(npframe, cv2.CV_LOAD_IMAGE_COLOR)
                    #pil_frame = cv2.imdecode(frame,-1)
                    frame_rgb = cv2.cvtColor(pil_frame, cv2.COLOR_BGR2RGB)
                    frame_resized = cv2.resize(frame_rgb, (width, height))
                    input_data = np.expand_dims(frame_resized, axis=0)

                    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
                    if floating_model:
                        input_data = (np.float32(input_data) - input_mean) / input_std

                    # Perform the actual detection by running the model with the image as input
                    interpreter.set_tensor(input_details[0]['index'], input_data)
                    interpreter.invoke()

                    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
                    classes = interpreter.get_tensor(output_details[1]['index'])[0]
                    scores = interpreter.get_tensor(output_details[2]['index'])[0]
                    for i in range(len(scores)):
                        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                            ymin = int(max(1, (boxes[i][0] * imH)))
                            xmin = int(max(1, (boxes[i][1] * imW)))
                            ymax = int(min(imH, (boxes[i][2] * imH)))
                            xmax = int(min(imW, (boxes[i][3] * imW)))

                            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax),
                                        (10, 255, 0), 2)

                            object_name = labels[int(classes[i])]
                            label = '%s: %d%%' % (object_name, int(scores[i] * 100)
                                                )  # Example: 'person: 72%'
                            labelSize, baseLine = cv2.getTextSize(label,
                                                                cv2.FONT_HERSHEY_SIMPLEX,
                                                                0.7, 2)
                            label_ymin = max(ymin, labelSize[1] + 10)
                            cv2.rectangle(
                                frame, (xmin, label_ymin - labelSize[1] - 10),
                                (xmin + labelSize[0], label_ymin + baseLine - 10),
                                (255, 255, 255), cv2.FILLED)
                            cv2.putText(frame, label, (xmin, label_ymin - 7),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                    self.websocket_server.manager.broadcast(self.output.frame, binary=True)
                    
        except:
            raise Exception