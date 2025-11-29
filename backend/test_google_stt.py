"""
Test script for Google Speech-to-Text using backend transcribe_audio.
Usage:
  python backend/test_google_stt.py <audio-file>

Requires: GOOGLE_API_KEY in backend/.env and STT_PROVIDER=google
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

if len(sys.argv) < 2:
    print('Usage: python backend/test_google_stt.py <audio-file>')
    sys.exit(1)

AUDIO_PATH = sys.argv[1]
if not os.path.exists(AUDIO_PATH):
    print(f'Error: audio file not found: {AUDIO_PATH}')
    sys.exit(2)

import flask
from app.services.stt_service import transcribe_audio

app = flask.Flask(__name__)
app.config['STT_PROVIDER'] = os.environ.get('STT_PROVIDER', 'google')
app.config['GOOGLE_API_KEY'] = os.environ.get('GOOGLE_API_KEY')

with app.app_context():
    print(f"Testing Google Speech-to-Text on: {AUDIO_PATH}")
    try:
        text, cache_hit = transcribe_audio(AUDIO_PATH, use_cache=False)
        print("\nTranscribed text:")
        print(text)
    except Exception as e:
        print("Error during transcription:", e)
        sys.exit(3)
