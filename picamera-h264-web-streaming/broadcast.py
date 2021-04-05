from threading import Thread

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
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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