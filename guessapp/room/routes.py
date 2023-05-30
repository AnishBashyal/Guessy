from flask import Blueprint, render_template, request, redirect, url_for, session

room = Blueprint("room", __name__)

@room.route("/arena", methods = ["GET", "POST"])
def arena():
    return render_template("arena.html")