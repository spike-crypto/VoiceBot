import { useState } from 'react'
import { useAudioRecorder } from '../hooks/useAudioRecorder'
import { formatTime } from '../utils/helpers'
import './AudioRecorder.css'

export const AudioRecorder = ({ onRecordingComplete, disabled }) => {
  const { isRecording, recordingTime, startRecording, stopRecording, cancelRecording } = useAudioRecorder()
  const [error, setError] = useState(null)

  const handleStart = async () => {
    try {
      setError(null)
      await startRecording()
    } catch (err) {
      setError('Failed to start recording. Please check microphone permissions.')
      console.error(err)
    }
  }

  const handleStop = async () => {
    try {
      const audioFile = await stopRecording()
      if (audioFile && onRecordingComplete) {
        onRecordingComplete(audioFile)
      }
    } catch (err) {
      setError('Failed to stop recording.')
      console.error(err)
    }
  }

  const handleCancel = () => {
    cancelRecording()
    setError(null)
  }

  return (
    <div className="audio-recorder">
      {error && <div className="error-message">{error}</div>}
      
      <div className="recorder-controls">
        {!isRecording ? (
          <button
            className="record-button start"
            onClick={handleStart}
            disabled={disabled}
            aria-label="Start recording"
            onKeyDown={(e) => {
              if ((e.key === 'Enter' || e.key === ' ') && !disabled) {
                e.preventDefault()
                handleStart()
              }
            }}
          >
            🎤 Start Recording
          </button>
        ) : (
          <>
            <div className="recording-indicator">
              <span className="pulse"></span>
              <span>Recording: {formatTime(recordingTime)}</span>
            </div>
            <div className="recording-actions">
              <button
                className="record-button stop"
                onClick={handleStop}
                aria-label="Stop recording"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    handleStop()
                  }
                }}
              >
                ⏹ Stop
              </button>
              <button
                className="record-button cancel"
                onClick={handleCancel}
                aria-label="Cancel recording"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    handleCancel()
                  }
                }}
              >
                ✕ Cancel
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

