"""
Input validation utilities
"""
import os
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def validate_audio_file(file):
    """Validate uploaded audio file"""
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, f"File type not allowed. Allowed types: {', '.join(current_app.config['ALLOWED_EXTENSIONS'])}"
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    max_size = current_app.config['MAX_CONTENT_LENGTH']
    if file_size > max_size:
        return False, f"File too large. Maximum size: {max_size / (1024*1024):.1f}MB"
    
    return True, None


def validate_session_id(session_id):
    """Validate session ID format"""
    if not session_id:
        return False, "Session ID is required"
    
    if len(session_id) < 8 or len(session_id) > 64:
        return False, "Session ID must be between 8 and 64 characters"
    
    return True, None


def sanitize_text(text):
    """Sanitize user input text"""
    if not text:
        return ""
    
    # Remove potentially harmful characters
    text = text.strip()
    # Limit length
    max_length = 5000
    if len(text) > max_length:
        text = text[:max_length]
    
    return text

