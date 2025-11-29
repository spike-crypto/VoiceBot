import { resumeData } from '../../data/resumeData'
import '../../styles/Portfolio.css'
import { useEffect, useRef, useState } from 'react'

export const ContactSection = ({ onScrollToChat }) => {
  const [isVisible, setIsVisible] = useState(false)
  const sectionRef = useRef(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1 }
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => {
      if (sectionRef.current) {
        observer.unobserve(sectionRef.current)
      }
    }
  }, [])

  return (
    <section 
      ref={sectionRef}
      id="contact" 
      className={`portfolio-section contact-section ${isVisible ? 'visible' : ''}`}
    >
      <h2 className="section-title">Get In Touch</h2>
      <div className="contact-content">
        <p className="section-content">
          Interested in learning more? Feel free to ask me anything through the chatbot above,
          or reach out through the links below.
        </p>
        <div className="contact-links">
          {resumeData.personal.email && (
            <a href={`mailto:${resumeData.personal.email}`} className="contact-link">
              Email
            </a>
          )}
          {resumeData.personal.linkedin && (
            <a href={resumeData.personal.linkedin} target="_blank" rel="noopener noreferrer" className="contact-link">
              LinkedIn
            </a>
          )}
          {resumeData.personal.github && (
            <a href={resumeData.personal.github} target="_blank" rel="noopener noreferrer" className="contact-link">
              GitHub
            </a>
          )}
          <button 
            className="contact-link" 
            onClick={onScrollToChat} 
            style={{ border: 'none', cursor: 'pointer' }}
            aria-label="Scroll to chatbot"
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault()
                onScrollToChat()
              }
            }}
          >
            Chat with Me
          </button>
        </div>
      </div>
    </section>
  )
}

