---
description: Complete deployment guide for Voice Bot
---

# 🚀 Voice Bot Deployment Guide

## Current Deployment Status

### ✅ **Production URLs:**
- **Frontend (Netlify)**: https://lively-crisp-4d3b28.netlify.app
- **Backend (Hugging Face)**: https://viperlurk-voicebot.hf.space

### ✅ **What's Working:**
1. Text-to-text chat (fully functional)
2. Voice-to-text (STT) - user can speak, LLM understands
3. LLM responds as Balamurugan persona
4. Conversation history/context maintained
5. Frontend CI/CD (auto-deploys on GitHub push)

### ⚠️ **Known Issues:**
1. **Text-to-voice (TTS)** - Requires valid ElevenLabs API key
2. **Backend CI/CD** - Manual deployment required (GitHub Action failing)

---

## 🔧 **Making Code Changes**

### **Frontend Changes (Auto-Deploy):**

1. Make changes to files in `frontend/` folder
2. Commit and push to GitHub:
   ```powershell
   git add .
   git commit -m "Your change description"
   git push
   ```
3. Netlify automatically detects the change and rebuilds
4. Check deployment status at: https://app.netlify.com

### **Backend Changes (Manual Deploy):**

// turbo
1. Make changes to files in `backend/` folder
2. Run the upload script:
   ```powershell
   $env:HF_TOKEN="your_hf_token_here"
   python clean_upload.py
   ```
3. Wait 1-2 minutes for Hugging Face to rebuild
4. Check logs at: https://huggingface.co/spaces/viperlurk/VoiceBot

---

## 🔑 **Environment Variables**

### **Netlify (Frontend):**
Set in: Site settings → Environment variables

| Variable | Value |
|----------|-------|
| `VITE_API_BASE_URL` | `https://viperlurk-voicebot.hf.space/api` |
| `VITE_WS_URL` | `https://viperlurk-voicebot.hf.space` |

### **Hugging Face (Backend):**
Set in: Space Settings → Variables and secrets (as **Secrets**, not Variables)

| Secret Name | Description |
|-------------|-------------|
| `ELEVENLABS_API_KEY` | Primary ElevenLabs API key |
| `ELEVENLABS_API_KEY_BACKUP_1` | Backup key 1 (for quota failover) |
| `ELEVENLABS_API_KEY_BACKUP_2` | Backup key 2 (for quota failover) |
| `ELEVENLABS_VOICE_ID` | `ErXwobaYiN019PkySvjV` (Antoni - male voice) |
| `MISTRAL_API_KEY` | Your Mistral API key |
| `SECRET_KEY` | Random string for Flask sessions |

---

## 🐛 **Troubleshooting**

### **Frontend not updating after push:**
1. Go to Netlify → Deploys
2. Click "Trigger deploy" → "Clear cache and deploy site"
3. Hard refresh browser: `Ctrl + Shift + R`

### **Backend not responding:**
1. Check Hugging Face Space status (should show "Running")
2. Check logs for errors
3. Verify all secrets are set correctly
4. Factory reboot if needed

### **Voice (TTS) not working:**
1. Verify ElevenLabs API key is valid
2. Check ElevenLabs account quota
3. Review backend logs for specific error
4. Fallback mechanism will try all 3 keys automatically

### **LLM errors (429 - Quota exceeded):**
1. Mistral API has rate limits
2. Wait a few minutes and try again
3. Consider upgrading Mistral tier
4. Or switch to `mistral-small-latest` model (edit `llm_service.py` line 76)

---

## 📊 **Monitoring**

### **Check Frontend Status:**
- Netlify Dashboard: https://app.netlify.com
- View deploy logs
- Check analytics

### **Check Backend Status:**
- Hugging Face Space: https://huggingface.co/spaces/viperlurk/VoiceBot
- View container logs
- Monitor API health: `https://viperlurk-voicebot.hf.space/api/health`

---

## 🔄 **Updating API Keys**

### **When ElevenLabs key expires:**
1. Go to elevenlabs.io → Profile → API Keys
2. Generate new key
3. Update Hugging Face secret: `ELEVENLABS_API_KEY`
4. Factory reboot Space

### **When Mistral key expires:**
1. Go to console.mistral.ai
2. Generate new key
3. Update Hugging Face secret: `MISTRAL_API_KEY`
4. Factory reboot Space

---

## ✅ **Deployment Checklist**

Before deploying changes:
- [ ] Test locally (`python run.py` for backend, `npm run dev` for frontend)
- [ ] Commit changes to GitHub
- [ ] Frontend: Push to GitHub (auto-deploys)
- [ ] Backend: Run `clean_upload.py` script
- [ ] Verify deployment on production URLs
- [ ] Test voice bot functionality
- [ ] Check logs for errors

---

## 🎯 **Future Improvements**

1. **Fix Backend CI/CD**: Resolve GitHub Action token issue for automatic backend deployment
2. **Add Monitoring**: Set up alerts for API failures
3. **Improve Error Handling**: Better user feedback when voice fails
4. **Add Analytics**: Track usage and conversation metrics
