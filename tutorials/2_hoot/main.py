import subprocess

command = "omxplayer -o alsa:hw:1,0 ../../assets/owl_sound.mp3 --vol 500"

player = subprocess.Popen(command.split(' '), 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE
                          )
