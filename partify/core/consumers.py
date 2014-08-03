__author__ = 'haukurk'

from flask import session
import json
import gevent
import redis
import config


class StreamConsumer(gevent.Greenlet):
    """Consumes items from a redis pubsub channel."""

    def __init__(self, channel, emit):
        """Subscribes to the specified pubsub channel."""

        print "Creating a Consumer: channel-", channel

        # Subscribe to the specified channel
        if config.REDIS_AUTH is True:
            r = redis.Redis(host=config.REDIS_IP, port=config.REDIS_PORT, password=config.REDIS_PASSWORD)
        else:
            r = redis.Redis(host=config.REDIS_IP, port=config.REDIS_PORT)

        self._pubsub = r.pubsub()
        self._pubsub.subscribe(channel)

        # Store the emit function (used to pass data to a socket.io client)
        self._emit = emit

        # Store channel
        self.channel = channel

        # Call Greenlet constructor
        super(StreamConsumer, self).__init__()

    def _run(self):
        """Listens to the pubsub channel and emits data."""

        for item in self._pubsub.listen():

            # NOTE: assumes the socketio channel has the same name as the
            # redis pubsub channel.

            if type(item['data']) is long:
                continue

            self._emit('stream-data-twitter', {'data': json.loads(item['data'])})

    def kill(self):
        print "Killing a Consumer: channel-", self.channel
        super(StreamConsumer, self).kill()


def create_consumer(consumers, namespaces):
    """Creates a new redis pub/sub consumer that subscribes to correct channel."""

    # Get user information
    tracking = session['tracking']
    username = session['identity']
    emit = namespaces[username].emit

    # Kill previous consumer (each user only gets one instance)
    if username in consumers:
        consumers[username].kill()

    # Create new Consumer
    channel = json.dumps(sorted(tracking))
    feed_consumer = StreamConsumer(channel, emit)
    feed_consumer.start()
    consumers[username] = feed_consumer