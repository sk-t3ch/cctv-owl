import cv2
import numpy as np

def classify_frame(net, inputQueue, outputQueue):
	while True:
		if not inputQueue.empty():
			frame = inputQueue.get()
			# frame = cv2.resize(frame, (300, 300))
			blob = cv2.dnn.blobFromImage(frame, 1/125,
				(300, 300), 127.5)
			net.setInput(blob)
			detections = net.forward()
			outputQueue.put(detections)
