# Backend LLM Model Issue - Manual Fix Required

## Problem
The backend keeps trying to use deprecated Groq models (`llama3-8b-8192` or `mixtral-8x7b-32768`) even after code changes, resulting in 500 errors.

## Root Cause
There's likely a `.env` file or environment variable that's overriding the code changes.

## Solution - Manual Steps

### 1. Find and Edit the .env File
```powershell
# Look for .env files
Get-ChildItem -Path "d:\Projects\Portfolio agent" -Filter ".env" -Recurse -Force

# Edit the .env file (likely in the root or backend folder)
# Change this line:
GROQ_MODEL=llama3-8b-8192  # or mixtral-8x7b-32768

# To this:
GROQ_MODEL=llama-3.3-70b-versatile
```

### 2. Verify Available Models
The following models are confirmed to work with your Groq API key:
- `llama-3.3-70b-versatile` (recommended - most capable)
- `llama-3.1-8b-instant` (faster, smaller)
- `openai/gpt-oss-120b` (alternative)
- `qwen/qwen3-32b` (alternative)

### 3. Kill ALL Python Processes
```powershell
taskkill /F /IM python.exe
```

### 4. Clear Python Cache
```powershell
cd "d:\Projects\Portfolio agent\backend"
Remove-Item -Path "app\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "app\services\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "app\routes\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
```

### 5. Start Backend Fresh
```powershell
cd "d:\Projects\Portfolio agent\backend"
python run.py
```

You should see:
```
DEBUG: Loaded GROQ_MODEL = llama-3.3-70b-versatile
```

### 6. Test
```powershell
python -c "import requests; r = requests.post('http://localhost:5000/api/session'); sid = r.json()['session_id']; r2 = requests.post('http://localhost:5000/api/chat', json={'text': 'hi', 'session_id': sid}); print('Status:', r2.status_code); print(r2.json())"
```

Expected output:
```
Status: 200
{'response': 'Hey! How can I help you today?', ...}
```

## If Still Failing

Check the terminal output for:
- `DEBUG: About to call generate_response` - confirms endpoint is hit
- `DEBUG: generate_response called with X messages` - confirms function is called
- `DEBUG: Config GROQ_MODEL in llm_service = llama-3.3-70b-versatile` - confirms correct model
- `Using Groq with model: llama-3.3-70b-versatile` - confirms API call uses correct model

If you don't see these debug prints, there's still a stale process running.

## Alternative: Use OpenAI Instead

If Groq continues to fail, you can switch to OpenAI:

1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. The backend will automatically fall back to OpenAI if Groq fails.

## Files Modified (for reference)
- `backend/app/config.py` - Line 23: `GROQ_MODEL = 'llama-3.3-70b-versatile'`
- `backend/app/services/llm_service.py` - Line 140: `model = 'llama-3.3-70b-versatile'`
- `backend/app/__init__.py` - Line 28: Added debug print
- `backend/app/routes/api.py` - Line 154: Added debug print

All code changes are correct. The issue is environmental (cache/env vars).
