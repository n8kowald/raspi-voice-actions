import feedparser
import time
import logging

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
# actor.add_keyword(_('news headlines'), readrssfeed(say, "http://feeds.bbci.co.uk/news/rss.xml?edition=uk", "title", 10))
# actor.add_keyword(_('currency check'), readrssfeed(say, "http://gbp.fxexchangerate.com/AUD.xml", "summary", 1, True))
##
class readrssfeed(object):
    # This is the BBC rss feed for top news in the uk
    # http://feeds.bbci.co.uk/news/rss.xml?edition=uk

    #######################################################################################
    # constructor
    # url - rss feed url to read
    # targetElement - The element in the RSS feed you want to say
    # feedCount - number of records to read
    # -(for example bbc rss returns around 62 items and you may not want all of
    # them read out so this allows limiting
    # firstLineOnly - Speak the first line of the result only
    #######################################################################################
    def __init__(self, say, url, targetElement, feedCount, firstLineOnly = False):
        self.say = say
        self.rssFeedUrl = url
        self.targetElement = targetElement
        self.feedCount = feedCount
        self.firstLineOnly = firstLineOnly

    def run(self, voice_command):
        res = self.getNewsFeed()

        # If res is empty then let user know
        if res == "":
            self.say('Cannot get the feed')

        # loop res and speak the title of the rss feed
        # here you could add further fields to read out
        for index in range(len(res)):

            # Test if the target element exists
            try:
                content = res[index][self.targetElement]
            except KeyError:
                logging.info('Target element ' + self.targetElement + ' does NOT exist in this feed')
                self.say('Target element, ' + self.targetElement + ' does not exist in this feed')
                results = str(res[index])
                logging.info('Here is the available info from this feed: ' + results);
                return

            # If more than one item is requested: add the item number to the voice
            if (index > 1):
                itemNumber = str(index + 1)
                sayPrefix = 'Item ' + itemNumber + '. '
            else:
                sayPrefix = ''

            # Replace HTML <br> tags with newlines
            content = content.replace('<br/>', '\n').replace('<br>', '\n').replace('<br />', '\n')

            # Remove all but first lines if firstLineOnly is True
            if self.firstLineOnly:
                content = content.split('\n', 1)[0]

            # Speak!
            #logging.info('Available info from ' + self.url + ': ' + res[index]);
            logging.info('RSS feed content for say: ' + content);
            self.say(sayPrefix + content)

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
