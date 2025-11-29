# Setup Guide

## Prerequisites

- Python 3.12+
- Node.js 18+
- npm or yarn
- Groq API key (get from https://console.groq.com)

## Local Development Setup

### Option 1: Manual Setup

#### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
python run.py
```

#### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Option 2: Docker Setup

```bash
# Create .env file in root
echo "GROQ_API_KEY=your_key_here" > .env

# Start services
docker-compose up --build
```

## Environment Variables

### Backend (.env)
```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
REDIS_ENABLED=false
FLASK_ENV=development
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_WS_URL=http://localhost:5000
```

## Testing

1. Start backend: `cd backend && python run.py`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: http://localhost:3000
4. Click "Start Recording" and speak a question
5. Wait for response

## Troubleshooting

### Backend Issues
- **Port 5000 in use**: Change port in `run.py`
- **Whisper model download**: First run downloads ~500MB model
- **API key error**: Check `.env` file has correct key

### Frontend Issues
- **CORS errors**: Check backend CORS configuration
- **API connection**: Verify backend is running on port 5000
- **Audio recording**: Check browser microphone permissions

## Production Deployment

See `DEPLOYMENT.md` for production deployment instructions.

