# Taken From https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited 
import os
from flask import Flask, render_template, Response
from camera_pi import Camera
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 255)

app = Flask(__name__)

@app.route('/')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    """Video streaming generator function."""
    p.start(7.5)
    while True:
        frame, pwm = camera.get_frame()
        p.ChangeDutyCycle(pwm)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
