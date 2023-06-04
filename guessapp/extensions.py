from flask_socketio import SocketIO
from flask_session import Session

sess = Session()
socketio = SocketIO(manage_session=False)