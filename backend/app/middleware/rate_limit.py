"""
Rate limiting middleware
"""
import time
from functools import wraps
from flask import request, jsonify, g
from app.utils.cache import get_cache, set_cache
import logging

logger = logging.getLogger(__name__)


def get_client_identifier():
    """Get unique identifier for rate limiting"""
    # Try to get session ID first
    session_id = request.headers.get('X-Session-ID')
    if session_id:
        return f"session:{session_id}"
    
    # Fall back to IP address
    return f"ip:{request.remote_addr}"


def rate_limit(per_minute: int = None, per_hour: int = None):
    """
    Rate limiting decorator
    
    Args:
        per_minute: Maximum requests per minute
        per_hour: Maximum requests per hour
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import current_app
            
            identifier = get_client_identifier()
            now = time.time()
            
            # Check per-minute limit
            if per_minute:
                minute_key = f"ratelimit:{identifier}:minute:{int(now / 60)}"
                minute_count = get_cache(minute_key) or 0
                
                if minute_count >= per_minute:
                    logger.warning(f"Rate limit exceeded (per minute) for {identifier}")
                    return jsonify({
                        'error': 'Rate Limit Exceeded',
                        'message': f'Maximum {per_minute} requests per minute allowed',
                        'retry_after': 60
                    }), 429
                
                set_cache(minute_key, minute_count + 1, ttl=60)
            
            # Check per-hour limit
            if per_hour:
                hour_key = f"ratelimit:{identifier}:hour:{int(now / 3600)}"
                hour_count = get_cache(hour_key) or 0
                
                if hour_count >= per_hour:
                    logger.warning(f"Rate limit exceeded (per hour) for {identifier}")
                    return jsonify({
                        'error': 'Rate Limit Exceeded',
                        'message': f'Maximum {per_hour} requests per hour allowed',
                        'retry_after': 3600
                    }), 429
                
                set_cache(hour_key, hour_count + 1, ttl=3600)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

