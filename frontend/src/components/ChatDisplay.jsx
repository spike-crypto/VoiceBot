import { useEffect, useRef } from 'react'
import { formatDate } from '../utils/helpers'
import './ChatDisplay.css'

export const ChatDisplay = ({ messages }) => {
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="chat-display">
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>Start a conversation by recording a question!</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
            >
              <div className="message-content">
                <div className="message-header">
                  <span className="message-role">
                    {message.role === 'user' ? 'You' : 'Balamurugan'}
                  </span>
                  {message.timestamp && (
                    <span className="message-time">
                      {formatDate(message.timestamp)}
                    </span>
                  )}
                </div>
                <div className="message-text">{message.content}</div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  )
}

