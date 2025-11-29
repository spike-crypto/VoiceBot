"""
WebSocket routes for real-time communication
"""
import logging
from flask import request
from flask_socketio import emit, join_room, leave_room
from app.services.stt_service import transcribe_audio
from app.services.llm_service import generate_response
from app.services.tts_service import text_to_speech
from app.services.session_service import get_conversation, add_message_to_session, create_session

logger = logging.getLogger(__name__)

def init_websocket(socketio_instance):
    """Initialize WebSocket handlers"""
    
    @socketio_instance.on('connect')
    def handle_connect():
        """Handle client connection"""
        logger.info(f"Client connected: {request.sid}")
        emit('connected', {'message': 'Connected to voice bot server'})
    
    @socketio_instance.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        logger.info(f"Client disconnected: {request.sid}")
    
    @socketio_instance.on('join_session')
    def handle_join_session(data):
        """Join a session room"""
        session_id = data.get('session_id')
        if session_id:
            join_room(session_id)
            emit('joined_session', {'session_id': session_id})
            logger.info(f"Client {request.sid} joined session {session_id}")
    
    @socketio_instance.on('process_voice')
    def handle_process_voice(data):
        """Process voice input via WebSocket"""
        try:
            session_id = data.get('session_id')
            audio_path = data.get('audio_path')
            
            if not audio_path:
                emit('error', {'message': 'Audio path is required'})
                return
            
            # Emit status
            emit('status', {'status': 'transcribing'})
            
            # Transcribe
            transcribed_text, _ = transcribe_audio(audio_path)
            emit('transcription', {'text': transcribed_text})
            
            # Get or create session
            if not session_id:
                session_id = create_session()
            
            conversation = get_conversation(session_id)
            if conversation:
                add_message_to_session(session_id, 'user', transcribed_text)
                conversation = get_conversation(session_id)
            
            # Generate response
            emit('status', {'status': 'generating_response'})
            response_text, metadata, _ = generate_response(
                conversation.get_messages_for_llm() if conversation else []
            )
            emit('response', {'text': response_text, 'metadata': metadata})
            
            # Add to conversation
            add_message_to_session(session_id, 'assistant', response_text)
            
            # Generate TTS
            emit('status', {'status': 'generating_speech'})
            audio_path, _ = text_to_speech(response_text)
            emit('audio_ready', {'audio_path': audio_path})
            
            emit('status', {'status': 'complete'})
            
        except Exception as e:
            logger.error(f"WebSocket process error: {str(e)}", exc_info=True)
            emit('error', {'message': str(e)})

