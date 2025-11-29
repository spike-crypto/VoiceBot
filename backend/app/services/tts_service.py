import logging
import os
import uuid
import requests
from typing import Tuple
from flask import current_app
from app.utils.cache import get_cache, set_cache, get_cache_key

logger = logging.getLogger(__name__)


def text_to_speech(text: str, use_cache: bool = True) -> Tuple[str, bool]:
    """
    Convert text to speech audio file using ElevenLabs ONLY
    
    Args:
        text: Text to convert to speech
        use_cache: Whether to use caching
    
    Returns:
        Tuple of (audio_file_path, cache_hit)
    """
    cache_hit = False

    # Try to get from cache
    if use_cache:
        cache_key = get_cache_key('tts', text)
        cached_path = get_cache(cache_key)
        if cached_path:
            # Normalize cached path to absolute if needed
            try:
                if not os.path.isabs(cached_path):
                    possible = []
                    # app/uploads
                    possible.append(os.path.join(current_app.root_path, cached_path))
                    # backend/uploads (one level up)
                    parent = os.path.abspath(os.path.join(current_app.root_path, '..'))
                    possible.append(os.path.join(parent, cached_path))
                    # cwd relative
                    possible.append(os.path.join(os.getcwd(), cached_path))
                    found = None
                    for p in possible:
                        if os.path.exists(p):
                            found = p
                            break
                    if found:
                        cached_path = found
            except Exception:
                pass
            if os.path.exists(cached_path):
                logger.info("Cache hit for TTS")
                return cached_path, True
            else:
                logger.info(f"Cached TTS path not found, will regenerate: {cached_path}")

    try:
        # Clean text for TTS (remove markdown)
        clean_text = text.replace('**', '').replace('*', '').replace('__', '').replace('`', '')
        logger.info(f"Converting text to speech: '{clean_text[:50]}...'")

        # Get all available API keys
        primary_key = current_app.config.get('ELEVENLABS_API_KEY')
        backup_key_1 = current_app.config.get('ELEVENLABS_API_KEY_BACKUP_1')
        backup_key_2 = current_app.config.get('ELEVENLABS_API_KEY_BACKUP_2')
        
        # Build list of keys to try
        api_keys = []
        if primary_key:
            api_keys.append(('primary', primary_key))
        if backup_key_1:
            api_keys.append(('backup_1', backup_key_1))
        if backup_key_2:
            api_keys.append(('backup_2', backup_key_2))
        
        if not api_keys:
            raise ValueError("No ELEVENLABS_API_KEY configured. Cannot generate speech.")
        
        voice_id = current_app.config.get('ELEVENLABS_VOICE_ID', 'ErXwobaYiN019PkySvjV')
        upload_rel = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        upload_folder = os.path.join(current_app.root_path, upload_rel)
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(upload_folder, filename)
        audio_path = os.path.abspath(audio_path)
        url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream'
        
        last_error = None
        
        # Try each API key in order
        for key_name, api_key in api_keys:
            try:
                logger.info(f"Attempting TTS with {key_name} key...")
                headers = {
                    'xi-api-key': api_key,
                    'Accept': 'audio/mpeg',
                    'Content-Type': 'application/json'
                }
                payload = {'text': clean_text}
                resp = requests.post(url, headers=headers, json=payload, stream=True, timeout=120)
                
                # Check for quota/rate limit errors
                if resp.status_code == 429:
                    logger.warning(f"{key_name} key hit quota limit (429), trying next key...")
                    last_error = f"{key_name}: Quota exceeded (429)"
                    continue
                elif resp.status_code == 401:
                    logger.warning(f"{key_name} key is invalid (401), trying next key...")
                    last_error = f"{key_name}: Invalid API key (401)"
                    continue
                elif resp.status_code != 200:
                    logger.warning(f"{key_name} key failed with {resp.status_code}: {resp.text[:200]}")
                    last_error = f"{key_name}: {resp.status_code} {resp.text[:200]}"
                    continue
                
                # Success! Write the audio file
                with open(audio_path, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
                    logger.warning(f"{key_name} produced no audio, trying next key...")
                    last_error = f"{key_name}: No audio produced"
                    continue
                
                # Success!
                logger.info(f"TTS successful with {key_name} key: {audio_path}")
                if use_cache:
                    cache_key = get_cache_key('tts', text)
                    set_cache(cache_key, audio_path, ttl=3600)
                return audio_path, cache_hit
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"{key_name} key request failed: {str(e)}, trying next key...")
                last_error = f"{key_name}: {str(e)}"
                continue
        
        # If we get here, all keys failed
        raise Exception(f"All ElevenLabs API keys failed. Last error: {last_error}")
        
    except Exception as e:
        logger.error(f"TTS error: {str(e)}", exc_info=True)
        raise Exception(f"Failed to convert text to speech: {str(e)}")

