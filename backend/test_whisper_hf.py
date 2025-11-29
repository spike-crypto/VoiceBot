"""Test script for Hugging Face Whisper (automatic-speech-recognition).

Usage:
  .\.venv\Scripts\python.exe backend\test_whisper_hf.py <audio-file>

The script loads `backend/.env` so it picks up `HUGGINGFACE_API_TOKEN` (or
`HF_TOKEN`) when run from the repo root. It prefers `huggingface_hub.InferenceClient`.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN') or os.environ.get('HF_TOKEN')
MODEL = os.environ.get('HUGGINGFACE_STT_MODEL', 'openai/whisper-large-v3')


def main():
    if not TOKEN:
        print('Error: HUGGINGFACE_API_TOKEN (or HF_TOKEN) not found in backend/.env')
        sys.exit(2)

    if len(sys.argv) < 2:
        print('Usage: python backend/test_whisper_hf.py <audio-file>')
        sys.exit(1)

    audio_path = sys.argv[1]
    if not os.path.exists(audio_path):
        print(f'Error: audio file not found: {audio_path}')
        sys.exit(3)

    try:
        from huggingface_hub import InferenceClient
    except Exception as e:
        print('Missing dependency: huggingface_hub')
        print('Install with: pip install huggingface-hub')
        print('Exception:', e)
        sys.exit(4)

    print(f'Initial model: {MODEL}')
    client = InferenceClient(api_key=TOKEN, provider="auto")

    print('Uploading audio and requesting transcription...')
    try:
        result = client.automatic_speech_recognition(audio_path, model=MODEL)
        if isinstance(result, dict):
            text = result.get('text') or result.get('transcription') or result.get('result')
            print('Transcription result (raw dict):')
            print(result)
            if text:
                print('\nDetected text:')
                print(text)
        else:
            print('Transcription result:')
            print(result)
    except Exception as e:
        import traceback
        print('Transcription request failed for model', MODEL)
        print(repr(e))
        tb = traceback.format_exc()
        print(tb)
        print('No other fallbacks. Please check your HF token or model access.')
        sys.exit(5)


if __name__ == '__main__':
    main()
