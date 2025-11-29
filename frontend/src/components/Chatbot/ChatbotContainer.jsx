import { useState, useRef, useEffect } from 'react'
import { useConversationContext } from '../../context/ConversationContext'
import { ChatInterface } from './ChatInterface'
import { InputArea } from './InputArea'
import { ResumeModal } from './ResumeModal'
import { processVoice, sendChat, textToSpeech } from '../../services/api'
import { STATUS } from '../../utils/constants'
import './Chatbot.css'

export const ChatbotContainer = () => {
  const { sessionId, messages, addMessage, clearConversation } = useConversationContext()
  const [status, setStatus] = useState(STATUS.IDLE)
  const [error, setError] = useState(null)
  const [audioUrl, setAudioUrl] = useState(null)
  const [inputMode, setInputMode] = useState('voice') // Default to voice mode
  const [showResume, setShowResume] = useState(false)
  const containerRef = useRef(null)

  const handleTextSubmit = async (text) => {
    if (!text.trim() || !sessionId) return

    setStatus(STATUS.PROCESSING)
    setError(null)

    try {
      const result = await sendChat(text, sessionId)
      addMessage('user', text)
      addMessage('assistant', result.response)
      setStatus(STATUS.IDLE)
    } catch (err) {
      console.error('Error sending chat:', err)
      setError(err.response?.data?.error || err.message || 'Failed to send message')
      setStatus(STATUS.ERROR)
    }
  }

  const handleVoiceSubmit = async (audioFile) => {
    if (!sessionId) {
      setError('Session not initialized')
      return
    }

    setStatus(STATUS.PROCESSING)
    setError(null)

    try {
      const result = await processVoice(audioFile, sessionId)
      addMessage('user', result.transcribed_text)
      addMessage('assistant', result.response_text)

      if (result.audio_url) {
        setAudioUrl(result.audio_url)
      } else {
        const audioBlobUrl = await textToSpeech(result.response_text)
        setAudioUrl(audioBlobUrl)
      }

      setStatus(STATUS.IDLE)
    } catch (err) {
      console.error('Error processing voice:', err)
      setError(err.response?.data?.error || err.message || 'Failed to process voice')
      setStatus(STATUS.ERROR)
    }
  }

  const handleClear = async () => {
    try {
      await clearConversation()
      setAudioUrl(null)
      setError(null)
      setStatus(STATUS.IDLE)
    } catch (err) {
      console.error('Error clearing conversation:', err)
    }
  }

  const scrollToBottom = () => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="chatbot-container" id="chatbot">
      <div className="chatbot-header">
        <h2>Chat with Balamurugan</h2>
        <button
          className="clear-chat-button"
          onClick={handleClear}
          aria-label="Clear chat"
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault()
              handleClear()
            }
          }}
        >
          Clear
        </button>
      </div>
      <div className="chatbot-messages" ref={containerRef}>
        <ChatInterface
          messages={messages}
          status={status}
          error={error}
          audioUrl={audioUrl}
          onShowResume={() => setShowResume(true)}
        />
      </div>
      <InputArea
        inputMode={inputMode}
        onModeChange={setInputMode}
        onTextSubmit={handleTextSubmit}
        onVoiceSubmit={handleVoiceSubmit}
        disabled={status === STATUS.PROCESSING}
        status={status}
      />
      <ResumeModal isOpen={showResume} onClose={() => setShowResume(false)} />
    </div>
  )
}

