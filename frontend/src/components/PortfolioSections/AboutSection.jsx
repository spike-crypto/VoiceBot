import { resumeData } from '../../data/resumeData'
import '../../styles/Portfolio.css'
import { useEffect, useRef, useState } from 'react'

export const AboutSection = () => {
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
      id="about" 
      className={`portfolio-section about-section ${isVisible ? 'visible' : ''}`}
    >
      <h2 className="section-title">About Me</h2>
      <div className="about-content">
        <div className="about-card">
          <h3 className="about-card-title">Life Story</h3>
          <p className="about-card-content">{resumeData.about.lifeStory}</p>
        </div>
        <div className="about-card">
          <h3 className="about-card-title">#1 Superpower</h3>
          <p className="about-card-content">{resumeData.about.superpower}</p>
        </div>
        <div className="about-card">
          <h3 className="about-card-title">Beyond the Code</h3>
          <p className="about-card-content">{resumeData.about.misconception}</p>
        </div>
        <div className="about-card">
          <h3 className="about-card-title">Pushing Boundaries</h3>
          <p className="about-card-content">{resumeData.about.boundaryPushing}</p>
        </div>
      </div>
    </section>
  )
}

