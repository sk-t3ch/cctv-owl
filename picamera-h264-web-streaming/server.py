#!/usr/bin/env python


import io
import picamera

from os import curdir, sep
from string import Template

from threading import Thread
from time import sleep, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from wsgiref.simple_server import make_server
from broadcast import BroadcastThread
from output import StreamingOutput

from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import (
    WSGIServer,
    WebSocketWSGIHandler,
    WebSocketWSGIRequestHandler,
)
from ws4py.server.wsgiutils import WebSocketWSGIApplication

###########################################
# CONFIGURATION
WIDTH = 640
HEIGHT = 480
FRAMERATE = 25
HTTP_PORT = 8082
WS_PORT = 8084


VFLIP = True
HFLIP = False

###########################################

###
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

###

class StreamingHttpHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET()


    def do_GET(self):
        #Serve index.html
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
            return
        elif self.path == '/index.html':
            content_type = 'text/html; charset=utf-8'
            tpl = Template(self.server.index_template)
            content = tpl.safe_substitute(dict(
                ADDRESS='%s:%d' % (self.request.getsockname()[0], WS_PORT)
                ))
        #Serve js
        elif self.path.startswith('/js/'):
            f = open(curdir + sep + self.path)
            
            self.send_response(200)
            self.send_header('Content-type',    'application/javascript')
            self.end_headers()
            self.wfile.write(bytes(f.read(),encoding='utf-8'))
            f.close()
            return
        #Serve css
        elif self.path.startswith('/css/'):
            f = open(curdir + sep + self.path)
            self.send_response(200)
            self.send_header('Content-type',    'text/css')
            self.end_headers()
            self.wfile.write(bytes(f.read(),encoding='utf-8'))
            f.close()
            return
            
        else:
            self.send_error(404, 'File not found')
            return
        content = content.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(content))
        self.send_header('Last-Modified', self.date_time_string(time()))
        self.end_headers()
        if self.command == 'GET':
            self.wfile.write(content)



class StreamingHttpServer(HTTPServer):
    def __init__(self):
       
        super(StreamingHttpServer, self).__init__(
                    ('', HTTP_PORT), StreamingHttpHandler)
        with io.open('index.html', 'r') as f:
            self.index_template = f.read()


class StreamingWebSocket(WebSocket):
    def opened(self):
        print("New client connected")
        # you can override various WebSocket class methods
        # to do more stuff with WebSockets other than streaming
        


def main():

    #Camera and the configuration
    print('Initializing camera')
    camera = picamera.PiCamera()
    camera.framerate = FRAMERATE
    camera.resolution = (WIDTH, HEIGHT)
    camera.vflip = VFLIP # flips image rightside up, as needed
    camera.hflip = HFLIP # flips image left-right, as needed
    sleep(1) # camera warm-up time

    #Custom output for h264 stream
    output = StreamingOutput()    

    #Websocket
    print('Initializing websockets server on port %d' % WS_PORT)
    WebSocketWSGIHandler.http_version = '1.1'
    websocket_server = make_server(
            '', WS_PORT,
            server_class=WSGIServer,
            handler_class=WebSocketWSGIRequestHandler,
            app=WebSocketWSGIApplication(handler_cls=StreamingWebSocket))

    websocket_server.initialize_websockets_manager()
    websocket_thread = Thread(target=websocket_server.serve_forever)

    #Http
    print('Initializing HTTP server on port %d' % HTTP_PORT)
    http_server = StreamingHttpServer()
    http_thread = Thread(target=http_server.serve_forever)
   
    #Broadcast
    print('Initializing broadcast thread')
    broadcast_thread = BroadcastThread(camera, output, websocket_server)


    # Start the threads here   
    try:
        print('Starting websockets thread')
        websocket_thread.start()
        print('Starting HTTP server thread')
        http_thread.start()
        print('Starting recording and broadcastasting thread')
        broadcast_thread.start()
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:

        print('Stopping recording')
        camera.stop_recording()
        print('Waiting for broadcast thread to finish')
        broadcast_thread.join()
        print('Shutting down HTTP server')
        http_server.shutdown()
        print('Shutting down websockets server')
        websocket_server.shutdown()
        print('Waiting for HTTP server thread to finish')
        http_thread.join()
        print('Waiting for websockets thread to finish')
        websocket_thread.join()
    


if __name__ == '__main__':
    main()
