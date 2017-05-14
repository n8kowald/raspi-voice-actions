#!/usr/bin/env python3
#
# play.py

# Play music from YouTube
# Created by @mikerr: https://www.raspberrypi.org/forums/viewtopic.php?p=1158827#p1158827
#
# Dependencies:
#   * vlc - install: sudo apt-get install vlc
#   * mps-youtube, youtube-dl - install: sudo pip3 install mps-youtube youtube-dl
##
import logging
import RPi.GPIO as gpio
import subprocess
import time

playshell = None
class play(object):

    def __init__(self, say, keyword):
        self.say = say
        self.keyword = keyword

    def run(self, voice_command):
        track = voice_command.replace(self.keyword, '', 1)

        global playshell
        if (playshell == None):
            playshell = subprocess.Popen(["/usr/local/bin/mpsyt",""],stdin=subprocess.PIPE ,stdout=subprocess.PIPE)

        playshell.stdin.write(bytes('/' + track + '\n1\n', 'utf-8'))
        playshell.stdin.flush()

        gpio.setmode(gpio.BCM)
        gpio.setup(23, gpio.IN)

        while gpio.input(23):
             time.sleep(1)

        while True:
            if gpio.input(23):
                pkill = subprocess.Popen(["/usr/bin/pkill","vlc"],stdin=subprocess.PIPE)
                break
            time.sleep(0.1)
