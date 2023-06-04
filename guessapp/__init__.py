from flask import Flask
from guessapp.room.game_events import socketio
from guessapp.extensions import sess
from guessapp.config import Config
from guessapp.main.routes import main
from guessapp.room.routes import room


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    sess.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(room)


    return app