# ElevenLabs API Key Fallback System

## Overview
The system now supports automatic fallback between multiple ElevenLabs API keys when quota limits are reached.

## How It Works

### 1. Configuration
Add these keys to your `.env` file:

```env
# Primary key (tried first)
ELEVENLABS_API_KEY=your_primary_key_here

# Backup key 1 (tried if primary fails)
ELEVENLABS_API_KEY_BACKUP_1=sk_ffe30c947567ad19245c8ccc6790875e925d0521cc97f70f

# Backup key 2 (tried if backup 1 fails)
ELEVENLABS_API_KEY_BACKUP_2=sk_841aeecbb016b397328498a2a86f9fd9386a9dc2be9c29d3
```

### 2. Fallback Logic
When a TTS request is made, the system:

1. **Tries Primary Key** first
2. If it gets a **429 (Quota Exceeded)** or **401 (Invalid Key)** error, it automatically tries **Backup Key 1**
3. If Backup Key 1 also fails, it tries **Backup Key 2**
4. If all keys fail, it returns an error with details about which key failed and why

### 3. Error Handling
The system handles these specific errors:
- **429**: Quota exceeded → Try next key
- **401**: Invalid API key → Try next key
- **Other errors**: Log and try next key
- **Network errors**: Try next key

### 4. Logging
The system logs which key is being used:
```
INFO: Attempting TTS with primary key...
WARNING: primary key hit quota limit (429), trying next key...
INFO: Attempting TTS with backup_1 key...
INFO: TTS successful with backup_1 key: /path/to/audio.mp3
```

## Benefits
✅ **Automatic failover** - No manual intervention needed
✅ **Quota management** - Distributes load across multiple keys
✅ **Transparent** - Logs show which key is being used
✅ **Resilient** - Continues working even if some keys are exhausted

## Testing
To test the fallback:
1. Set an invalid primary key → Should automatically use backup_1
2. Set quota-exceeded primary key → Should automatically use backup_1
3. Remove all keys → Should fail with clear error message

## Notes
- Keys are tried in order: primary → backup_1 → backup_2
- Once a key succeeds, it stops trying others
- The system caches successful TTS results to minimize API calls
