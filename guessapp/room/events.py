#importing socketio from events instead of extensions to load the object with all events
from flask import request, session
from guessapp.room.extensions import socketio
from guessapp.room.routes import room_data
from flask_socketio import send, emit, join_room, leave_room

users = []
room_code, name, secret_word, current_turn_sid = "", "", "", ""

def currentTurn():
    global secret_word, current_turn_sid
    secret_word, current_turn_sid = "", ""
    s_id, s_name = next(iter(users[0].items()))
    print("CURRENT TURNRRRRR", s_name)
    emit("turn", to=s_id, namespace = "/game")
    emit("turnDecided", {"name" : s_name}, to = room_code, namespace="/game" )

#GAME ARENA
@socketio.on("connect", namespace="/game")
def handle_game_connect(auth):
    global room_code, name
    room_code = session.get("room_code")
    name = session.get("name")

    join_room(room_code)
    users.append({request.sid : name})

    if len(users) == 1:
       currentTurn()
    else:
        emit("turnDecided", {"name" : next(iter(users[0].items()))[1]}, to = request.sid, namespace="/game" )

    print(users)

    message = {
        "name" : name,
        "message" : "has joined the game"
    }
    send(message, to = room_code, namespace = "/game")
    print("Player connected", request.sid)


@socketio.on("disconnect", namespace="/game")
def handle_game_disconnect():
    deleted_user = users[0]
    users[:] = [user for user in users if request.sid not in user]  
    if users and request.sid in deleted_user:
        currentTurn()
    
    leave_room(room_code)
    message = {
        "name" : name,
        "message" : "has left the game"
    }
    send(message, to = room_code, namespace = "/game")
    print("Player disconnected", request.sid)


@socketio.on("message", namespace="/game")
def handle_game_message(data):
    global secret_word
    message = {
        "name" : name ,
        "message": data["data"]
    }
    print("Message received " , message)
    if request.sid is not current_turn_sid and secret_word:
        if secret_word.lower() == data["data"].lower():
            message["message"] = secret_word
            emit("wordGuessed", message, to=room_code, namespace="/game")
            currentTurn()
        else:
            send(message, to=room_code, namespace = "/game" )
    else:
        emit("alert", {"message": "You are locked for now!"}, to=request.sid, namespace = "/game")


@socketio.on("wordSet", namespace="/game")
def handle_game_word_set(data):
    global secret_word, current_turn_sid
    if not current_turn_sid and request.sid in users[0]:
        current_turn_sid = request.sid
        secret_word = data["data"]
        users.append(users.pop(0))
        message = {
            "name" : name ,
            "message": data["data"]
        }
        emit("wordSet", message, to=room_code, namspace = "/game")
    else:
        emit("alert", {"message": "Not Your Turn"}, to=request.sid, namespace = "/game")


@socketio.on("wordNotGuessed", namespace="/game")
def handle_game_word_not_guessed():
    currentTurn()


#############################CHAT ARENA###############################################
@socketio.on("connect", namespace="/chat")
def handle_chat_connect(auth):

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
    message = {
        "name" : name ,
        "message": data["data"]
    }
    room_data[room_code]["messages"].append(message)
    print("Message received " , message)
    send(message, to=room_code, namespace = "/chat" )