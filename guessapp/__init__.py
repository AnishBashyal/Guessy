import os
from flask import Flask
from flask_session import Session
from guessapp.room.events import socketio
from guessapp.main.routes import main
from guessapp.room.routes import room


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SESSION_TYPE"] = "filesystem"

    app.register_blueprint(main)
    app.register_blueprint(room)
    Session(app)
    socketio.init_app(app)
    return app