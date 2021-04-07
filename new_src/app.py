import os
import time
from imutils.video import VideoStream
from flask import Flask, render_template, Response, request, jsonify
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
import threading
import imutils
import time
import cv2
from PIL import Image
from utils import *
from flask_cors import CORS, cross_origin


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 50)
pwm = 7.5


box_color = (0, 0, 255)
label_text_color = (255, 255, 255)

outputFrame = None
lock = threading.Lock()
engine = DetectionEngine('./tpu/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
labels = dataset_utils.read_label_file('./tpu/coco_labels.txt')

# USER CONFIG
selected_label = 'person'
selected_threshold = 0.7
config = {
    'selected_label': selected_label,
    'selected_threshold': selected_threshold
}

app = Flask(__name__)
cors = CORS(app)

PI_IMAGE_WIDTH = 320
PI_IMAGE_HEIGHT = 240
vs = VideoStream(usePiCamera=True, resolution=(PI_IMAGE_WIDTH, PI_IMAGE_HEIGHT)).start()
# vs = VideoStream(src=0).start()
time.sleep(2.0)

def process_frame(frame, selected_label, selected_threshold=0.7):
    prep_img = Image.fromarray(frame.copy())
    detections = engine.detect_with_image(prep_img,
                                       threshold=selected_threshold,
                                       keep_aspect_ratio=True,
                                       relative_coord=False,
                                       top_k=10)
    shift_difference, shift_direction = 0, 0 # To be removed after tracking
    if detections:
        filtered_detections = filter(lambda obj: labels[obj.label_id]==selected_label, detections)
        for obj in filtered_detections:
            object_name = labels[obj.label_id]
            box = obj.bounding_box.flatten().tolist()
            box_left = int(box[0])
            box_top = int(box[1])
            box_right = int(box[2])
            box_bottom = int(box[3])

            draw_label(frame, object_name, obj.score, box_left, box_top, box_right, box_bottom)
            shift_difference, shift_direction = determine_shift(frame.shape[0], box_left, box_right)

    return frame, shift_difference, shift_direction

def draw_label(frame, obj_name, obj_score, box_left, box_top, box_right, box_bottom):
    cv2.rectangle(frame, (box_left, box_top),
                            (box_right, box_bottom), box_color, 1)
    percentage = int(obj_score * 100)
    label_text = obj_name + \
        " (" + str(percentage) + "%)"
    label_size = cv2.getTextSize(label_text,
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    1)[0]
    label_left = box_left
    label_top = box_top - label_size[1]
    if (label_top < 1):
        label_top = 1
    label_right = label_left + label_size[0]
    label_bottom = label_top + label_size[1]
    cv2.rectangle(frame, (label_left - 1, label_top - 1),
                    (label_right + 1, label_bottom + 1), box_color,
                    -1)
    cv2.putText(frame, label_text, (label_left, label_bottom),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_text_color, 1)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/config", methods=['POST'])
def updateConfig():
    print("REQUEST: ", request)
    return jsonify(config)


def detect_objects():
    global cap, outputFrame, lock, selected_label, selected_threshold
    pwm = 7.5
    p.start(7.5)

    while True:
        start_time = time.time()
        frame = vs.read()

        # TAG AND TRACK
        frame, shift_difference, shift_direction = process_frame(frame, selected_label, selected_threshold)

        # print("#### ", shift_difference, shift_direction)
        # ROTATE
        if shift_direction:
            pwm = determine_update_movement(pwm, shift_direction, shift_difference)
            p.ChangeDutyCycle(pwm)
            # print("####p ", pwm)
        cv2.putText(frame, f"PWM: {pwm}. {shift_direction}", (
                90, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, box_color, 1)

        # FPS
        fps = round(1.0 / (time.time() - start_time), 0)
        cv2.putText(frame, f"FPS: {fps}", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, box_color, 1)

        with lock:
            outputFrame = cv2.resize(frame, (640, 480))


def generate():
    global outputFrame, lock
    while True:
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) +
               b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    t = threading.Thread(target=detect_objects)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True,
            use_reloader=False)

vs.stop()
