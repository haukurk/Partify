# coding=utf-8
__version__ = 0.1
version = __version__

import random
import config

from flask import Flask, render_template, request, session
from flask.ext.socketio import SocketIO, emit
from flask.ext.socketio import request as requests_io
from partify.modules.twitter import streams
import core

# Start the Flask awesomeness.
app = Flask(__name__, static_folder=config.STATIC_FOLDER_DEV, static_url_path='/static')

# Setup Config
app.config.from_object('config')

# SocketIO
socketio = SocketIO(app)

# Background thread
thread = None

# # Api routing
# Example Weather Route
from modules.twitter.routes import mod as twitter_module

app.register_blueprint(twitter_module)

# Globals used to keep track of Consumer/Producer services
producers = {}   # Stores each Producer service
consumers = {}   # Stores each user's Consumer service
namespaces = {}	 # Stores a list of each user's namespace (used for the socket location)

"""
App global
"""


@app.before_request
def setup():
    """Adds a username to the session object to identify the client."""
    session['identity'] = request.remote_addr + "-" + str(
        random.randint(0, 100))  # Small hack to be able to open two streams on the same IP.
    print "New Client. IP:", request.remote_addr, "with identity", session['identity']


"""
Routes that does not matter.
"""


@app.route('/', methods=['GET', 'OPTIONS', 'POST'])
def partify():
    """
    Main Route for Partify.
    """

    return render_template('index.html', version=version)


## Socket IO routes


def msg_generator(search):
    """
    Example of how to send server generated events to clients.
    Useful to use threading.
    """
    count = 0
    print("Streaming thread active.")

    def msgtwitter(data):
        socketio.emit('twitter response',
                      {'data': data},
                      namespace='/stream')

    streams.start([search], msgtwitter)


@socketio.on('start-stream', namespace='/stream')
def on_start_stream(message):
    print message
    emit('status', {'tracking': message})

    print 'Starting stream for', requests_io.namespace.socket.sessid
    tracking = message
    session['tracking'] = message[u"tracking"]

    core.create_producer(producers)
    core.create_consumer(consumers, namespaces)


@socketio.on('connect', namespace='/stream')
def on_connect():
    # Let the client know that we are connected
    emit('status', {'data': 'Connected'})

    print '[Socket Connected] Session', requests_io.namespace.socket.sessid
    namespaces[session['identity']] = request.namespace  # Used by socketio.

@socketio.on('disconnect', namespace='/stream')
def on_disconnect():
    print '[Socket DISCONNECTED] Session', requests_io.namespace.socket.sessid
    core.kill_stream(consumers, producers)
