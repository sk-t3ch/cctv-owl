import subprocess

def hoot():
  command = "omxplayer -o alsa:hw:1,0 ../assets/owl_sound.mp3 --vol 200".split(' ')
  subprocess.Popen(command, 
                  stdin=subprocess.PIPE, 
                  stdout=subprocess.PIPE, 
                  stderr=subprocess.PIPE
                )
