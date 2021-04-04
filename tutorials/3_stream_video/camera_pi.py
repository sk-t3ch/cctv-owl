# Taken From https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited 
import io
import time
import picamera
from base_camera import BaseCamera
import numpy as np
from PIL import Image
import cv2

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
                img = np.array(img)
                img = Image.open(stream)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                yield cv2.imencode('.jpg', img)[1].tobytes()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()




    
