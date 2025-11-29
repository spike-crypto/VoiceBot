"""
Fixed backend runner that forces correct configuration
"""
import os
import sys

# FORCE CONFIGURATION BEFORE IMPORTING APP
os.environ['GROQ_MODEL'] = 'llama-3.3-70b-versatile'
print(f"DEBUG: Forced GROQ_MODEL to {os.environ['GROQ_MODEL']}")

from app import create_socketio_app

app, socketio = create_socketio_app()

# DOUBLE CHECK CONFIG
app.config['GROQ_MODEL'] = 'llama-3.3-70b-versatile'
print(f"DEBUG: App config GROQ_MODEL is {app.config['GROQ_MODEL']}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.logger.info(f"Starting server on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=debug, allow_unsafe_werkzeug=True)
