import { MessageBubble } from './MessageBubble'
import { TypingIndicator } from '../TypingIndicator'
import { AudioPlayer } from '../AudioPlayer'

export const ChatInterface = ({ messages, status, error, audioUrl, onShowResume }) => {
  return (
    <div className="chat-interface">
      {messages.length === 0 ? (
        <div className="chat-empty-state">
          <h3>Let's Talk!</h3>
          <p>I'm here to answer your questions about my work, skills, and what drives me.</p>
          <p className="subtitle">Go ahead - ask me anything.</p>
          <button className="view-resume-btn" onClick={onShowResume}>
            View Resume
          </button>
        </div>
      ) : (
        messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))
      )}

      {status === 'processing' && (
        <TypingIndicator message="Processing your question..." />
      )}

      {status === 'generating' && (
        <TypingIndicator message="Generating response..." />
      )}

      {error && (
        <div className="chat-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {audioUrl && (
        <div className="chat-audio-player">
          <AudioPlayer audioUrl={audioUrl} autoPlay={true} />
        </div>
      )}
    </div>
  )
}

