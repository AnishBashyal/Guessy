#importing socketio from events instead of extensions to load the object with all events
from flask import request
from guessapp.room.extensions import socketio

@socketio.on("connect")
def handle_connect():
    print("Client connected", request.sid)