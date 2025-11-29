"""End-to-end test: ElevenLabs TTS -> POST to /api/process

Saves TTS output from /api/tts then uploads it to /api/process and prints the JSON response.
Requires backend server running on http://localhost:5000 and backend .env configured.
"""
import os
import requests
from pathlib import Path

BASE = os.environ.get('API_BASE', 'http://localhost:5000')
UPLOADS = Path('uploads')
UPLOADS.mkdir(exist_ok=True)

def get_tts(text='Hello, this is an end-to-end test.'):
    url = f'{BASE}/api/tts'
    try:
        resp = requests.post(url, json={'text': text}, timeout=60)
        if resp.status_code == 200:
            filename = UPLOADS / 'e2e_tts.mp3'
            with open(filename, 'wb') as f:
                f.write(resp.content)
            print(f'Wrote TTS audio to {filename}')
            return filename
        else:
            print(f'TTS endpoint returned {resp.status_code}: {resp.text[:200]}')
            return None
    except Exception as e:
        print('TTS request failed:', e)
        return None


def post_process(audio_path):
    url = f'{BASE}/api/process'
    files = {'audio': (audio_path.name, open(audio_path, 'rb'), 'audio/mpeg')}
    try:
        resp = requests.post(url, files=files, timeout=180)
        try:
            print('Process response status:', resp.status_code)
            print('Response JSON:', resp.json())
        except Exception:
            print('Response text:', resp.text[:1000])
    except Exception as e:
        print('Process request failed:', e)


if __name__ == '__main__':
    tts_file = get_tts()
    if tts_file:
        post_process(tts_file)
