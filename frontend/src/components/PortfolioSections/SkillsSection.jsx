import { resumeData } from '../../data/resumeData'
import '../../styles/Portfolio.css'
import { useEffect, useRef, useState } from 'react'

export const SkillsSection = () => {
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
      id="skills" 
      className={`portfolio-section skills-section ${isVisible ? 'visible' : ''}`}
    >
      <h2 className="section-title">Skills</h2>
      <div className="skills-grid">
        {Object.entries(resumeData.skills).map(([category, skills]) => (
          <div key={category} className="skill-category">
            <h3 className="skill-category-title">{category}</h3>
            <div className="skill-tags">
              {skills.map((skill, index) => (
                <span key={index} className="skill-tag">{skill}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

