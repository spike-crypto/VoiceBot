# How to See Errors in Backend Logs

## The Problem

Errors **ARE** being logged, but you might not see them because:

1. **Backend is running old code** - Python caches bytecode, so changes don't apply until restart
2. **Log file location** - You might be looking at the wrong file
3. **Log file not refreshing** - The file viewer might not auto-refresh

## ✅ Solution: View Errors in Real-Time

### Method 1: Watch Log File in Real-Time (RECOMMENDED)

```powershell
# Navigate to backend directory
cd "D:\Projects\Portfolio agent\backend"

# Watch log file in real-time (updates as errors occur)
Get-Content "logs\voicebot_20251127.log" -Wait -Tail 50
```

**This will:**
- Show the last 50 lines
- **Auto-update** when new errors occur
- Keep running until you press `Ctrl+C`

### Method 2: Check Terminal Output

Errors are also printed to **stderr** (the terminal where you ran `python run.py`). Look at that terminal window - you should see:

```
================================================================================
❌ ERROR in /api/process: AttributeError: 'Request' object has no attribute 'app'
Traceback:
...
================================================================================
```

### Method 3: View Recent Errors Only

```powershell
# Show only ERROR lines from the last 100 lines
Get-Content "D:\Projects\Portfolio agent\backend\logs\voicebot_20251127.log" -Tail 100 | Select-String -Pattern "ERROR|Exception|Traceback" -Context 3
```

### Method 4: Find All Errors Today

```powershell
# Find all errors in today's log file
Get-Content "D:\Projects\Portfolio agent\backend\logs\voicebot_20251127.log" | Select-String -Pattern "ERROR" -Context 5
```

## 🔍 Where Are Logs?

- **Log File**: `backend/logs/voicebot_YYYYMMDD.log` (e.g., `voicebot_20251127.log`)
- **Console**: The terminal where you run `python run.py`
- **Format**: `YYYY-MM-DD HH:MM:SS - module - LEVEL - [file:line] - message`

## 🐛 Current Error You're Seeing

The error `'Request' object has no attribute 'app'` is being logged. You can see it in the log file:

```
2025-11-27 23:40:09,025 - app.routes.api - ERROR - [api.py:263] - Process voice error: 'Request' object has no attribute 'app'
Traceback (most recent call last):
  File "D:\Projects\Portfolio agent\backend\app\routes\api.py", line 199, in process_voice
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
                    ^^^^^^^^^^^
AttributeError: 'Request' object has no attribute 'app'
```

## ⚠️ Why You Might Not See It

1. **Log file viewer not refreshing** - Use `Get-Content -Wait` to see updates
2. **Looking at wrong file** - Check the date in filename (YYYYMMDD format)
3. **Backend not restarted** - Old code is still running

## ✅ Quick Fix: See Errors Now

```powershell
# 1. Stop backend (Ctrl+C in the terminal running it)

# 2. Clear cache and restart
cd "D:\Projects\Portfolio agent\backend"
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
python run.py

# 3. In ANOTHER terminal, watch logs in real-time:
Get-Content "logs\voicebot_20251127.log" -Wait -Tail 50
```

## 📊 Log Levels

- **DEBUG**: Detailed information (everything)
- **INFO**: General information (normal operations)
- **WARNING**: Warning messages (non-critical issues)
- **ERROR**: Error messages (exceptions, failures) ← **You want to see these**
- **CRITICAL**: Critical errors (system failures)

Errors are logged at **ERROR** level, which is **always visible** in both file and console.


