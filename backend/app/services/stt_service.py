"""
Speech-to-Text service using ElevenLabs Scribe
"""
import logging
import requests
import os
from typing import Optional, Tuple
from flask import current_app
from app.utils.cache import get_cache, set_cache, get_cache_key

logger = logging.getLogger(__name__)






def transcribe_audio(audio_path: str, use_cache: bool = True) -> Tuple[str, bool]:
    """
    Transcribe audio file to text using ElevenLabs Scribe ONLY
    
    Args:
        audio_path: Path to audio file
        use_cache: Whether to use caching
    
    Returns:
        Tuple of (transcribed_text, cache_hit)
    """
    cache_hit = False
    
    # Try to get from cache
    if use_cache:
        cache_key = get_cache_key('stt', audio_path)
        cached_result = get_cache(cache_key)
        if cached_result:
            logger.info(f"Cache hit for transcription: {audio_path}")
            return cached_result, True
    
    try:
        # STRICTLY ELEVENLABS ONLY
        logger.info("Using ElevenLabs Scribe for STT")
        api_key = current_app.config.get('ELEVENLABS_API_KEY')
        if not api_key:
             raise ValueError("ELEVENLABS_API_KEY is missing. Cannot transcribe.")

        model_id = current_app.config.get('ELEVENLABS_STT_MODEL', 'scribe_v1')
        url = 'https://api.elevenlabs.io/v1/speech-to-text'
        
        headers = {
            'xi-api-key': api_key
        }
        
        # Open file and send request
        with open(audio_path, 'rb') as fh:
            files = {'file': (os.path.basename(audio_path), fh, 'audio/wav')}
            data = {'model_id': model_id}
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)
        
        if resp.status_code != 200:
            raise Exception(f'ElevenLabs STT failed: {resp.status_code} {resp.text}')
        
        j = resp.json()
        if 'text' in j:
            transcribed_text = j['text'].strip()
        else:
            # Fallback if response structure is different
            transcribed_text = str(j)
        
        # Cache the result
        if use_cache and transcribed_text:
            cache_key = get_cache_key('stt', audio_path)
            set_cache(cache_key, transcribed_text, ttl=3600)
        
        logger.info(f"Transcription completed: '{transcribed_text[:50]}...'")
        return transcribed_text, cache_hit
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}", exc_info=True)
        raise Exception(f"Failed to transcribe audio: {str(e)}")

