import { formatDate } from '../../utils/helpers'

export const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user'

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-bubble-content">
        <div className="message-bubble-header">
          <span className="message-bubble-role">
            {isUser ? 'You' : 'Balamurugan'}
          </span>
          {message.timestamp && (
            <span className="message-bubble-time">
              {formatDate(message.timestamp)}
            </span>
          )}
        </div>
        <div className="message-bubble-text">{message.content}</div>
      </div>
    </div>
  )
}

