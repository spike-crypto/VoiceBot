import { useEffect } from 'react'
import resumeData from '../../resume_text.json'

export const ResumeModal = ({ isOpen, onClose }) => {
    if (!isOpen) return null

    useEffect(() => {
        const handleEscape = (e) => {
            if (e.key === 'Escape') onClose()
        }
        window.addEventListener('keydown', handleEscape)
        return () => window.removeEventListener('keydown', handleEscape)
    }, [onClose])

    return (
        <div className="resume-modal-backdrop" onClick={onClose}>
            <div className="resume-modal" onClick={(e) => e.stopPropagation()}>
                <div className="resume-modal-header">
                    <h2>My Resume</h2>
                    <button className="close-btn" onClick={onClose}>×</button>
                </div>
                <pre className="resume-text">{resumeData.resume}</pre>
            </div>
        </div>
    )
}
