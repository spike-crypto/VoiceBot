# How to View Logs

## Log File Location
- **Path**: `backend/logs/voicebot_YYYYMMDD.log`
- **Example**: `backend/logs/voicebot_20251127.log`

## View Logs in Real-Time

### Windows PowerShell:
```powershell
# View last 50 lines
Get-Content "backend\logs\voicebot_20251127.log" -Tail 50

# Follow logs in real-time (like tail -f)
Get-Content "backend\logs\voicebot_20251127.log" -Wait -Tail 20

# Search for errors only
Get-Content "backend\logs\voicebot_20251127.log" | Select-String -Pattern "ERROR|Exception|Traceback" -Context 3
```

### View All Errors:
```powershell
Get-Content "backend\logs\voicebot_20251127.log" | Select-String "ERROR"
```

### View Latest Errors:
```powershell
Get-Content "backend\logs\voicebot_20251127.log" -Tail 100 | Select-String "ERROR|Exception"
```

## Terminal Output

Errors also appear in the **terminal where you run `python run.py`**:
- Look at the terminal window where the backend is running
- Errors will appear in red or with "ERROR" prefix
- Full tracebacks are shown in the terminal

## Log Levels

- **DEBUG**: Detailed information (usually only when debugging)
- **INFO**: General information (normal operations)
- **WARNING**: Warning messages (non-critical issues)
- **ERROR**: Error messages (exceptions, failures)
- **CRITICAL**: Critical errors (system failures)

## Common Issues

### Logs Not Updating
- Make sure the backend server is running
- Check if you're looking at the correct log file (check date in filename)
- Restart the backend to create a new log session

### Can't Find Log File
- Check if `backend/logs/` directory exists
- Check file permissions
- Verify LOG_DIR in config

### Too Many Logs
- Adjust LOG_LEVEL in `.env` file
- Set to `WARNING` to see only warnings and errors
- Set to `ERROR` to see only errors

