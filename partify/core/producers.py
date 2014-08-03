__author__ = 'haukurk'

from flask import session
import tweepy
import os
import redis
import json
import time
import gevent
import config

import partify.modules.twitter
from partify.modules.twitter import filters


class CustomStreamListener(tweepy.StreamListener):
    """Listens to a twitter stream and publishes tweets to redis."""

    def __init__(self, tracking):
        """Gets redis instance."""

        if config.REDIS_AUTH is True:
            self._redis = redis.Redis(host=config.REDIS_IP, port=config.REDIS_PORT, password=config.REDIS_PASSWORD)
        else:
            self._redis = redis.Redis(host=config.REDIS_IP, port=config.REDIS_PORT)
        self._tracking = tracking
        self._channel = json.dumps(sorted(tracking))

        # Call StreamListener constructor
        super(CustomStreamListener, self).__init__()

    def on_status(self, status):
        """Publishes the Tweet to redis."""

        # Only get tweets that contain the tracking terms
        for term in self._tracking:
            if term.lower() not in status.text.lower():
                return

        # Publish the data
        data = filters.filter_twitter_status(status)

        self._redis.publish(self._channel, json.dumps(data))

        # Throttle our results
        time.sleep(1)


class StreamProducer(gevent.Greenlet):
    """Defines a Greenlet that publishes twitter data to redis."""

    def __init__(self, tracking):
        """Creates instance of CustomStreamListener."""

        self._stream_listener = CustomStreamListener(tracking)

        # The name of the channel will be the alpha-sorted tracking terms as a list.
        self.channel = json.dumps(sorted(tracking))
        self.tracking = tracking
        print "Creating a Producer: channel-", self.channel

        # Initialize the client list
        self.clients = []

        # Call gevent.Greenlet constructor
        super(StreamProducer, self).__init__()

    def _run(self):
        """Starts the twitter stream listener/redis-publisher."""
        # Listen to the stream of tweets containing the words/hashtags in 'filtering'
        stream = tweepy.Stream(partify.modules.twitter.auth, self._stream_listener)

        print "Starting filter on: ", self.tracking
        stream.filter(track=self.tracking)

    def add_client(self, user):
        """Increments the number of clients."""
        self.clients.append(user)

    def remove_client(self, user):
        """Decrements the number of clients. Kills self if the count is below 1."""
        self.clients.remove(user)

        if len(self.clients) < 1:
            print "Producer client size is now 0. Killing: channel-", self.channel
            self.kill()


class DebugStreamProducer(StreamProducer):

    def _run(self):

        # Get redis instance
        r = redis.Redis()

        # Publish data forever
        while True:
            time.sleep(2)
            r.publish(self.channel, json.dumps({'text': 'This is a tweet.', 'user_image_url': '/static/img/raspberry-pi.png'}))


def create_producer(producers):
    """Creates a new Producer stream for the terms specified in tracking."""

    # Get user's tracking terms and username
    tracking = session['tracking']
    terms = frozenset(tracking)
    user = session['identity']

    # Remove this client from other streams
    for p_terms, producer in producers.iteritems():
        if user in producer.clients:
            if producer.tracking is not tracking:
                producer.remove_client(user)

    # Create a new producer if it doesn't exist or it has been killed.
    if terms not in producers or producers[terms].value:
        # Create a Twitter stream Producer (that filters on the term 'tracking')
        feed_producer = StreamProducer(tracking)
        feed_producer.start()
        producers[terms] = feed_producer

    # Add this user to the client list
    producers[terms].add_client(user)