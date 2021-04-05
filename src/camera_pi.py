# Taken From https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited 
import io
import time
import picamera
from base_camera import BaseCamera
import numpy as np
from PIL import Image
import cv2

import imutils
from multiprocessing import Process
from multiprocessing import Queue

from classify_frame import classify_frame
from make_sound import hoot
import requests

WIDTH=300
HEIGHT=300
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe('../assets/MobileNetSSD_deploy.prototxt.txt',
                               '../assets/MobileNetSSD_deploy.caffemodel')

inputQueue = Queue(maxsize=1)
outputQueue = Queue(maxsize=1)
detections = None

p = Process(target=classify_frame, args=(net, inputQueue,
	outputQueue,))
p.daemon = True
p.start()

def scale(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def find_new_position(pwm, startX, endX, budge_value):
    height, width = 300, 300
    half_width = width/2
    middle_of_feature = startX + ((endX-startX)/ 2)
    if (middle_of_feature > half_width): # if too far right
        pwm -= budge_value
    else:
        pwm += budge_value
    # lock bounds
    if pwm > 12.5:
        pwm = 12.5
    if pwm < 2.5:
        pwm = 2.5
    return pwm

class Camera(BaseCamera):
    firstFrame = None
    @staticmethod
    def frames():
        height, width = 300, 300
        pwm = 7.5 # ranges between 2.5 and 12.5
        firstFrame = None
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(1)
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                               use_video_port=True):
                stream.seek(0)
                img = stream.read()
                img = Image.open(stream)
                img = np.array(img)
                img = imutils.resize(img, width=WIDTH, height=HEIGHT)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                (fH, fW) = img.shape[:2]
                
                if inputQueue.empty():
                    inputQueue.put(img)

                detections = None
                if not outputQueue.empty():
                    detections = outputQueue.get()
                if detections is not None:
                    # process detections
                    for i in np.arange(0, detections.shape[2]):
                        confidence = detections[0, 0, i, 2]
                        if confidence < 0.1:
                            continue
                        idx = int(detections[0, 0, i, 1])
                        dims = np.array([fW, fH, fW, fH])
                        box = detections[0, 0, i, 3:7] * dims
                        (startX, startY, endX, endY) = box.astype("int")
                        label = f"{CLASSES[idx]}: {confidence * 100}"
                        print("LABEL :", label)
                        if CLASSES[idx] == "person":
                            hoot()
                            payload = {
                            "app_key": "APPKEY",
                            "app_secret": "APPSECRET",
                            "target_type": "app",
                            "content": "Zombie approaching!"
                            }
                            # r = requests.post("https://api.pushed.co/1/push", data=payload)
                            cv2.rectangle(img, (startX, startY), (endX, endY),
                                COLORS[idx], 2)
                            budge_value = 0.4
                            pwm = find_new_position(pwm, startX, endX, budge_value)
                            print("NEW PWM", pwm)

                yield cv2.imencode('.jpg', img)[1].tobytes(), pwm

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()




    
