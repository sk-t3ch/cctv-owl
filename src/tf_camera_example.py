import io
import io
import picamera
import logging
import socketserver
from threading import Condition
from PIL import ImageFont, ImageDraw, Image
import cv2
import traceback
import numpy as np
import datetime as dt
import imutils
import os
import argparse
import sys
import time
from threading import Thread
import importlib.util


from http.server import BaseHTTPRequestHandler, HTTPServer


WIDTH=300
HEIGHT=300

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
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
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

PAGE = """\
<html>
<head>
<title>SkyWeather MJPEG streaming demo</title>
</head>
<body>
<h1>SkyWeather MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="1296" height="730" />
</body>
</html>
"""


def process_frame(frame):
    # Convert to PIL Image
    cv2.CV_LOAD_IMAGE_COLOR = 1  # set flag to 1 to give colour image
    npframe = np.fromstring(frame, dtype=np.uint8)
    pil_frame = cv2.imdecode(npframe, cv2.CV_LOAD_IMAGE_COLOR)
    #pil_frame = cv2.imdecode(frame,-1)
    pil_frame = imutils.resize(pil_frame, width=WIDTH, height=HEIGHT)
    frame_rgb = cv2.cvtColor(pil_frame, cv2.COLOR_BGR2RGB)
    # pil_im = Image.fromarray(frame_rgb)

    # 
    # (fH, fW) = cv2_im_rgb.shape[:2]

    # blob = cv2.dnn.blobFromImage(cv2_im_rgb, 1/125, (300, 300), 127.5)
    # net.setInput(blob)
    # detections = net.forward()
    # for i in np.arange(0, detections.shape[2]):
    #     confidence = detections[0, 0, i, 2]
    #     if confidence < 0.1:
    #         continue
    #     idx = int(detections[0, 0, i, 1])
    #     dims = np.array([fW, fH, fW, fH])
    #     box = detections[0, 0, i, 3:7] * dims
    #     (startX, startY, endX, endY) = box.astype("int")
    #     label = f"{CLASSES[idx]}: {confidence * 100}"
    #     print("LABEL:", label)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
    #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)

    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
            
            cv2.rectangle(frame_rgb, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

            # Draw label
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(frame_rgb, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(frame_rgb, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

    pil_im = Image.fromarray(frame_rgb)

    draw = ImageDraw.Draw(pil_im)
    # Choose a font
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf", 25)
    myText = "SkyWeather " + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Draw the text
    color = 'rgb(255,255,255)'
    #draw.text((0, 0), myText,fill = color, font=font)

    # get text size
    text_size = font.getsize(myText)

    # set button size + 10px margins
    button_size = (text_size[0] + 20, text_size[1] + 10)

    # create image with correct size and black background
    button_img = Image.new('RGBA', button_size, "black")

    #button_img.putalpha(128)
    # put text on button with 10px margins
    button_draw = ImageDraw.Draw(button_img)
    button_draw.text((10, 5), myText, fill=color, font=font)

    pil_im.paste(button_img, (0, 0))
    bg_w, bg_h = pil_im.size
    # WeatherSTEM logo in lower left
    size = 64
    # WSLimg = Image.open("WeatherSTEMLogoSkyBackground.png")
    # WSLimg.thumbnail((size,size),Image.ANTIALIAS)
    # pil_im.paste(WSLimg, (0, bg_h-size))

    # # SkyWeather log in lower right
    # SWLimg = Image.open("SkyWeatherLogoSymbol.png")
    # SWLimg.thumbnail((size,size),Image.ANTIALIAS)
    # pil_im.paste(SWLimg, (bg_w-size, bg_h-size))

    # Save the image
    buf = io.BytesIO()
    pil_im.save(buf, format='JPEG')
    frame = buf.getvalue()
    return frame


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)



class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type',
                             'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                        frame = process_frame(frame)
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                traceback.print_exc()
                logging.warning('Removed streaming client %s: %s',
                                self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


#with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
#with picamera.PiCamera(resolution='1920x1080', framerate=24) as camera:
with picamera.PiCamera(resolution='320x240', framerate=2) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    camera.annotate_foreground = picamera.Color(y=0.2, u=0, v=0)
    camera.annotate_background = picamera.Color(y=0.8, u=0, v=0)
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()