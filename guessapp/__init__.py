import os
from flask import Flask

from guessapp.main.events import socketio
from guessapp.main.routes import main

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    app.register_blueprint(main)

    socketio.init_app(app)

    return app