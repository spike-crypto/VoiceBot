"""
Application entry point
"""
import os
from app import create_socketio_app

app, socketio = create_socketio_app()

if __name__ == '__main__':
    # Use PORT env var if available (for deployment), else default to 5001
    port = int(os.environ.get('PORT', 5001))
    
    app.logger.info(f"Starting server on port {port}")
    # Use threading mode (already configured in __init__.py)
    socketio.run(app, debug=False, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
