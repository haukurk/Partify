import time
import sys

import tweepy

from partify.modules.twitter import auth, filters


def start(hashtags, callback):
    listen = PartifyTwitterStreamListener(tweepy.API(auth), callback)
    stream = tweepy.Stream(auth, listen)

    try:
        stream.filter(track=hashtags)
    except:
        stream.disconnect()


class PartifyTwitterStreamListener(tweepy.StreamListener):

    def __init__(self, api, callback):
        self.api = api
        self.callback = callback
        super(tweepy.StreamListener, self).__init__()

    def on_status(self, status):
        data = filters.filter_twitter_status(status)
        self.callback(data)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream