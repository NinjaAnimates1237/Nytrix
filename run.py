from dotenv import load_dotenv
load_dotenv()

from app import create_app, socketio
import socket_events  # Import to register socket handlers

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=6767, allow_unsafe_werkzeug=True)
