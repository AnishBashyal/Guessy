#importing socketio from events instead of extensions to load the object with all events
from flask import request, session
from guessapp.room.chat_events import socketio
from guessapp.room.routes import scores_data, users_data
from flask_socketio import send, emit, join_room, leave_room

secret_word, current_turn_sid = "", ""

def currentTurn():
    room_code = session.get("room_code")
    global secret_word, current_turn_sid
    secret_word, current_turn_sid = "", ""

    s_id, s_name = next(iter(users_data[room_code][0].items()))
    # print("CURRENT TURNRRRRR", s_name)

    emit("turn", to=s_id, namespace = "/game")
    emit("turnDecided", {"name" : s_name}, to = room_code, namespace="/game" )


@socketio.on("connect", namespace="/game")
def handle_game_connect(auth):
    room_code = session.get("room_code")
    name = session.get("name")
   
    join_room(room_code)        
    users_data[room_code].append({request.sid : name})
    scores_data[room_code][request.sid] = session.get("score")

    if len(users_data[room_code]) == 1:
       currentTurn()
    else:
        emit("turnDecided", {"name" : next(iter(users_data[room_code][0].items()))[1]}, to = request.sid, namespace="/game" )

    # print(users_data[room_code])

    message = {
        "name" : name,
        "message" : "has joined the game",
    }

    emit("setSid", {"sid":request.sid}, to=request.sid, namespace="/game")
    send(message, to = room_code, namespace = "/game")
    # print("Player connected", request.sid)
    emit("displayTable", [scores_data[room_code], users_data[room_code]], to=room_code, namespace="/game")


@socketio.on("disconnect", namespace="/game")
def handle_game_disconnect():
    room_code = session.get("room_code")
    name = session.get("name")

    deleted_user = users_data[room_code][0]
    users_data[room_code][:] = [user for user in users_data[room_code] if request.sid not in user]  
    del scores_data[room_code][request.sid]

    if users_data[room_code] and request.sid in deleted_user:
        currentTurn()
    
    leave_room(room_code)
    message = {
        "name" : name,
        "message" : "has left the game"
    }
    
    send(message, to = room_code, namespace = "/game")
    # print("Player disconnected", request.sid)
    emit("displayTable", [scores_data[room_code], users_data[room_code]], to=room_code, namespace="/game")

@socketio.on("message", namespace="/game")
def handle_game_message(data):
    global secret_word
    room_code = session.get("room_code")
    name = session.get("name")

    message = {
        "name" : name ,
        "message": data["data"]
    }
    # print("Message received " , message, name)
    if request.sid is not current_turn_sid and secret_word:
        if secret_word.lower() == data["data"].lower():
            message["message"] = secret_word
            message["winner_sid"] = request.sid
            emit("wordGuessed", message, to=room_code, namespace="/game")

            session["score"] += 1
            scores_data[room_code][request.sid] = session.get("score")

            emit("displayTable", [scores_data[room_code], users_data[room_code]], to=room_code, namespace="/game")
            currentTurn()
        else:
            send(message, to=room_code, namespace = "/game" )
    else:
        emit("alert", {"message": "You are locked for now!",  "category" : "warning"}, to=request.sid, namespace = "/game")


@socketio.on("wordSet", namespace="/game")
def handle_game_word_set(data):
    if len(data["data"]) > 10 or len(data["data"].split()) > 1:
        emit("alert", {"message": "Secret must be a single word upto 10 letters", "category":"warning"}, to=request.sid, namespace="/game")
        return
    
    global secret_word, current_turn_sid
    room_code = session.get("room_code")
    name = session.get("name")

    if not current_turn_sid and request.sid in users_data[room_code][0]:
        current_turn_sid = request.sid
        secret_word = data["data"]
        users_data[room_code].append(users_data[room_code].pop(0))
        message = {
            "name" : name ,
            "message": data["data"]
        }
        emit("wordSet", message, to=room_code, namspace = "/game")
    else:
        emit("alert", {"message": "Not Your Turn", "category" : "warning"}, to=request.sid, namespace = "/game")


@socketio.on("wordNotGuessed", namespace="/game")
def handle_game_word_not_guessed():
    currentTurn()

