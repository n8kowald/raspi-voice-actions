#!/usr/bin/env python3
#
# PowerAction.py
# Shutdown or reboot the Pi with your voice
#
# Created by @ktinkerer: https://github.com/ktinkerer/aiyprojects-raspbian/blob/shutdown/src/action.py
##
import logging
import subprocess

class PowerAction(object):
    def __init__(self, say, command):
        self.say = say
        self.command = command

    def run(self, voice_command):
        if self.command == "shutdown":
            self.say("Shutting down, goodbye")
            subprocess.call("sudo shutdown now", shell=True)
        elif self.command == "reboot":
            self.say("Rebooting")
            subprocess.call("sudo shutdown -r now", shell=True)
        else:
            logging.error("Error identifying power command.")
            self.say("Sorry I didn't identify that command")
