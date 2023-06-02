from flask import session
from guessapp.room.extensions import socketio
from guessapp.room.routes import room_data, scores_data, users_data
from flask_socketio import send, join_room, leave_room

@socketio.on("connect", namespace="/chat")
def handle_chat_connect(auth):
    room_code = session.get("room_code")
    name = session.get("name")
    join_room(room_code)
    room_data[room_code]["members"]+=1 

    message = {
        "name" : name,
        "message" : "has joined the chat"
    }
    send(message, to = room_code, namespace = "/chat")
    # print("Client connected", request.sid)

@socketio.on("disconnect", namespace="/chat")
def handle_chat_disconnect():
    room_code = session.get("room_code")
    name = session.get("name")
    leave_room(room_code)
    room_data[room_code]["members"]-=1
    if room_data[room_code]["members"] == 0:
        del scores_data[room_code]
        del users_data[room_code]
        del room_data[room_code]
    message = {
        "name" : name,
        "message" : "has left the chat"
    }
    send(message, to = room_code, namespace = "/chat")
    # print("Client disconnected", request.sid)

@socketio.on("message", namespace="/chat")
def handle_chat_message(data):
    room_code = session.get("room_code")
    name = session.get("name")
    score = session.get("score")
    message = {
        "name" : name ,
        "message": data["data"]
    }
    room_data[room_code]["messages"].append(message)
    # print("SESSION VALUES", name, room_code, score, scores_data)
    # print("Message received " , message)
    send(message, to=room_code, namespace = "/chat" )