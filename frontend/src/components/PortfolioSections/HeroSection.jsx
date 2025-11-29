import { resumeData } from '../../data/resumeData'
import '../../styles/Portfolio.css'

export const HeroSection = ({ onScrollToChat }) => {
  return (
    <section className="hero-section">
      <div className="hero-background"></div>
      <div className="hero-content">
        <h1 className="hero-name">{resumeData.personal.name}</h1>
        <p className="hero-title">{resumeData.personal.title}</p>
        <p className="hero-description">
          Building AI-powered solutions that bridge enterprise systems with cutting-edge LLMs.
          Ask me anything about my experience, projects, or skills!
        </p>
        <button 
          className="hero-cta" 
          onClick={onScrollToChat}
          aria-label="Scroll to chatbot to start conversation"
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault()
              onScrollToChat()
            }
          }}
        >
          Start Conversation
        </button>
      </div>
    </section>
  )
}

