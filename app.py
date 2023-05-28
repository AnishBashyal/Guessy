from guessapp import create_app, socketio

app = create_app()

socketio.run(app, debug=True)