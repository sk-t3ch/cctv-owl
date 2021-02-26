# 🦉Zombie Detecting Smart Security Owl (Deep Learning)

In this Halloween tutorial, we’ll be showing you how we put a super spooky twist on a mundane household classic: the security camera. How?! We’ve made a night vision owl which uses image processing to track people. Oh, and it hoots, just like the real thing!

<center><iframe width='560' height='315' src ='https://www.youtube.com/embed/$aLX4btGs_x8' frameborder='0' allowfullscreen></iframe></center>

We’ve been super excited about this project and we’ve been waiting to do it ever since the new Raspberry Pi 4 dropped. It’s got 4GB RAM, which opens the door to loads of really exciting possibilities, including doing some image processing with deep learning models in real time.

If you want to keep an eye out for approaching zombies on Halloween, or just check your garden the rest of the year round, this is the one for you. Security doesn’t have to be boring to be effective!

## Notes

* [Video](https://youtu.be/aLX4btGs_x8)

* [Code](https://github.com/sk-t3ch/cctv-owl)

## Supplies

For this build, you will need:

* Raspberry Pi 4 (4GB Ram) [Amazon](https://amzn.to/2MNkHyM)

* Night Vision Camera [Amazon](https://amzn.to/2MMqXa1)

* Micro Servo [Amazon](https://amzn.to/2BLTlCR)

* Fake Owl [Amazon](https://amzn.to/31S2qEO)

* Glue [Amazon](https://amzn.to/2NdoNiU)

* Paint [Amazon](https://amzn.to/2WiDaGQ)

* Screws [Amazon](https://amzn.to/2JqCjyl)

* USB speaker [Amazon](https://amzn.to/2BNuPBr)

* Large (5v+) portable power supply [Amazon](https://amzn.to/2BLTlCR)

* 3D printer [Amazon](https://amzn.to/31NpuES)

## Build 🛠️

### 1. Decapitate

a. Pull the head off the owl (sometimes you just have to be brutal) by pulling hard on its head where it attaches to the spring.

![](https://cdn-images-1.medium.com/max/6720/1*7rq75YSq5iwv4MVWwZOp8Q.png)

b. The owl’s head connects to the body by a cylinder which sits on top of a large spring. Remove this cylinder by taking out the screw.

![](https://cdn-images-1.medium.com/max/6720/1*SS4iGqFmv8xcYCBXL1Fj8g.png)

![](https://cdn-images-1.medium.com/max/6720/1*8rOZrDB63YvHblKlV0D7Og.png)

c. The cylinder you just removed is made of two parts, a plastic cup and a bearing which sits inside it. Remove the bearing from the cylinder using a screwdriver (or similar tool).

![](https://cdn-images-1.medium.com/max/6720/1*-uDi1YWPXH4W4_3Sb_Zt1g.png)

d. Remove the spring by unscrewing the three screws that secure it to the body.

![](https://cdn-images-1.medium.com/max/6720/1*p8Q1CHVBUWIeQgEThEj-XA.png)

e. Make a hole in the top of the owl’s body which is large enough to fit some wires and the camera cable. We used an inelegant combination of a drill and a screwdriver to do this.

![](https://cdn-images-1.medium.com/max/6720/1*78TkdVagBYkE4wa0D1l9_w.png)

### 2. Add Smart 🧠

a. 3D print the camera case and paint it to match the owl — we used some cheap acrylic paints. Painting isn’t a vital step, but it does dramatically improve the overall look!
[**Raspberry Pi Night Vision Camera Mount IR CUT by Minims**
*Works with Raspberry Pi and night vision camera using auto IR CUT + Infrared spots : =>…*www.thingiverse.com](https://www.thingiverse.com/thing:2755175/makes)
[**GoPro compatible visor mount by olivermandic**
*Download files and build them with your 3D printer, laser cutter, or CNC. Thingiverse is a universe of things.*www.thingiverse.com](https://www.thingiverse.com/thing:2860717)

![](https://cdn-images-1.medium.com/max/6720/1*ue2DKZxCQ-VeY9PBZVQyfw.png)

b. With the owl’s head upside down, screw the top of the camera case into the inside of its head, where the beak protrudes.

![](https://cdn-images-1.medium.com/max/6720/1*G5U6JG6M2J8FR4us0ietaQ.png)

c. Put the camera into the case and connect the camera cable.

d. Glue the servo to the top panel of the spring.

![](https://cdn-images-1.medium.com/max/6720/1*L2uYQovtJrzuLFYgU2ydZw.png)

e. Connect long wires to the servo pins (5V, GND, Signal)

f. Feed the camera cable and wires for the servo through the spring and through the hole you made in the top of the body so they are inside the owl’s hollow body.

![](https://cdn-images-1.medium.com/max/6720/1*iXR0f4iOzNebi8kh_8JIAg.png)

g. Screw the neck back together and push the head on.

![](https://cdn-images-1.medium.com/max/6720/1*Ze0cqRPQkePOlF0LeyaKCw.png)

![](https://cdn-images-1.medium.com/max/6720/1*2XX4iiSlH4VmQLdKKqd2Dg.png)

### 3. Fill Her Up 🤖

a. Remove the plug from the bottom of the owl and increase the size of this hole by cutting the plastic. Continue increasing the size until the Raspberry Pi and speaker can fit through into the body of the owl.

![](https://cdn-images-1.medium.com/max/6720/1*E9a1eN6_xsrf7NSZeU1t7w.png)

![](https://cdn-images-1.medium.com/max/6720/1*s6d0wi6d3lw2gTssHZh2vQ.png)

b. Once the hole is big enough for all the components to fit inside, pull the camera cable which you fed through the top of the owl out of the base and plug it into the Raspberry Pi.

![](https://cdn-images-1.medium.com/max/6720/1*i89gxOJ34iGMPPGlNHa2DA.png)

c. Similarly, pull the servo wires through and plug them into the Raspberry Pi:
> ***+5V Servo => +5V Pi
GND Servo => GND Pi
Signal Servo => Pin 12 Pi***

![](https://cdn-images-1.medium.com/max/6720/1*V3CZ1ulT-C-gqqzIzzuGLw.png)

d. Plug the USB speaker into the Pi.

![](https://cdn-images-1.medium.com/max/6720/1*EkssCADAEsN6Ol9ZGAxsmQ.png)

e. Insert the SD card into the Pi.

f. Power Pi using portable power supply.

![](https://cdn-images-1.medium.com/max/6720/1*ZT64QwwB95yEWtEGskAy4Q.png)

g. Insert the Pi, power supply and speaker into owl through the hole in the base.

![](https://cdn-images-1.medium.com/max/6720/1*HPksQ8sEA6ouJqXW5HHQOA.png)

### 4. Setup the Pi 🥧

a. Download [Raspian](https://www.raspberrypi.org/downloads/) and upload it to your SD card using [Balena Etcher](https://www.balena.io/etcher).

b. To access your pi remotely:

* Add a file called ssh to your boot sd card

* Add a file called `wpa_supplicant.conf` and put your wifi credentials in

    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev update_config=1   
    network={   
             ssid="MySSID"   
             psk="MyPassword"  
    }

c. Insert the SD card in the pi and try an access via ssh.

### 5. Moving the Head ⚙️
> **Code tutorial for moving the head (controlling a servo with a raspberry pi) — [github](https://github.com/sk-t3ch/cctv-owl/tree/master/tutorials/1_move_the_head)**

To control a servo running on the Pi we are going to create script that controls the GPIO pins which the servo is connected to.

a. Ensure connections between the servo to the Pi:
> ***+5V Servo => +5V Pi
GND Servo => GND Pi
Signal Servo => Pin 12 Pi***

b. You must first set up the gpio pins to use PWM on the signal pin of the servo.

c. Then, it is as simple as selecting the duty cycle (explained here) of the signal pin to move the servo from 90 degrees with a duty cycle of 7.5 to 0 degrees when the duty cycle is 2.5 and to 180 degrees with a duty cycle of 12.5


```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)

p.start(7.5)
try:
    while True:
        p.ChangeDutyCycle(7.5)  # 90 degrees
        time.sleep(1)
        p.ChangeDutyCycle(2.5)  # 0 degrees
        time.sleep(1)
        p.ChangeDutyCycle(12.5) # 180 degrees
        time.sleep(1)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
```

### 6. Making It Hoot 🔉
> **Code tutorial for making the owl hoot (playing audio with a raspberry pi)-[github](https://github.com/sk-t3ch/cctv-owl/tree/master/tutorials/2_hoot)**

a. Plug in the USB speaker.

b. Download a sound — we chose a spooky hoot.

c. Play the sound by running this command: `omxplayer -o alsa:hw:1,0 owl_sound.mp3`

![](https://cdn-images-1.medium.com/max/2000/1*EcMl1RIOmM9TWTC5BUNxvQ.png)

![](https://cdn-images-1.medium.com/max/2000/1*4Hgbl5cMmm94q0DbnozPyQ.png)

[d. If this doesn’t work, check what output your Pi is using and at what volume by using the command alsamixer — you will be greeted with the mixer screen where you can change the volume and select your media device. To increase the volume of your sound, do the command like this `omgxplayer -o alsa:hw:1,0 owl_sound.mp3 -vol 500` to play this sound using Python, have a look at our test script.]


```python
import subprocess

command = "omxplayer -o alsa:hw:1,0 ../../assets/owl_sound.mp3 --vol 500"

player = subprocess.Popen(command.split(' '), 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE
                          )
```

### 7. Stream the Video From the Pi 🎦
> **Code tutorial creating a raspberry pi camera stream — [github](https://github.com/sk-t3ch/cctv-owl/tree/master/tutorials/3_stream_video)**

a. Run python `app.py` and view on your local network at `http://raspberrypi.local:5000` .

b. This code was taken and slightly adapted from Miguel Grinberg [blog post](https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited), he explains nicely how it’s done and his tutorials are great — deffo check him out! The basic concept is that we use threading and generators to improve the streaming speed.

The camera works in both night and dark.

![](https://cdn-images-1.medium.com/max/6712/1*dNIXGPUZLdpUZIRW1X2PpA.png)

![](https://cdn-images-1.medium.com/max/6698/1*D5S6-jzJzmKUrjRQyIT03w.png)

### 8. Body Detection 🕵️‍♀️
> **Code for body detection(ImageNetSSD on a video stream with raspberry pi) — [github](https://github.com/sk-t3ch/cctv-owl/tree/master/tutorials/4_object_detection)**

![](https://cdn-images-1.medium.com/max/6702/1*_Emu1QthbTEOYYSG3kkroQ.png)

a. Since we’re using the Raspberry Pi 4, we thought it was best to try out some deep learning models on it instead of the basic [HaarCascade](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html) method we’ve been limited to so far.

b. We had a look at some of the pre-trained models out there, like [YOLOv3](https://pjreddie.com/darknet/yolo/) which looks super cool. YOLOv3 tiny weights, which would have been perfect for the Pi, but we couldn’t get it running :(

c. Instead, we opted for the MobileSSD model which we can run using openCVs DNN (deep neural net) module, as we learnt from this [code](https://heartbeat.fritz.ai/real-time-object-detection-on-raspberry-pi-using-opencv-dnn-98827255fa60): and from the hero of image processing tutorials, [Adrian Rosebrock](https://www.pyimagesearch.com/2017/09/11/object-detection-with-deep-learning-and-opencv/).

d. However, as we are trying to stream this content and run models on every frame, this results in a laggy, fragmented video. We learnt again from [Adrian Rosebrock](https://www.pyimagesearch.com/2017/10/16/raspberry-pi-deep-learning-object-detection-with-opencv/) and used the Python multiprocessing module to put our images into queues where they can be processed without blocking the camera stream so heavily.

e. Try running the code yourself


```python
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe('../../model/MobileNetSSD_deploy.prototxt.txt',
                               '../../MobileNetSSD_deploy.caffemodel')
                               
                               
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
            cv2.rectangle(img, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            pwm = find_new_position(pwm, startX, endX)

```

### 9. Sending Zombie Notifications
> **Code for sending a notification (python to phone) — [github](https://github.com/sk-t3ch/cctv-owl/tree/master/tutorials/5_send_notifications)**

a. We decided to use [https://pushed.co ](https://pushed.co/)notification service.

![](https://cdn-images-1.medium.com/max/3840/1*NFWj71jx3sr6O0rPtYLhHg.png)

b. You can get a free account and download the app and really quickly get set up making mobile notifications. We created the notifications using a python script like this.


```python
import requests 

payload = {
          "app_key": "APP_KEY",
          "app_secret": "APP_SECRET",
          "target_type": "app",
          "content": "Zombie approaching!"
          }

r = requests.post("https://api.pushed.co/1/push", data=payload)
```

![](https://cdn-images-1.medium.com/max/6720/1*So_2fLRiOMjPpZrgRPK4ew.png)

## Step 10: What a Hoot!

We hope you enjoyed our Smart Security Owl project! This has been a super fun make and I feel a whole lot safer knowing my house is being guarded by our trusty owl. Checkout the [Youtube Video](https://youtu.be/aLX4btGs_x8).

![](https://cdn-images-1.medium.com/max/12000/1*v0DOwFnyENbPyaLqNf7jvg.png)

## Thanks For Reading

I hope you have enjoyed this article. If you like the style, check out [T3chFlicks.org](https://t3chflicks.org/) for more tech focused educational content ([YouTube](https://www.youtube.com/channel/UC0eSD-tdiJMI5GQTkMmZ-6w), [Instagram](https://www.instagram.com/t3chflicks/), [Facebook](https://www.facebook.com/t3chflicks), [Twitter](https://twitter.com/t3chflicks)).