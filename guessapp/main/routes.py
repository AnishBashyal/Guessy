from flask import Blueprint, render_template, session, flash

main = Blueprint("main", __name__)

@main.route("/")
def home():
    name = session.get("name") if session.get("name") else ""   
    return render_template("home.html", page="home", name=name)

