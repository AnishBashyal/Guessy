#importing socketio from events instead of extensions to load the object with all events
from guessapp.main.extensions import socketio

@socketio.on("connect")
def handle_connect():
    print("Client connected")