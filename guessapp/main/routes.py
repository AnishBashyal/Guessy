from flask import Blueprint, render_template, session

main = Blueprint("main", __name__)

@main.route("/")
def home():
    session.clear()
    return render_template("home.html")

