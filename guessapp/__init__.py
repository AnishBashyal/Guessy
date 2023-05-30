import os
from flask import Flask

from guessapp.room.events import socketio
from guessapp.main.routes import main
from guessapp.room.routes import room

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    app.register_blueprint(main)
    app.register_blueprint(room)

    socketio.init_app(app)

    return app