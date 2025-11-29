"""Test Mistral Cloud connectivity and list available models.

Run with venv active:
  .\.venv\Scripts\python.exe backend\test_mistral_connect.py
"""
import os
from dotenv import load_dotenv
import requests

# Load backend .env so tests pick up keys when run from repo root
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

base = os.environ.get('MISTRAL_API_BASE', 'https://api.mistral.ai').rstrip('/')
api_key = os.environ.get('MISTRAL_API_KEY') or os.environ.get('Mirstal')

headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}

print(f"Mistral base: {base}")
print(f"Using API key: {'yes' if api_key else 'no'}")

endpoints = [
    f"{base}/v1/models",
    f"{base}/v1/models/list",
    f"{base}/v1/models?limit=50",
    f"{base}/v1/model/list",
]

for url in endpoints:
    try:
        print('\nGET', url)
        r = requests.get(url, headers=headers, timeout=10)
        print('Status:', r.status_code)
        try:
            print('Response JSON:', r.json())
        except Exception:
            print('Response text:', r.text[:1000])
    except Exception as e:
        print('Request failed:', e)

# Also try generate ping (no model)
try:
    gen_url = f"{base}/v1/generate"
    payload = {'model': 'mistral-large-latest', 'input': 'Hello'}
    print('\nPOST', gen_url)
    r = requests.post(gen_url, headers=headers, json=payload, timeout=10)
    print('Status:', r.status_code)
    try:
        print('Response JSON:', r.json())
    except Exception:
        print('Response text:', r.text[:1000])

    # Try the /v1/models/{model}/outputs endpoint which some Mistral APIs use
    model = 'mistral-large-latest'
    outputs_url = f"{base}/v1/models/{model}/outputs"
    out_payload = {'input': 'Hello from test', 'max_new_tokens': 64}
    print('\nPOST', outputs_url)
    r2 = requests.post(outputs_url, headers=headers, json=out_payload, timeout=10)
    print('Status:', r2.status_code)
    try:
        print('Response JSON:', r2.json())
    except Exception:
        print('Response text:', r2.text[:1000])
except Exception as e:
    print('Generate test failed:', e)

# Additional: try chat/completions shapes which many modern APIs use
try:
    chat_url = f"{base}/v1/models/{model}/chat/completions"
    chat_payload = {
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Say hello briefly.'}
        ],
        'temperature': 0.3,
        'max_tokens': 60
    }
    print('\nPOST', chat_url)
    r3 = requests.post(chat_url, headers=headers, json=chat_payload, timeout=10)
    print('Status:', r3.status_code)
    try:
        print('Response JSON:', r3.json())
    except Exception:
        print('Response text:', r3.text[:1000])

    # Try generic chat completions endpoint with model parameter
    generic_chat = f"{base}/v1/chat/completions"
    gen_payload = {'model': model, 'messages': chat_payload['messages'], 'temperature': 0.3, 'max_tokens': 60}
    print('\nPOST', generic_chat)
    r4 = requests.post(generic_chat, headers=headers, json=gen_payload, timeout=10)
    print('Status:', r4.status_code)
    try:
        print('Response JSON:', r4.json())
    except Exception:
        print('Response text:', r4.text[:1000])
except Exception as e:
    print('Chat test failed:', e)
