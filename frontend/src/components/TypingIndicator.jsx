import './TypingIndicator.css'

export const TypingIndicator = ({ message = 'Processing...' }) => {
  return (
    <div className="typing-indicator">
      <div className="dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <span className="message">{message}</span>
    </div>
  )
}

