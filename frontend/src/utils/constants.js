export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api'
export const WS_URL = import.meta.env.VITE_WS_URL || 'http://localhost:5001'

export const MESSAGE_TYPES = {
  USER: 'user',
  ASSISTANT: 'assistant',
  SYSTEM: 'system'
}

export const STATUS = {
  IDLE: 'idle',
  RECORDING: 'recording',
  PROCESSING: 'processing',
  TRANSCRIBING: 'transcribing',
  GENERATING: 'generating',
  SPEAKING: 'speaking',
  ERROR: 'error'
}

