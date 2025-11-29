import { useState, useEffect, useCallback } from 'react'
import { createSession, getConversation, clearConversation as clearConv } from '../services/api'

export const useConversation = () => {
  const [sessionId, setSessionId] = useState(null)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Initialize session - ALWAYS START FRESH
    const initSession = async () => {
      // Clear any stored session
      localStorage.removeItem('session_id')

      // Create new session
      const newSessionId = await createSession()
      setSessionId(newSessionId)
      setMessages([])

      console.log('Fresh session created:', newSessionId)
    }
    initSession()
  }, [])

  const addMessage = useCallback((role, content) => {
    const newMessage = {
      role,
      content,
      timestamp: new Date().toISOString()
    }
    setMessages((prev) => [...prev, newMessage])
  }, [])

  const clearConversation = useCallback(async () => {
    if (sessionId) {
      try {
        await clearConv(sessionId)
        setMessages([])
        const newSessionId = await createSession()
        setSessionId(newSessionId)
      } catch (error) {
        console.error('Error clearing conversation:', error)
      }
    }
  }, [sessionId])

  return {
    sessionId,
    messages,
    addMessage,
    clearConversation,
    loading,
    setLoading
  }
}

