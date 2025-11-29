# Voice Bot Backend API

Flask REST API backend for the Voice Bot Interview Assistant.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your API keys to `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the server:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Health check endpoint

### Session Management
- `POST /api/session` - Create a new session
- `GET /api/conversation/<session_id>` - Get conversation history
- `DELETE /api/conversation/<session_id>` - Clear conversation

### Audio Processing
- `POST /api/transcribe` - Transcribe audio to text
- `POST /api/tts` - Convert text to speech
- `POST /api/process` - Complete voice-to-voice pipeline

### Chat
- `POST /api/chat` - Generate response from text

## WebSocket

- Connect to `/socket.io` for real-time communication
- Events: `connect`, `disconnect`, `join_session`, `process_voice`

## Configuration

See `.env.example` for all configuration options.

## Features

- RESTful API with Flask
- WebSocket support for real-time communication
- Multi-provider LLM support (Groq, OpenAI)
- Caching with Redis (optional)
- Session management
- Rate limiting
- Comprehensive logging
- Error handling

