"""
Session management service
"""
import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional
from flask import current_app
from app.models import Conversation, Message
from app.utils.cache import get_cache, set_cache, delete_cache

logger = logging.getLogger(__name__)


def create_session() -> str:
    """Create a new session and return session ID"""
    session_id = str(uuid.uuid4())
    conversation = Conversation(session_id=session_id)
    
    # System message will be added by LLM service, not stored in conversation
    
    # Store in cache
    _save_conversation(conversation)
    
    logger.info(f"Created new session: {session_id}")
    return session_id


def get_conversation(session_id: str) -> Optional[Conversation]:
    """Get conversation by session ID"""
    try:
        cache_key = f"session:{session_id}"
        cached_data = get_cache(cache_key)
        
        if cached_data:
            return Conversation.from_dict(cached_data)
        
        return None
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}")
        return None


def save_conversation(conversation: Conversation):
    """Save conversation to storage"""
    _save_conversation(conversation)


def _save_conversation(conversation: Conversation):
    """Internal method to save conversation"""
    cache_key = f"session:{conversation.session_id}"
    conversation_dict = conversation.to_dict()
    
    # Set cache with session timeout
    timeout = current_app.config.get('SESSION_TIMEOUT', 3600)
    set_cache(cache_key, conversation_dict, ttl=timeout)


def delete_session(session_id: str):
    """Delete a session"""
    cache_key = f"session:{session_id}"
    delete_cache(cache_key)
    logger.info(f"Deleted session: {session_id}")


def add_message_to_session(session_id: str, role: str, content: str):
    """Add a message to a session"""
    conversation = get_conversation(session_id)
    
    if not conversation:
        logger.warning(f"Session not found: {session_id}, creating new session")
        conversation = Conversation(session_id=session_id)
    
    message = Message(role=role, content=content)
    conversation.add_message(message)
    save_conversation(conversation)
    
    return conversation

