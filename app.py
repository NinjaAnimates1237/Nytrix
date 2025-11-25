from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
import os

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__, static_folder='client/dist', static_url_path='')
    app.config.from_object('config.Config')
    
    # Disable strict slashes to allow both /api/auth/me and /api/auth/me/
    app.url_map.strict_slashes = False
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    socketio.init_app(app, cors_allowed_origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.friends import friends_bp
    from routes.messages import messages_bp
    from routes.channels import channels_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(friends_bp, url_prefix='/api/friends')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(channels_bp, url_prefix='/api/channels')
    
    # Health check
    @app.route('/api/health')
    def health():
        return {'status': 'ok'}, 200
    
    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
