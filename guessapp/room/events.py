#importing socketio from events instead of extensions to load the object with all events
from flask import request, session
from guessapp.room.extensions import socketio
from guessapp.room.routes import room_data
from flask_socketio import send, emit, join_room, leave_room

users = []
#GAME ARENA
@socketio.on("connect", namespace="/game")
def handle_game_connect(auth):
    room_code = session.get("room_code")
    name = session.get("name")
    join_room(room_code)

    if not users:
        emit("turn", to=request.sid, namespace = "/game")
    users.append({request.sid : name})
    print(users)
    message = {
        "name" : name,
        "message" : "has joined the game"
    }
    send(message, to = room_code, namespace = "/game")
    print("Player connected", request.sid)


@socketio.on("disconnect", namespace="/game")
def handle_game_disconnect():
    if request.sid == next(iter(users[0])) and len(users) > 1:
        emit("turn", to= next(iter(users[1])), namespace = "/game")
    users[:] = [user for user in users if request.sid not in user]  
    room_code = session.get("room_code")
    name = session.get("name")
    
    leave_room(room_code)
    message = {
        "name" : name,
        "message" : "has left the game"
    }
    send(message, to = room_code, namespace = "/game")
    print("Player disconnected", request.sid)


@socketio.on("message", namespace="/game")
def handle_game_message(data):
    room_code = session.get("room_code")
    name = session.get("name")
    message = {
        "name" : name ,
        "message": data["data"]
    }
    print("Message received " , message)
    if request.sid not in users[-1]:
        if secret_word == data["data"]:
            message["message"] = secret_word
            emit("wordGuessed", message, to=room_code, namespace="/game")
            emit("turn", to=request.sid, namespace = "/game")
        else:
            send(message, to=room_code, namespace = "/game" )
    else:
        emit("alert", {"message": "You cannot guess your own word"}, to=request.sid, namespace = "/game")


@socketio.on("wordSet", namespace="/game")
def handle_game_word_set(data):
    room_code = session.get("room_code")
    name = session.get("name")
    current_turn = users[0]
    if request.sid in current_turn:
        global secret_word
        secret_word = data["data"]
        users.pop(0)
        users.append(current_turn)
        message = {
            "name" : name ,
            "message": data["data"]
        }
        emit("wordSet", message, to=room_code, namspace = "/game")
    else:
        emit("alert", {"message": "Not Your Turn"}, to=request.sid, namespace = "/game")


@socketio.on("wordNotGuessed", namespace="/game")
def handle_game_word_not_guessed():
    emit("turn", to=request.sid, namespace = "/game")


#############################CHAT ARENA###############################################
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
    print("Client connected", request.sid)

@socketio.on("disconnect", namespace="/chat")
def handle_chat_disconnect():
    room_code = session.get("room_code")
    name = session.get("name")
    
    leave_room(room_code)
    room_data[room_code]["members"]-=1
    if room_data[room_code]["members"] == 0:
        del room_data[room_code]
    message = {
        "name" : name,
        "message" : "has left the chat"
    }
    send(message, to = room_code, namespace = "/chat")
    print("Client disconnected", request.sid)


@socketio.on("message", namespace="/chat")
def handle_chat_message(data):
    room_code = session.get("room_code")
    name = session.get("name")
    message = {
        "name" : name ,
        "message": data["data"]
    }
    room_data[room_code]["messages"].append(message)
    print("Message received " , message)
    send(message, to=room_code, namespace = "/chat" )