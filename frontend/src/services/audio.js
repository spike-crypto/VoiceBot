export class AudioRecorder {
  constructor() {
    this.mediaRecorder = null
    this.audioChunks = []
    this.stream = null
  }

  async startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      this.stream = stream
      
      this.mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      })
      
      this.audioChunks = []
      
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data)
        }
      }
      
      this.mediaRecorder.start()
      return true
    } catch (error) {
      console.error('Error starting recording:', error)
      throw error
    }
  }

  stopRecording() {
    return new Promise((resolve, reject) => {
      if (!this.mediaRecorder || this.mediaRecorder.state === 'inactive') {
        reject(new Error('Recording not started'))
        return
      }

      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' })
        const audioFile = new File([audioBlob], 'recording.webm', { type: 'audio/webm' })
        
        // Stop all tracks
        if (this.stream) {
          this.stream.getTracks().forEach(track => track.stop())
        }
        
        resolve(audioFile)
      }

      this.mediaRecorder.stop()
    })
  }

  isRecording() {
    return this.mediaRecorder?.state === 'recording'
  }

  cancelRecording() {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop()
    }
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop())
    }
    this.audioChunks = []
  }
}

export const playAudio = (audioUrl) => {
  return new Promise((resolve, reject) => {
    const audio = new Audio(audioUrl)
    
    audio.onended = () => resolve()
    audio.onerror = (error) => reject(error)
    
    audio.play().catch(reject)
  })
}

