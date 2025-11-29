"""
Flask application factory and initialization
"""
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from app.config import Config
from app.utils.logger import setup_logging
from app.middleware.error_handler import register_error_handlers
from app.routes.api import api_bp
# Export socketio for use in run.py
__all__ = ['create_app', 'create_socketio_app', 'socketio_instance']

# Initialize extensions
cors = CORS()
# Use threading mode instead of eventlet for Python 3.12 compatibility
socketio_instance = SocketIO(
    cors_allowed_origins="*",
    async_mode='threading'  # Use threading instead of eventlet for Python 3.12
)


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    cors.init_app(app)
    socketio_instance.init_app(app)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Initialize WebSocket handlers
    from app.routes.websocket import init_websocket
    init_websocket(socketio_instance)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def create_socketio_app():
    """Create app with SocketIO support"""
    app = create_app()
    return app, socketio_instance

