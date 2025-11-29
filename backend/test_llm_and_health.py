"""Quick health and LLM smoke test for the voice-bot API.

Checks:
- GET /api/health
- POST /api/chat with a short prompt (HTTP if server running)
- If HTTP is not reachable, imports the Flask app and calls `generate_response` directly

Run: from repo root with virtualenv activated:
  .\.venv\Scripts\Activate.ps1; python backend\test_llm_and_health.py
"""
import os
import sys
import time
import json
from datetime import datetime

import requests

DEFAULT_BASE = os.environ.get('API_BASE_URL') or os.environ.get('VITE_API_BASE_URL') or 'http://localhost:5000'
HEALTH_URL = DEFAULT_BASE.rstrip('/') + '/api/health'
CHAT_URL = DEFAULT_BASE.rstrip('/') + '/api/chat'


def http_health_check():
    print(f"Checking HTTP health at {HEALTH_URL}")
    try:
        r = requests.get(HEALTH_URL, timeout=6)
        print(f"HTTP {r.status_code} - {r.text}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"HTTP health check failed: {e}")
        return False


def http_llm_check(prompt: str = "Hello, please introduce yourself briefly."):
    print(f"Calling LLM via HTTP POST {CHAT_URL}")
    payload = {'text': prompt}
    try:
        r = requests.post(CHAT_URL, json=payload, timeout=30)
        print(f"HTTP {r.status_code}")
        try:
            data = r.json()
        except Exception:
            print("Response was not JSON:\n", r.text)
            return False

        if r.status_code == 200 and 'response' in data:
            print("LLM HTTP response:")
            print(json.dumps({'response': data.get('response'), 'metadata': data.get('metadata')}, indent=2))
            return True
        else:
            print("LLM HTTP call returned non-200 or missing 'response':", data)
            return False
    except requests.exceptions.RequestException as e:
        print(f"HTTP LLM request failed: {e}")
        return False


def direct_llm_call(prompt: str = "Hello, please introduce yourself briefly."):
    """Fallback: import the app factory and call generate_response directly inside app context"""
    print("Attempting direct (in-process) LLM call using app context")
    try:
        from app import create_app
        from app.services.llm_service import generate_response
    except Exception as e:
        print(f"Failed to import app or llm service: {e}")
        return False

    app = create_app()
    with app.app_context():
        # Build a minimal conversation history expected by generate_response
        conv = [{'role': 'user', 'content': prompt}]
        try:
            resp_text, metadata, cache_hit = generate_response(conv, use_cache=False)
            print("Direct LLM result:")
            print(json.dumps({'response': resp_text, 'metadata': metadata, 'cache_hit': cache_hit}, indent=2))
            return True
        except Exception as e:
            print(f"Direct generate_response failed: {e}")
            return False


def main():
    print(f"LLM & API Health Check - {datetime.now().isoformat()}")
    print(f"Using base URL: {DEFAULT_BASE}")

    http_ok = http_health_check()

    if http_ok:
        print('\n-- LLM via HTTP --')
        llm_ok = http_llm_check()
        if not llm_ok:
            print('\nHTTP server reachable but LLM call failed. You can inspect server logs for details.')
    else:
        print('\nHTTP server not reachable; trying in-process LLM call')
        llm_ok = direct_llm_call()

    print('\nSummary:')
    print(f"  HTTP reachable: {http_ok}")
    print(f"  LLM check passed: {llm_ok}")

    if not http_ok and not llm_ok:
        print('\nNo working LLM endpoint found. Check environment variables (OPENAI_API_KEY, GROQ_API_KEY), and ensure the backend is running.')
        sys.exit(2)

    print('\nDone.')


if __name__ == '__main__':
    main()
