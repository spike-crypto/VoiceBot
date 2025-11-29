# Force Restart Backend - CRITICAL

## The Error You're Seeing

The error `'Request' object has no attribute 'app'` means the backend is running **OLD CODE** that hasn't been reloaded.

## Solution: Force Restart

### Step 1: Kill All Python Processes
```powershell
# Find all Python processes
Get-Process python -ErrorAction SilentlyContinue

# Kill all Python processes (be careful!)
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### Step 2: Verify Port 5000 is Free
```powershell
# Check if port 5000 is in use
netstat -ano | findstr :5000

# If something is using it, kill it (replace PID)
taskkill /PID <PID> /F
```

### Step 3: Clear Python Cache
```powershell
cd "D:\Projects\Portfolio agent\backend"
# Remove all __pycache__ directories
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
# Remove all .pyc files
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
```

### Step 4: Restart Backend
```powershell
cd "D:\Projects\Portfolio agent\backend"
python run.py
```

### Step 5: Verify It's Running New Code
- Check terminal output for: `Starting server on port 5000`
- Test: `http://localhost:5000/api/health`
- Should see: `{"status": "healthy"}`

## Why This Happens

Python caches compiled bytecode (`.pyc` files) in `__pycache__` directories. When you modify code, Python might still use the old cached version until you:
1. Restart the server
2. Clear the cache
3. Force a reload

## Quick Fix Command (Run All at Once)

```powershell
cd "D:\Projects\Portfolio agent\backend"
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
python run.py
```


