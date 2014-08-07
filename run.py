if __name__ == '__main__':
    from partify import app, socketio
    print("Starting the Development HTTP server..")
    app.debug = True
    socketio.run(app) # using gevent.