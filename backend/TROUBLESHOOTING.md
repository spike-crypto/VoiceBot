# Troubleshooting Guide

## Python 3.12 Compatibility Issue

### Problem
```
AttributeError: module 'ssl' has no attribute 'wrap_socket'
```

### Explanation
This error occurs because:
1. **Python 3.12** removed the deprecated `ssl.wrap_socket()` method
2. **eventlet** (used by Flask-SocketIO) still tries to use this deprecated method
3. **eventlet** hasn't been fully updated for Python 3.12 compatibility

### Solution Applied
We've configured Flask-SocketIO to use **threading mode** instead of **eventlet**:
- Changed `async_mode='threading'` in SocketIO initialization
- Removed `eventlet` from requirements.txt
- WebSocket functionality still works, just uses threading instead

### Alternative Solutions

#### Option 1: Use Python 3.11 (if threading doesn't work)
```bash
# Install Python 3.11
# Then create virtual environment with Python 3.11
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Option 2: Use gevent instead of eventlet
```bash
pip install gevent
# Then change async_mode to 'gevent' in __init__.py
```

#### Option 3: Disable WebSocket (if not needed)
- Remove Flask-SocketIO dependency
- Use only REST API endpoints
- Simpler setup, no async issues

## Other Common Issues

### Module Not Found Errors
```bash
# Make sure you're in the backend directory
cd backend
pip install -r requirements.txt
```

### API Key Not Found
```bash
# Create .env file
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### Port Already in Use
```bash
# Change port in run.py or set PORT environment variable
export PORT=5001  # On Windows: $env:PORT=5001
python run.py
```

### Whisper Model Download Issues
- First run downloads ~500MB model
- Requires internet connection
- May take 5-10 minutes on slow connections

## Testing the Fix

After applying the fix, test with:
```bash
cd backend
python run.py
```

You should see:
```
INFO - Voice Bot Interview Assistant - Backend Starting
INFO - Starting server on port 5000
```

If you see errors, check the logs in `backend/logs/` directory.

