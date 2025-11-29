"""
REST API routes
"""
import os
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from app.services.llm_service import generate_response
from app.services.tts_service import text_to_speech
from app.services.session_service import (
    create_session, get_conversation, add_message_to_session, delete_session
)
from app.middleware.rate_limit import rate_limit
from app.utils.validators import validate_audio_file, validate_session_id, sanitize_text
from app.models import ProcessingMetrics

logger = logging.getLogger(__name__)

# Helper function to get config safely  
def get_upload_folder():
    """Get upload folder from config, with fallback"""
    # Default fallback
    default_folder = 'uploads'
    
    try:
        # Try to access current_app - it should be available in Flask route handlers
        # Use has_request_context to ensure we're in a request context
        from flask import has_request_context
        if has_request_context():
            try:
                folder = current_app.config.get('UPLOAD_FOLDER', default_folder)
                # Return absolute path under app root for consistency
                try:
                    return os.path.join(current_app.root_path, folder)
                except Exception:
                    return folder
            except RuntimeError as e:
                # current_app not available in this context
                logger.debug(f"current_app not in context, using default: {e}")
                return default_folder
        else:
            return default_folder
    except Exception as e:
        # Any other error, use default
        logger.warning(f"Error getting upload folder from config: {e}, using default")
        return default_folder

api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'voice-bot-api'
    }), 200


@api_bp.route('/session', methods=['POST'])
def create_new_session():
    """Create a new conversation session"""
    try:
        session_id = create_session()
        return jsonify({
            'session_id': session_id,
            'message': 'Session created successfully'
        }), 201
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500




@api_bp.route('/chat', methods=['POST'])
@rate_limit(per_minute=30, per_hour=100)
def chat():
    """Generate chat response from text"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = sanitize_text(data['text'])
        session_id = data.get('session_id')
        
        # Get or create session
        if session_id:
            is_valid, error_msg = validate_session_id(session_id)
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            conversation = get_conversation(session_id)
        else:
            session_id = create_session()
            conversation = get_conversation(session_id)
        
        if not conversation:
            return jsonify({'error': 'Session not found'}), 404
        
        # Add user message
        add_message_to_session(session_id, 'user', text)
        conversation = get_conversation(session_id)
        
        # Generate response
        start_time = datetime.now()
        print(f"DEBUG: About to call generate_response")
        response_text, metadata, cache_hit = generate_response(
            conversation.get_messages_for_llm()
        )
        llm_time = (datetime.now() - start_time).total_seconds()
        
        # Add assistant message
        add_message_to_session(session_id, 'assistant', response_text)
        
        return jsonify({
            'response': response_text,
            'session_id': session_id,
            'cache_hit': cache_hit,
            'llm_time': llm_time,
            'metadata': metadata
        }), 200
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@api_bp.route('/tts', methods=['POST'])
@rate_limit(per_minute=30, per_hour=100)
def tts():
    """Convert text to speech"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = sanitize_text(data['text'])
        
        # Generate speech (force regeneration to avoid stale cached paths)
        start_time = datetime.now()
        audio_path, cache_hit = text_to_speech(text, use_cache=False)
        tts_time = (datetime.now() - start_time).total_seconds()
        
        # Normalize audio_path if relative: check common locations
        if not os.path.isabs(audio_path):
            candidates = [
                os.path.join(current_app.root_path, audio_path),
                os.path.join(current_app.root_path, current_app.config.get('UPLOAD_FOLDER', 'uploads'), os.path.basename(audio_path)),
                os.path.join(os.getcwd(), audio_path),
                os.path.join(os.getcwd(), 'uploads', os.path.basename(audio_path))
            ]
            found = None
            for c in candidates:
                if os.path.exists(c):
                    found = c
                    break
            if found:
                audio_path = found

        # Debug: ensure file exists before sending
        if not os.path.exists(audio_path):
            upload_folder = get_upload_folder()
            try:
                files = os.listdir(upload_folder)
            except Exception as ex:
                files = [f'Could not list {upload_folder}: {ex}']
            logger.error(f"TTS produced path but file missing: {audio_path}. Upload folder contents: {files}")
            return jsonify({'error': f"TTS file not found: {audio_path}", 'upload_folder': upload_folder, 'contents': files}), 500
        
        return send_file(
            audio_path,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='response.mp3'
        ), 200
        
    except Exception as e:
        logger.error(f"TTS error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500




@api_bp.route('/conversation/<session_id>', methods=['GET'])
def get_conversation_history(session_id):
    """Get conversation history"""
    try:
        is_valid, error_msg = validate_session_id(session_id)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        conversation = get_conversation(session_id)
        
        if not conversation:
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify(conversation.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Get conversation error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@api_bp.route('/conversation/<session_id>', methods=['DELETE'])
def clear_conversation(session_id):
    """Clear conversation history"""
    try:
        is_valid, error_msg = validate_session_id(session_id)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        delete_session(session_id)
        
        return jsonify({'message': 'Conversation cleared successfully'}), 200
        
    except Exception as e:
        logger.error(f"Clear conversation error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@api_bp.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    """Serve audio files"""
    try:
        # Audio files are stored in temp directory or uploads
        import tempfile
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, filename)
        
        # Also check uploads folder
        if not os.path.exists(filepath):
            upload_folder = get_upload_folder()
            filepath = os.path.join(upload_folder, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Audio file not found'}), 404
        
        return send_file(filepath, mimetype='audio/mpeg')
    except Exception as e:
        logger.error(f"Get audio error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

