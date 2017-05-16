#!/usr/bin/env python3
#
# Kilian.py

# Get data about kilianonline's videos
#
# Dependencies:
#   * mps-youtube, youtube-dl - install: sudo pip3 install mps-youtube youtube-dl
#                               configure it: mpsyt set player vlc, set playerargs vlc, exit
#   * vlc - run: sudo apt-get install vlc
##
import logging
import RPi.GPIO as gpio
import subprocess
import time
import re
import locale
locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

playshell = None
class KilianAction(object):

    def __init__(self, say, keyword):
        self.say = say
        self.keyword = keyword

    def run(self, voice_command):
        command = voice_command.lower().replace(self.keyword, '', 1)

        global playshell
        if (playshell == None):
            playshell = subprocess.Popen(["/usr/local/bin/mpsyt",""],stdin=subprocess.PIPE ,stdout=subprocess.PIPE)

        #if (command == 'views'):
        playshell.stdin.write(bytes('set search_music False\n', 'utf-8'))
        playshell.stdin.write(bytes('set user_order date\n', 'utf-8'))
        playshell.stdin.write(bytes('user kilianonline\n', 'utf-8'))
        playshell.stdin.write(bytes('i 1\n', 'utf-8'))
        output = playshell.communicate()[0].decode('utf-8')
        views = re.search('View count\s:\s([0-9]*)\n', output).group(1)
        views = locale.format("%d", int(views), grouping=True)
        logging.info('View count found: ' + views)
        published = re.search('Published\s+:\s+(.*)\n', output).group(1)
        videos = re.findall('[1-5] .*\n', output)
        #topFive = matches[:5]
        lastVideoUploaded = re.search('[1-5]\s+Kilian\s-\s(.*)\d{2}:\d{2}$', videos[0]).group(1)
        self.say("The last video uploaded by Kilian is: " + lastVideoUploaded)
        self.say("It was uploaded on " + published + " and has " + views + " views")

        # Play it
        playshell = subprocess.Popen(["/usr/local/bin/mpsyt",""],stdin=subprocess.PIPE ,stdout=subprocess.PIPE)
        playshell.stdin.write(bytes('set search_music False\n', 'utf-8'))
        playshell.stdin.write(bytes('set user_order date\n', 'utf-8'))
        playshell.stdin.write(bytes('user kilianonline\n', 'utf-8'))
        playshell.stdin.write(bytes('1\n', 'utf-8'))
        self.say("It sounds like this")
        playshell.stdin.flush()

        # Stop voice by pressing the button
        gpio.setmode(gpio.BCM)
        gpio.setup(23, gpio.IN)
        while True:
            if gpio.input(23):
                logging.info("Stopping YouTube playback")
                pkill = subprocess.Popen(["/usr/bin/pkill","vlc"],stdin=subprocess.PIPE)
                break
            time.sleep(0.1)
