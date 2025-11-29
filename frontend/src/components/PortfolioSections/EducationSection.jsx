import { resumeData } from '../../data/resumeData'
import '../../styles/Portfolio.css'
import { useEffect, useRef, useState } from 'react'

export const EducationSection = () => {
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
      id="education" 
      className={`portfolio-section education-section ${isVisible ? 'visible' : ''}`}
    >
      <h2 className="section-title">Education</h2>
      <div className="education-timeline">
        {resumeData.education.map((edu, index) => (
          <div key={index} className="education-item">
            <h3 className="education-degree">{edu.degree}</h3>
            {edu.specialization && (
              <p className="education-institution">{edu.specialization}</p>
            )}
            <p className="education-institution">{edu.institution}</p>
            <p className="education-period">{edu.period}</p>
            <p className="education-description">{edu.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

