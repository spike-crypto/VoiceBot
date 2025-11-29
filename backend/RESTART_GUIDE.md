# Backend Restart Guide

## If you're getting 500 errors, restart the backend:

### Windows PowerShell:
```powershell
# 1. Stop the current server (Ctrl+C in the terminal where it's running)
# OR find and kill the process:
Get-Process python | Where-Object {$_.MainWindowTitle -like "*run.py*"} | Stop-Process

# 2. Navigate to backend directory
cd "D:\Projects\Portfolio agent\backend"

# 3. Restart the server
python run.py
```

### Quick Restart:
1. Press `Ctrl+C` in the terminal where backend is running
2. Run `python run.py` again

## Verify it's working:
- Check logs: `backend/logs/voicebot_YYYYMMDD.log`
- Test health endpoint: `http://localhost:5000/api/health`
- Should see: `{"status": "healthy", ...}`

## Common Issues After Restart:

### Port Already in Use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000
# Kill it (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Module Not Found
```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Error
- Make sure `.env` file exists in `backend/` directory
- Check `GROQ_API_KEY` is set correctly

