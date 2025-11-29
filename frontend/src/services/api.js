import axios from 'axios'
import { API_BASE_URL } from '../utils/constants'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const sessionId = localStorage.getItem('session_id')
    if (sessionId) {
      config.headers['X-Session-ID'] = sessionId
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 429) {
      console.error('Rate limit exceeded')
    }
    return Promise.reject(error)
  }
)

export const createSession = async () => {
  const response = await api.post('/session')
  const sessionId = response.data.session_id
  localStorage.setItem('session_id', sessionId)
  return sessionId
}

export const transcribeAudio = async (audioFile) => {
  const formData = new FormData()
  formData.append('audio', audioFile)

  const response = await api.post('/transcribe', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

export const sendChat = async (text, sessionId) => {
  const response = await api.post('/chat', {
    text,
    session_id: sessionId
  })
  return response.data
}

export const textToSpeech = async (text) => {
  const response = await api.post('/tts', { text }, {
    responseType: 'blob'
  })
  return URL.createObjectURL(response.data)
}

export const processVoice = async (audioFile, sessionId) => {
  const formData = new FormData()
  formData.append('audio', audioFile)
  if (sessionId) {
    formData.append('session_id', sessionId)
  }

  const response = await api.post('/process', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

export const getConversation = async (sessionId) => {
  const response = await api.get(`/conversation/${sessionId}`)
  return response.data
}

export const clearConversation = async (sessionId) => {
  const response = await api.delete(`/conversation/${sessionId}`)
  return response.data
}

export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

// Grouped API exports
export const chatAPI = {
  createSession,
  sendMessage: sendChat,
  textToSpeech: async (text) => {
    const response = await api.post('/tts', { text }, {
      responseType: 'blob'
    })
    return response.data // Return blob directly
  },
  transcribeAudio,
  processVoice,
  getConversation,
  clearConversation,
  healthCheck
}

