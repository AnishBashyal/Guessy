import secrets
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

room = Blueprint("room", __name__)

room_data = {}

@room.route("/view_room")
def view_room():
    room_code = session.get("room_code")
    name = session.get("name")
    if not name or not room_code or room_code not in room_data:
        # flash("Make sure room code is correct")
        return redirect(url_for("main.home"))
    return render_template("room.html", room_code = room_code, history_messages = room_data[room_code]["messages"])

@room.route("/create_room", methods = ["POST"])
def create_room():
    name = request.form.get("name")
    room_code = secrets.token_hex(4)
    room_data[room_code] = {
        'members' : 0,
        'messages' : []
    }
    session["name"] = name
    session["room_code"] = room_code
    print(room_data)
    return redirect(url_for("room.view_room"))

@room.route("/join_room", methods=["POST"])
def join_room():
    name = request.form.get("name")
    room_code = request.form.get("room_code")
    session["name"] = name
    session["room_code"] = room_code
    return redirect(url_for("room.view_room"))
