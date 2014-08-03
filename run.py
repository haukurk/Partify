if __name__ == '__main__':
    from partify import app, socketio
    print("Starting the Development HTTP server..")
    socketio.run(app) # using gevent.