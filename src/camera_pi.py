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


import requests

WIDTH=260
HEIGHT=240
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe('../assets/MobileNetSSD_deploy.prototxt.txt',
                               '../assets/MobileNetSSD_deploy.caffemodel')

def hoot():
  command = "omxplayer -o alsa:hw:1,0 ../aseets/owl_sound.mp3 --vol 200".split(' ')
  subprocess.Popen(command, 
                  stdin=subprocess.PIPE, 
                  stdout=subprocess.PIPE, 
                  stderr=subprocess.PIPE
                )

def find_new_position(pwm, startX, endX):
    half_width = WIDTH/2
    middle_of_feature = startX + ((endX-startX)/ 2)
    if (middle_of_feature > half_width): # if too far right
        pwm -= 0.5
    else:
        pwm += 0.5
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
                img = imutils.resize(img, width=WIDTH, height=HEIGHT)
                img = np.array(img)
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
                            pwm = find_new_position(pwm, startX, endX)

                yield cv2.imencode('.jpg', img)[1].tobytes()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()




    
