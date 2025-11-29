# 🚀 Deployment Guide: Voice Bot Agent

This guide covers how to deploy the **Frontend to Netlify** and the **Backend to Hugging Face Spaces**.

---

## 📦 Part 1: Backend Deployment (Hugging Face Spaces)

Hugging Face Spaces is excellent for hosting Python/Flask applications.

### 1. Create a New Space
1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. **Name**: `voice-bot-backend` (or similar)
4. **License**: MIT (optional)
5. **SDK**: Select **Docker** (This is important!)
6. **Visibility**: Public or Private (Private recommended if you have API keys)

### 2. Upload Code
You can upload files directly via the web interface or use Git.
**Files to upload from `backend/` folder:**
- `Dockerfile`
- `requirements.txt`
- `run.py`
- `app/` (entire folder)
- `logs/` (create empty folder if needed, or ignore)

### 3. Configure Environment Variables (Secrets)
In your Space settings, go to **"Settings"** -> **"Variables and secrets"**.
Add the following **Secrets** (from your `.env` file):

| Key | Value |
|-----|-------|
| `ELEVENLABS_API_KEY` | Your Primary Key |
| `ELEVENLABS_API_KEY_BACKUP_1` | Your Backup Key 1 |
| `ELEVENLABS_API_KEY_BACKUP_2` | Your Backup Key 2 |
| `ELEVENLABS_VOICE_ID` | `ErXwobaYiN019PkySvjV` |
| `MISTRAL_API_KEY` | Your Mistral Key |
| `SECRET_KEY` | A random secret string |

### 4. Build & Run
Hugging Face will automatically build your Docker container. Watch the **"Logs"** tab. Once it says "Running on port 7860", your backend is live!
**Copy the Direct URL**: It will look like `https://username-space-name.hf.space`.

---

## 🌐 Part 2: Frontend Deployment (Netlify)

Netlify is perfect for the React frontend.

### 1. Prepare Frontend Config
1. Open `frontend/.env` (or create it in Netlify settings).
2. You need to point the frontend to your **Hugging Face Backend URL**.

### 2. Deploy to Netlify
**Option A: Drag & Drop (Manual)**
1. Run `npm run build` in your `frontend` folder.
2. Go to [Netlify Drop](https://app.netlify.com/drop).
3. Drag and drop the `frontend/dist` folder.

**Option B: Git (Recommended)**
1. Push your code to GitHub.
2. Log in to Netlify and click **"Add new site"** -> **"Import from existing project"**.
3. Select your GitHub repo.
4. **Build Settings**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
5. **Environment Variables**:
   Click "Show advanced" -> "New Variable".
   - Key: `VITE_API_BASE_URL`
   - Value: `https://YOUR-HF-SPACE-URL.hf.space/api` (e.g., `https://balamurugan-voice-bot.hf.space/api`)
   - Key: `VITE_WS_URL`
   - Value: `https://YOUR-HF-SPACE-URL.hf.space`

### 3. Publish
Click **"Deploy site"**. Netlify will build and host your site.

---

## 🔗 Part 3: Final Connection

Once both are deployed:
1. Ensure the **Frontend** `VITE_API_BASE_URL` points to the **Backend** URL.
2. If you get CORS errors, you might need to update `backend/app/__init__.py` to allow the Netlify domain in `CORS(app, resources={r"/*": {"origins": "*"}})`. (Currently it allows `*` so it should work out of the box).

## ✅ Verification
1. Open your Netlify URL.
2. Check the console for connection errors.
3. Test the voice bot!
