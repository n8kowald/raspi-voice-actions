#!/usr/bin/env python3
#
# RadioAction.py
# Play radio stations with 'radio %station%'
#
# Created by @ktinkerer: https://www.raspberrypi.org/forums/viewtopic.php?p=1160155#p1160155
#
# Dependencies:
#   * vlc - install: sudo apt-get install vlc
##
import logging
import RPi.GPIO as gpio
import subprocess
import time

class RadioAction(object):

    radio_stations = {
        'absolute 80s': "http://network.absoluteradio.co.uk/core/audio/mp3/live.pls?service=a8bb",
        'bbc 1 extra': "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1xtra_mf_p?s=1494265403",
        'bbc 1': "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_p?s=1494265262",
        'bbc 2': "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio2_mf_p?s=1494265194",
        'bbc 3': "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio3_mf_p?s=1494265402",
        'bbc 4 extra': "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio4extra_mf_q?s=1494265404",
        'bbc 4': "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio4fm_mf_p?s=1494265402",
        'bbc 5': "http://open.live.bbc.co.uk/mediaselector/5/redir/version/2.0/mediaset/http-icy-mp3-a-stream/proto/http/vpid/bbc_radio_five_live",
        'bbc 6': "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_6music_mf_p?s=1494265223",
        # Thanks to philicibine for this! https://www.raspberrypi.org/forums/viewtopic.php?p=1161489#p1161489
        'bbc world service': "http://wsdownload.bbc.co.uk/worldservice/meta/live/shoutcast/mp3/eieuk.pls",
        'news': "http://wsdownload.bbc.co.uk/worldservice/css/96mp3/latest/bbcnewssummary.mp3",
        'fresh fm': "http://www.fresh927.com.au/streams/liveAAC.m3u",
        'home': "http://www.australianliveradio.com/5aa.m3u",
        'lbc': 'http://media-ice.musicradio.com/LBCLondonMP3Low.m3u',
        'london': "http://www.radiofeeds.co.uk/bbclondon.pls",
        'nova': "http://www.australianliveradio.com/nova919.m3u",
    }

    def __init__(self, say, keyword):
        self.say = say
        self.keyword = keyword

    def get_station(self, station_name):
        return self.radio_stations[station_name]

    def list_stations(self):
        self.say("Here are the available radio stations")

        # TODO: Maintain order of dict
        for station in self.radio_stations:
            self.say(station)

    def run(self, voice_command):

        # List available stations
        if (voice_command.lower() == self.keyword + ' stations'):
            self.list_stations()
            return

        global station
        try:
            voice_command = (voice_command.lower().replace(self.keyword, '', 1)).strip()
            self.say("Tuning the radio into " + voice_command)
            logging.info("Looking for this station in the radio_stations dictionary: " + voice_command)
            station = self.get_station(voice_command)
        except KeyError:
            self.say("Voice command not recognised. To hear a list of available radio stations say, radio stations")
            return

        p = subprocess.Popen(["/usr/bin/cvlc",station],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        p.poll()

        gpio.setmode(gpio.BCM)
        gpio.setup(23, gpio.IN)

        while True:
            if gpio.input(23):
                logging.info("stopping radio")
                p.kill()
                break
            time.sleep(0.1)
