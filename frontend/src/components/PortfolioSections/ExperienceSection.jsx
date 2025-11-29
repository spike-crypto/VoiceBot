import { resumeData } from '../../data/resumeData'
import '../../styles/Portfolio.css'
import { useEffect, useRef, useState } from 'react'

export const ExperienceSection = () => {
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
      id="experience" 
      className={`portfolio-section experience-section ${isVisible ? 'visible' : ''}`}
    >
      <h2 className="section-title">Experience</h2>
      <div className="experience-timeline">
        {resumeData.experience.map((exp, index) => (
          <div key={index} className="experience-item">
            <div className="experience-header">
              <div>
                <h3 className="experience-title">{exp.title}</h3>
                <p className="experience-company">{exp.company}</p>
              </div>
              <p className="experience-period">{exp.period}</p>
            </div>
            <p className="experience-description">{exp.description}</p>
            <div className="experience-tech">
              {exp.technologies && exp.technologies.length > 0 && (
                <div className="experience-tech">
                  {exp.technologies.map((tech, techIndex) => (
                    <span key={techIndex} className="tech-tag">{tech}</span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

