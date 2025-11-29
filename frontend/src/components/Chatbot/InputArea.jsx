import { useState } from 'react'
import { AudioRecorder } from '../AudioRecorder'
import { STATUS } from '../../utils/constants'

export const InputArea = ({
  inputMode,
  onModeChange,
  onTextSubmit,
  onVoiceSubmit,
  disabled,
  status
}) => {
  const [textInput, setTextInput] = useState('')

  const handleTextSubmit = (e) => {
    e.preventDefault()
    if (textInput.trim() && !disabled) {
      onTextSubmit(textInput.trim())
      setTextInput('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleTextSubmit(e)
    }
  }

  return (
    <div className="chatbot-input-area">
      <div className="input-mode-toggle">
        <button
          className={`mode-button ${inputMode === 'text' ? 'active' : ''}`}
          onClick={() => onModeChange('text')}
          disabled={disabled}
          aria-label="Text input mode"
        >
          Text
        </button>
        <button
          className={`mode-button ${inputMode === 'voice' ? 'active' : ''}`}
          onClick={() => onModeChange('voice')}
          disabled={disabled}
          aria-label="Voice input mode"
        >
          Voice
        </button>
      </div>

      {inputMode === 'text' ? (
        <form onSubmit={handleTextSubmit} className="text-input-form">
          <input
            type="text"
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={disabled}
            className="text-input"
            aria-label="Message input"
          />
          <button
            type="submit"
            disabled={disabled || !textInput.trim()}
            className="send-button"
            aria-label="Send message"
          >
            {status === STATUS.PROCESSING ? '...' : 'Send'}
          </button>
        </form>
      ) : (
        <div className="voice-input-area">
          <AudioRecorder
            onRecordingComplete={onVoiceSubmit}
            disabled={disabled}
          />
        </div>
      )}
    </div>
  )
}

