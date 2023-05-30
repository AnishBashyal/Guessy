#importing socketio from events instead of extensions to load the object with all events
from flask import request, session, flash, redirect, url_for
from guessapp.room.extensions import socketio
from guessapp.room.routes import room_data
from flask_socketio import send, join_room, leave_room


@socketio.on("connect")
def handle_connect():
    room_code = session.get("room_code")
    name = session.get("name")

    join_room(room_code)
    room_data[room_code]["members"]+=1
    message = {
        "name" : name,
        "body" : "has joined the chat"
    }
    send(message, to = room_code)
    print("Client connected", request.sid)

@socketio.on("disconnect")
def handle_connect():
    room_code = session.get("room_code")
    name = session.get("name")
    
    leave_room(room_code)
    room_data[room_code]["members"]-=1
    if room_data[room_code]["members"] == 0:
        del room_data[room_code]
    message = {
        "name" : name,
        "body" : "has left the chat"
    }
    send(message, to = room_code)
    print("Client disconnected", request.sid)


@socketio.on("message")
def handle_message(data):
    room_code = session.get("room_code")
    name = session.get("name")
    message = {
        "name" : name ,
        "body": data["data"]
    }
    room_data[room_code]["messages"].append(message)
    print("Message received " , message)
    send(message, to=room_code )