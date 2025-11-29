import { useState, useRef, useCallback } from 'react'
import { AudioRecorder } from '../services/audio'

export const useAudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const recorderRef = useRef(null)
  const timerRef = useRef(null)

  const startRecording = useCallback(async () => {
    try {
      const recorder = new AudioRecorder()
      await recorder.startRecording()
      recorderRef.current = recorder
      setIsRecording(true)
      setRecordingTime(0)

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1)
      }, 1000)
    } catch (error) {
      console.error('Error starting recording:', error)
      throw error
    }
  }, [])

  const stopRecording = useCallback(async () => {
    if (!recorderRef.current) {
      return null
    }

    try {
      const audioFile = await recorderRef.current.stopRecording()
      setIsRecording(false)
      
      if (timerRef.current) {
        clearInterval(timerRef.current)
        timerRef.current = null
      }
      
      recorderRef.current = null
      return audioFile
    } catch (error) {
      console.error('Error stopping recording:', error)
      setIsRecording(false)
      if (timerRef.current) {
        clearInterval(timerRef.current)
        timerRef.current = null
      }
      throw error
    }
  }, [])

  const cancelRecording = useCallback(() => {
    if (recorderRef.current) {
      recorderRef.current.cancelRecording()
      recorderRef.current = null
    }
    setIsRecording(false)
    setRecordingTime(0)
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
  }, [])

  return {
    isRecording,
    recordingTime,
    startRecording,
    stopRecording,
    cancelRecording
  }
}

