"""
Caching utilities
"""
import hashlib
import json
import logging
from typing import Optional, Any
from flask import current_app

logger = logging.getLogger(__name__)

# In-memory cache for development (fallback when Redis is not available)
_memory_cache = {}


def get_cache_key(prefix: str, *args) -> str:
    """Generate a cache key from prefix and arguments"""
    key_string = f"{prefix}:{':'.join(str(arg) for arg in args)}"
    return hashlib.md5(key_string.encode()).hexdigest()


def get_cache(key: str) -> Optional[Any]:
    """Get value from cache"""
    if not current_app.config.get('ENABLE_CACHING', True):
        return None
    
    try:
        if current_app.config.get('REDIS_ENABLED'):
            import redis
            redis_client = redis.from_url(current_app.config['REDIS_URL'])
            cached = redis_client.get(key)
            if cached:
                return json.loads(cached)
        else:
            # Use in-memory cache
            if key in _memory_cache:
                return _memory_cache[key]
    except Exception as e:
        logger.warning(f"Cache get error: {str(e)}")
    
    return None


def set_cache(key: str, value: Any, ttl: Optional[int] = None):
    """Set value in cache"""
    if not current_app.config.get('ENABLE_CACHING', True):
        return
    
    ttl = ttl or current_app.config.get('CACHE_TTL', 3600)
    
    try:
        if current_app.config.get('REDIS_ENABLED'):
            import redis
            redis_client = redis.from_url(current_app.config['REDIS_URL'])
            redis_client.setex(key, ttl, json.dumps(value))
        else:
            # Use in-memory cache (no TTL support)
            _memory_cache[key] = value
    except Exception as e:
        logger.warning(f"Cache set error: {str(e)}")


def delete_cache(key: str):
    """Delete value from cache"""
    try:
        if current_app.config.get('REDIS_ENABLED'):
            import redis
            redis_client = redis.from_url(current_app.config['REDIS_URL'])
            redis_client.delete(key)
        else:
            _memory_cache.pop(key, None)
    except Exception as e:
        logger.warning(f"Cache delete error: {str(e)}")

