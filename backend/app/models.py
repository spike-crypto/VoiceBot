"""
Data models for the application
"""
from datetime import datetime
from typing import List, Dict, Optional
import json


class Message:
    """Represents a single message in a conversation"""
    
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        self.role = role  # 'user', 'assistant', or 'system'
        self.content = content
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert message to dictionary"""
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        """Create message from dictionary"""
        timestamp = datetime.fromisoformat(data['timestamp']) if 'timestamp' in data else None
        return cls(
            role=data['role'],
            content=data['content'],
            timestamp=timestamp
        )


class Conversation:
    """Represents a conversation session"""
    
    def __init__(self, session_id: str, created_at: Optional[datetime] = None):
        self.session_id = session_id
        self.messages: List[Message] = []
        self.created_at = created_at or datetime.now()
        self.updated_at = datetime.now()
        self.metadata: Dict = {}
    
    def add_message(self, message: Message):
        """Add a message to the conversation"""
        self.messages.append(message)
        self.updated_at = datetime.now()
    
    def get_messages_for_llm(self) -> List[Dict]:
        """Get messages in format suitable for LLM API"""
        return [msg.to_dict() for msg in self.messages]
    
    def to_dict(self) -> Dict:
        """Convert conversation to dictionary"""
        return {
            'session_id': self.session_id,
            'messages': [msg.to_dict() for msg in self.messages],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Conversation':
        """Create conversation from dictionary"""
        conv = cls(
            session_id=data['session_id'],
            created_at=datetime.fromisoformat(data['created_at'])
        )
        conv.messages = [Message.from_dict(msg) for msg in data.get('messages', [])]
        conv.updated_at = datetime.fromisoformat(data['updated_at'])
        conv.metadata = data.get('metadata', {})
        return conv


class ProcessingMetrics:
    """Tracks processing metrics for analytics"""
    
    def __init__(self):
        self.transcription_time: float = 0.0
        self.llm_time: float = 0.0
        self.tts_time: float = 0.0
        self.total_time: float = 0.0
        self.tokens_used: int = 0
        self.cache_hit: bool = False
    
    def to_dict(self) -> Dict:
        """Convert metrics to dictionary"""
        return {
            'transcription_time': self.transcription_time,
            'llm_time': self.llm_time,
            'tts_time': self.tts_time,
            'total_time': self.total_time,
            'tokens_used': self.tokens_used,
            'cache_hit': self.cache_hit
        }

