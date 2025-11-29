---
description: Deployment guide for frontend and backend
---

# Deployment Guide

## Front‑end (React) – Vercel or Netlify

1. **Prerequisites**
   - Ensure the project builds without errors (`npm run build`).
   - All environment variables used at build time must be defined in the hosting service (e.g., `REACT_APP_API_URL`).

2. **Vercel**
   - Sign in to <https://vercel.com> and click **New Project**.
   - Connect the GitHub repository (or push the current repo to a new GitHub repo).
   - Vercel automatically detects a React/Vite project. Set the **Build Command** to `npm run build` and the **Output Directory** to `dist` (or `build` if you use Create‑React‑App).
   - Add any required environment variables under **Settings → Environment Variables**.
   - Deploy – Vercel will provide a preview URL and a production URL.

3. **Netlify**
   - Sign in to <https://app.netlify.com> and click **New site from Git**.
   - Connect the repository and set the **Build command** to `npm run build` and **Publish directory** to `dist` (or `build`).
   - Add environment variables in **Site settings → Build & deploy → Environment**.
   - Deploy – Netlify will generate a live URL.

4. **Considerations**
   - Both platforms serve static assets over a CDN, giving fast load times.
   - Ensure the **CORS** configuration on the backend allows the frontend domain (use `CORS_ORIGINS` in `backend/app/config.py`).
   - For a seamless voice‑chat experience, keep the audio files small (< 5 MB) and enable HTTPS (both Vercel and Netlify provide it by default).

## Back‑end (Flask) – Hugging Face Spaces

1. **Create a Space**
   - Go to <https://huggingface.co/spaces> and click **Create new Space**.
   - Choose **“Docker”** as the SDK (or **“Gradio”** if you want the UI, but we’ll run Flask). Give it a name, e.g., `voice-bot-backend`.

2. **Project Structure for Spaces**
   - The root of the Space should contain:
     - `app.py` (or `run.py`) – the Flask entry point.
     - `requirements.txt` – list all Python dependencies (including `flask`, `flask_cors`, `groq`, `whisper`, `gtts`, etc.).
     - `backend/` – keep your existing Flask app code.
     - `Dockerfile` – optional; Hugging Face will auto‑detect a `requirements.txt` and build the container.

3. **Modify the entry point for Spaces**
   - Spaces expects the server to listen on the port provided by the `PORT` environment variable. Your existing `run.py` already does this:
     ```python
     port = int(os.environ.get('PORT', 5000))
     socketio.run(app, host='0.0.0.0', port=port)
     ```
   - Ensure the file is named `app.py` or set the `HF_SPACE_RUN` environment variable to point to `run.py`.

4. **Add Secrets**
   - In the Space settings, add the required API keys (`GROQ_API_KEY`, `ELEVENLABS_API_KEY`, etc.) under **Secrets**. They will be injected as environment variables.

5. **Deploy**
   - Commit and push the code to the Space repository. Hugging Face will automatically build and start the Flask server.
   - The public URL will be something like `https://<username>.hf.space`. Test the health endpoint (`/health`) to confirm it’s up.

6. **CORS Configuration**
   - In `backend/app/config.py`, set `CORS_ORIGINS` to the domain of your frontend (e.g., `['https://your-frontend.vercel.app']`).
   - The Flask app already loads this value and applies `CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})` (or similar).

## Summary of Rules to Remember
- **Frontend**: Deploy on Vercel or Netlify (static CDN, HTTPS, easy env‑var handling).
- **Backend**: Deploy on Hugging Face Spaces as a Flask app, using the existing `run.py` entry point and providing API keys via Secrets.
- **CORS**: Keep `CORS_ORIGINS` in sync with the deployed frontend URL.
- **Priority**: Voice‑chat priority is stored in `config.py` (`VOICE_PRIORITY`/`TEXT_PRIORITY`). You can later use these values for request‑handling logic.

---

*These guidelines are now part of the project’s internal documentation and can be referenced for any future development or CI/CD pipelines.*
