import { useState, useRef, useEffect } from 'react'
import { playAudio } from '../services/audio'
import './AudioPlayer.css'

export const AudioPlayer = ({ audioUrl, autoPlay = true }) => {
  const [isPlaying, setIsPlaying] = useState(false)
  const [error, setError] = useState(null)
  const audioRef = useRef(null)

  useEffect(() => {
    if (audioUrl && autoPlay) {
      handlePlay()
    }
  }, [audioUrl])

  const handlePlay = async () => {
    if (!audioUrl) return

    try {
      setError(null)
      setIsPlaying(true)
      await playAudio(audioUrl)
      setIsPlaying(false)
    } catch (err) {
      setError('Failed to play audio')
      setIsPlaying(false)
      console.error(err)
    }
  }

  if (!audioUrl) return null

  return (
    <div className="audio-player">
      {error && <div className="error-message">{error}</div>}
      <button
        className="play-button"
        onClick={handlePlay}
        disabled={isPlaying}
        aria-label="Play audio"
      >
        {isPlaying ? '⏸ Playing...' : '▶ Play Response'}
      </button>
    </div>
  )
}

