import { useState, useEffect, useRef } from 'react'
import { useConversationContext } from '../../context/ConversationContext'
import { chatAPI } from '../../services/api'
import './VoiceBot.css'
import './VoiceBot-additions.css'
import './VoiceBot-mobile.css'

const VoiceBot = () => {
    const { messages, addMessage, sessionId, clearConversation } = useConversationContext()
    const [isListening, setIsListening] = useState(false)
    const [isSpeaking, setIsSpeaking] = useState(false)
    const [isThinking, setIsThinking] = useState(false)
    const [transcript, setTranscript] = useState('')
    const [mode, setMode] = useState('voice')
    const [textInput, setTextInput] = useState('')
    const [error, setError] = useState(null)

    const audioRef = useRef(null)
    const recognitionRef = useRef(null)

    useEffect(() => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
            recognitionRef.current = new SpeechRecognition()
            recognitionRef.current.continuous = false
            recognitionRef.current.interimResults = true
            recognitionRef.current.lang = 'en-US'

            recognitionRef.current.onresult = (event) => {
                const current = event.resultIndex
                const transcriptText = event.results[current][0].transcript
                setTranscript(transcriptText)

                if (event.results[current].isFinal) {
                    handleVoiceInput(transcriptText)
                }
            }

            recognitionRef.current.onerror = (event) => {
                console.error('Speech recognition error:', event.error)
                setError('Voice recognition failed. Try switching to text mode below.')
                setIsListening(false)
            }

            recognitionRef.current.onend = () => {
                setIsListening(false)
            }
        }
    }, [])

    const startListening = () => {
        if (!recognitionRef.current) {
            setError('Speech recognition not supported. Please use text mode.')
            return
        }

        setError(null)
        setTranscript('')
        setIsListening(true)

        try {
            recognitionRef.current.start()
        } catch (err) {
            console.error('Error starting recognition:', err)
            setError('Could not start voice recognition. Try text mode.')
            setIsListening(false)
        }
    }

    const stopListening = () => {
        if (recognitionRef.current && isListening) {
            recognitionRef.current.stop()
        }
    }

    const handleVoiceInput = async (text) => {
        if (!text.trim()) return

        setIsListening(false)
        setTranscript('')
        setIsThinking(true)
        addMessage('user', text)

        try {
            const response = await chatAPI.sendMessage(text, sessionId)
            setIsThinking(false)
            addMessage('assistant', response.response)
            await speakResponse(response.response)
        } catch (err) {
            console.error('Error processing voice input:', err)
            setIsThinking(false)
            setError('Voice processing failed. Please switch to text mode for a better experience.')
            addMessage('assistant', 'Sorry, I encountered an error. Please try text mode.')
        }
    }

    const speakResponse = async (text) => {
        setIsSpeaking(true)

        try {
            const audioBlob = await chatAPI.textToSpeech(text)
            const audioUrl = URL.createObjectURL(audioBlob)

            if (audioRef.current) {
                audioRef.current.src = audioUrl
                audioRef.current.onended = () => {
                    setIsSpeaking(false)
                    URL.revokeObjectURL(audioUrl)
                }
                await audioRef.current.play()
            }
        } catch (err) {
            console.error('Error speaking response:', err)
            setIsSpeaking(false)
            setError('Text-to-speech failed. The response is shown in the conversation panel.')
        }
    }

    const stopSpeaking = () => {
        if (audioRef.current) {
            audioRef.current.pause()
            audioRef.current.currentTime = 0
            setIsSpeaking(false)
        }
    }

    const handleTextSubmit = async (e) => {
        e.preventDefault()
        if (!textInput.trim()) return

        const text = textInput
        setTextInput('')
        setIsThinking(true)
        addMessage('user', text)

        try {
            const response = await chatAPI.sendMessage(text, sessionId)
            setIsThinking(false)
            addMessage('assistant', response.response)
        } catch (err) {
            console.error('Error processing text input:', err)
            setIsThinking(false)
            setError('Failed to process your message. Please try again.')
            addMessage('assistant', 'Sorry, I encountered an error. Please try again.')
        }
    }

    const toggleMode = () => {
        setMode(mode === 'voice' ? 'text' : 'voice')
        setError(null)
    }

    const handleClearChat = async () => {
        if (window.confirm('Are you sure you want to clear the conversation?')) {
            await clearConversation()
        }
    }

    return (
        <div className="voice-bot">
            <audio ref={audioRef} style={{ display: 'none' }} />

            <div className="voice-bot__background">
                <div className="voice-bot__orb voice-bot__orb--1"></div>
                <div className="voice-bot__orb voice-bot__orb--2"></div>
                <div className="voice-bot__orb voice-bot__orb--3"></div>
            </div>

            <div className="voice-bot__container">

                <div className="voice-bot__header">
                    <h1 className="voice-bot__title">Balamurugan Nithyanantham</h1>
                    <p className="voice-bot__subtitle">AI/ML Engineer - Voice Interview Bot</p>
                </div>

                <div className="voice-bot__status">
                    {isListening && (
                        <div className="voice-bot__status-badge voice-bot__status-badge--listening">
                            <span className="voice-bot__status-dot"></span>
                            Listening...
                        </div>
                    )}
                    {isThinking && (
                        <div className="voice-bot__status-badge voice-bot__status-badge--thinking">
                            <span className="voice-bot__status-dot"></span>
                            Thinking...
                        </div>
                    )}
                    {isSpeaking && (
                        <div className="voice-bot__status-badge voice-bot__status-badge--speaking">
                            <span className="voice-bot__status-dot"></span>
                            Speaking...
                            <button onClick={stopSpeaking} className="voice-bot__stop-btn">Stop</button>
                        </div>
                    )}
                    {!isListening && !isSpeaking && !isThinking && (
                        <div className="voice-bot__status-badge voice-bot__status-badge--idle">
                            <span className="voice-bot__status-dot"></span>
                            Ready
                        </div>
                    )}
                </div>

                {transcript && (
                    <div className="voice-bot__transcript">
                        <p>{transcript}</p>
                    </div>
                )}

                {error && (
                    <div className="voice-bot__error">
                        <p>{error}</p>
                        {mode === 'voice' && (
                            <button onClick={toggleMode} className="voice-bot__error-action">
                                Switch to Text Mode
                            </button>
                        )}
                    </div>
                )}

                <div className="voice-bot__visualizer">
                    {mode === 'voice' ? (
                        <button
                            className={`voice-bot__mic-button ${isListening ? 'voice-bot__mic-button--active' : ''} ${isSpeaking ? 'voice-bot__mic-button--speaking' : ''} ${isThinking ? 'voice-bot__mic-button--thinking' : ''}`}
                            onClick={isListening ? stopListening : startListening}
                            disabled={isSpeaking || isThinking}
                        >
                            <div className="voice-bot__mic-icon">
                                {isListening ? (
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <rect x="6" y="6" width="12" height="12" rx="2" />
                                    </svg>
                                ) : (
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                                        <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                                        <line x1="12" y1="19" x2="12" y2="23" />
                                        <line x1="8" y1="23" x2="16" y2="23" />
                                    </svg>
                                )}
                            </div>
                            <div className="voice-bot__ripple"></div>
                            <div className="voice-bot__ripple voice-bot__ripple--delay"></div>
                        </button>
                    ) : (
                        <form onSubmit={handleTextSubmit} className="voice-bot__text-form">
                            <input
                                type="text"
                                value={textInput}
                                onChange={(e) => setTextInput(e.target.value)}
                                placeholder="Type your message..."
                                className="voice-bot__text-input"
                                disabled={isThinking}
                                autoFocus
                            />
                            <button type="submit" className="voice-bot__send-button" disabled={isThinking}>
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <line x1="22" y1="2" x2="11" y2="13" />
                                    <polygon points="22 2 15 22 11 13 2 9 22 2" />
                                </svg>
                            </button>
                        </form>
                    )}
                </div>

                <div className="voice-bot__mode-toggle">
                    <button onClick={toggleMode} className="voice-bot__toggle-button">
                        {mode === 'voice' ? (
                            <>
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                                </svg>
                                Switch to Text
                            </>
                        ) : (
                            <>
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                                    <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                                </svg>
                                Switch to Voice
                            </>
                        )}
                    </button>
                </div>

                {messages.length > 0 && (
                    <div className="voice-bot__messages">
                        <div className="voice-bot__messages-header">
                            <h3>Conversation</h3>
                            <button onClick={handleClearChat} className="voice-bot__clear-btn" title="Clear conversation">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <polyline points="3 6 5 6 21 6" />
                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                                </svg>
                            </button>
                        </div>
                        <div className="voice-bot__messages-list">
                            {messages.map((msg, idx) => (
                                <div key={idx} className={`voice-bot__message voice-bot__message--${msg.role}`}>
                                    <div className="voice-bot__message-content">
                                        {msg.content}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {messages.length === 0 && (
                    <div className="voice-bot__instructions">
                        <p>
                            {mode === 'voice'
                                ? 'Click the microphone to start talking. I\'ll listen and respond automatically.'
                                : 'Type your message and press Enter or click Send.'}
                        </p>
                    </div>
                )}
            </div>
        </div>
    )
}

export default VoiceBot
