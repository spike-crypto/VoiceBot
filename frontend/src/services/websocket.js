import { io } from 'socket.io-client'
import { WS_URL } from '../utils/constants'

class WebSocketService {
  constructor() {
    this.socket = null
    this.listeners = {}
  }

  connect(sessionId) {
    if (this.socket?.connected) {
      return
    }

    this.socket = io(WS_URL, {
      transports: ['websocket', 'polling']
    })

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
      if (sessionId) {
        this.socket.emit('join_session', { session_id: sessionId })
      }
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
    })

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error)
    })
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  on(event, callback) {
    if (this.socket) {
      this.socket.on(event, callback)
    }
  }

  off(event, callback) {
    if (this.socket) {
      this.socket.off(event, callback)
    }
  }

  emit(event, data) {
    if (this.socket?.connected) {
      this.socket.emit(event, data)
    }
  }

  isConnected() {
    return this.socket?.connected || false
  }
}

export const wsService = new WebSocketService()

