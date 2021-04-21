import os
import time
from imutils.video import VideoStream
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
import threading
import imutils
import time
import cv2
from PIL import Image
from utils import *
from flask_cors import CORS, cross_origin
import requests
from make_sound import hoot 
import numpy as np
import RPi.GPIO as GPIO

from motrackers import CentroidTracker #, CentroidKF_Tracker, SORT, IOUTracker
from motrackers.utils import draw_tracks
from motrackers.utils.misc import get_centroid
tracker = CentroidTracker(max_lost=0, tracker_output_format='mot_challenge')
# tracker = CentroidKF_Tracker(max_lost=0, tracker_output_format='mot_challenge')
# tracker = SORT(max_lost=3, tracker_output_format='mot_challenge', iou_threshold=0.3)
# tracker = IOUTracker(max_lost=2, iou_threshold=0.5, min_detection_confidence=0.4, max_detection_confidence=0.7,
#                     tracker_output_format='mot_challenge')

MOTOR_PIN = 12
PI_IMAGE_WIDTH = 320
PI_IMAGE_HEIGHT = 240
OUTPUT_IMAGE_WIDTH = 640
OUTPUT_IMAGE_HEIGHT = 480

box_color = (255, 0, 0) # green
label_text_color = (255, 255, 255) # white

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(MOTOR_PIN, GPIO.OUT)
p = GPIO.PWM(MOTOR_PIN, 50)
pwm = 7.5

outputFrame = None
lock = threading.Lock()

# CORAL MODEL
engine = DetectionEngine('./tpu/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
labels = dataset_utils.read_label_file('./tpu/coco_labels.txt')

config = {
    'label': 'person',
    'threshold': 0.7,
    'tracking': 'manual',
    'hoot': False,
    'pwm': 7.5
}

app = Flask(__name__,
            static_folder = "./frontend/dist/static",
            template_folder = "./frontend/dist"
            )
cors = CORS(app)

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
    if detections and selected_label != "all":
        detections = list(filter(lambda obj: labels[obj.label_id]==selected_label, detections))
    return detections


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


@app.route("/config", methods=['POST'])
def update_config():
    global config
    new_config = request.get_json()
    config = new_config
    return jsonify(config)


def detect_objects():
    global cap, outputFrame, lock, config
    shift_difference, shift_direction = None, None
    pwm = 7.5
    old_pwm = 7.5
    p.start(5)

    while True:
        start_time = time.time()
        frame = vs.read()

        detections = process_frame(frame, config["label"], config["threshold"])
        
        for obj in detections:
            object_name = labels[obj.label_id]
            # if detections do the hoot thing
            box = obj.bounding_box.flatten().tolist()
            box_left = int(box[0])
            box_top = int(box[1])
            box_right = int(box[2])
            box_bottom = int(box[3])
            draw_label(frame, object_name, obj.score, box_left, box_top, box_right, box_bottom)

        if config["tracking"] != "manual":
            if detections:
                bboxes = np.array([obj.bounding_box.flatten() for obj in detections])
                confidences = [obj.score for obj in detections]
                class_ids = [obj.label_id for obj in detections]
                tracks = tracker.update(bboxes, confidences, class_ids)
                # (<frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>)
                frame = draw_tracks(frame, tracks)
                if config["tracking"] == "centroid":
                    #                           (xmin,   ymin,   width,  height)
                    tracked_bboxes = np.array([ (obj[2], obj[3], obj[4], obj[5]) for obj in tracks ])
                    tracked_bbox_centroids = get_centroid(tracked_bboxes)
                    centroid = np.mean(tracked_bbox_centroids, axis=0)
                elif config["tracking"] == "single":
                    # [(1, 0, 25, 47, 110, 163, 0.73046875, -1, -1, -1)]
                    latest_track = max(tracks,  key=lambda t: t[1]) # tracking_id
                    track = latest_track
                    tracked_bbox = np.array([track[2], track[3], track[4], track[5]])
                    centroid = get_centroid(tracked_bbox)
                    print("centroid", centroid)
                shift_difference, shift_direction = determine_shift(frame.shape[0], centroid[0])
                print("changing", shift_direction, shift_difference)
                pwm = determine_update_movement(pwm, shift_direction, shift_difference)
        else:
            pwm = config["pwm"]


        # check for diff in pwm
        # if old_pwm != pwm:
        #     p.start(pwm)
        #     p.ChangeDutyCycle(pwm)
        # else:
        #     p.stop()
        p.start(pwm)
        p.ChangeDutyCycle(pwm)
        old_pwm = pwm

        cv2.putText(frame, f"PWM: {pwm}. {shift_direction}", (
                90, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, box_color, 1)

        # FPS
        fps = round(1.0 / (time.time() - start_time), 0)
        cv2.putText(frame, f"FPS: {fps}", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, box_color, 1)

        with lock:
            outputFrame = cv2.resize(frame, (OUTPUT_IMAGE_WIDTH, OUTPUT_IMAGE_HEIGHT))


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


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    t = threading.Thread(target=detect_objects)
    t.daemon = True
    t.start()
    app.debug = True
    app.run(host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True,
            use_reloader=False)

vs.stop()
