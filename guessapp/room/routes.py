import secrets
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

room = Blueprint("room", __name__)

room_data, users_data, scores_data = {}, {}, {}
@room.route("/view_room")
def view_room():
    room_code = session.get("room_code")
    name = session.get("name")
    score = session.get("score")
   
   
    if None in (name, room_code, score) or any(room_code not in data for data in (room_data, users_data, scores_data)):
        flash("Unable to enter room!", "danger")
        return redirect(url_for("main.home"))
    
    
    return render_template("room.html", page="room", room_code = room_code, history_messages = room_data[room_code]["messages"])

@room.route("/create_room", methods = ["POST"])
def create_room():
    name = request.form.get("name")
    if len(name) > 8:
        flash("Choose a number under 8 characters!", "danger")
        return redirect(url_for("main.home"))
    room_code = secrets.token_hex(4)
    room_data[room_code] = {
        'members' : 0,
        'messages' : []
    }
    users_data[room_code] = []
    scores_data[room_code] = {}
    session["name"] = name
    session["room_code"] = room_code
    session["score"] = 0
    # print(room_data)
    return redirect(url_for("room.view_room"))

@room.route("/join_room", methods=["POST"])
def join_room():
    name = request.form.get("name")
    if len(name) > 8:
        flash("Choose a number under 8 characters!", "danger")
        return redirect(url_for("main.home"))
    room_code = request.form.get("room_code")
    session["name"] = name
    session["room_code"] = room_code
    session["score"] = 0
    return redirect(url_for("room.view_room"))
