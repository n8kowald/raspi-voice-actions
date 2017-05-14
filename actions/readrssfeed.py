import feedparser
import time

##
# readrssfeed.py
# Feedparser is used to parse the rss feeds (for more information: http://www.pythonforbeginners.com/feedparser/using-feedparser-in-python)
#
# Created by: @markblue777 - https://www.raspberrypi.org/forums/viewtopic.php?p=1160812#p1160812
#
# Dependencies:
# feedparser - install: sudo pip install feedparser
#
# Usage:
# actor.add_keyword(_('the news'), readrssfeed(say, "http://feeds.bbci.co.uk/news/rss.xml?edition=uk#",10))
##
class readrssfeed(object):
    # This is the BBC rss feed for top news in the uk
    # http://feeds.bbci.co.uk/news/rss.xml?edition=uk

    #######################################################################################
    # constructor
    # url - rss feed url to read
    # feedCount - number of records to read
    # -(for example bbc rss returns around 62 items and you may not want all of
    # them read out so this allows limiting
    #######################################################################################
    def __init__(self, say, url, feedCount):
        self.say = say
        self.rssFeedUrl = url
        self.feedCount = feedCount

    def run(self, voice_command):
        res = self.getNewsFeed()

        # If res is empty then let user know
        if res == "":
            self.say('Cannot get the feed')

        # loop res and speak the title of the rss feed
        # here you could add further fields to read out
        for index in range(len(res)):
            itemNumber = str(index + 1)
            self.say("Item " + itemNumber + ". " + res[index].title_detail.value)

        # TODO: Stop voice by pressing the button

    def getNewsFeed(self):
        # parse the feed and get the result in res
        res = feedparser.parse(self.rssFeedUrl)

        # get the total number of entries returned
        resCount = len(res.entries)

        # exit out if empty
        if resCount == 0:
            return ""

        # if the resCount is less than the feedCount specified cap the feedCount to the resCount
        if resCount < self.feedCount:
            self.feedCount = resCount

        # create empty array
        resultList = []

        # loop from 0 to feedCount so we append the right number of entries to the return list
        for x in range(0,self.feedCount):
            resultList.append(res.entries[x])

        return resultList
