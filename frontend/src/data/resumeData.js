// Centralized resume data extracted from backend system prompt
// This data is used for both displaying portfolio sections and chatbot context

export const resumeData = {
  personal: {
    name: "Balamurugan Nithyanantham",
    title: "AI/ML Engineer",
    location: "Tiruchirappalli, Tamil Nadu, India",
    email: "", // Add if available
    linkedin: "", // Add if available
    github: "", // Add if available
  },

  about: {
    lifeStory: "I'm Balamurugan Nithyanantham, originally from Tiruchirappalli in central Tamil Nadu, where I grew up and earned my Bachelor's in Mechanical Engineering. After graduation, I headed to Germany for a Master's in Engineering Management with a Big Data specialization at IU International University, diving into data workflows with manufacturing and ERP companies as a working student— that's where I picked up fluent German and got hooked on AI's potential, inspired by visions like Jarvis from Iron Man. Due to family financial challenges, I returned to India, but that pivot fueled my shift to Gen AI; now, as an intern at IT Resonance, I'm building multi-agent systems for SAP integrations, while personally developing VentSpace—a mental health venting app aiming to make therapy accessible and eventually replace traditional psychiatrists with AI-driven balance tools. I'm thrilled about teams like 100x that see AI's future in seamless automation.",
    superpower: "My superpower is rapidly prototyping AI workflows that bridge enterprise systems like SAP with cutting-edge LLMs—whether it's fine-tuning Qwen for code generation or chaining RAG pipelines with n8n for invoice automation, I thrive on turning complex integrations into efficient, scalable solutions under tight deadlines.",
    misconception: "My coworkers often see me as the quiet data wizard buried in code and pipelines, but they miss how much I'm an idea generator at heart—fueled by late-night brainstorming on projects like VentSpace, where I blend tech with empathy to tackle real human challenges.",
    boundaryPushing: "I push my limits by committing to one 'moonshot' side project per quarter, like building VentSpace from scratch with FastAPI, React, and agentic RAG— it forces me to learn new tools weekly, cold-email open-source contributors for feedback, and iterate based on user tests, turning discomfort into breakthroughs."
  },

  education: [
    {
      degree: "Master's in Engineering Management",
      specialization: "Big Data",
      institution: "IU International University",
      location: "Germany",
      period: "2022-2024",
      description: "Specialized in Big Data, worked as a working student with manufacturing and ERP companies, diving into data workflows. Gained fluency in German and developed passion for AI."
    },
    {
      degree: "Bachelor's in Mechanical Engineering",
      institution: "Tiruchirappalli",
      location: "Tamil Nadu, India",
      period: "2018-2022",
      description: "Earned Bachelor's degree in Mechanical Engineering from my hometown."
    }
  ],

  experience: [
    {
      title: "AI Engineer Intern",
      company: "IT Resonance",
      location: "India",
      period: "July 2025 - Present",
      description: "Building multi-agent systems for SAP integrations. Fine-tuned LLMs like Mistral-7B and Qwen 2.5 Coder using PEFT/LoRA for SAP Fiori triage. Built end-to-end RAG systems with LangChain, Supabase vectors, and Neo4j graphs. Developed AI invoice automation via n8n/OCR and continuous learning pipelines, integrating with SAP CPI/CAPM.",
      technologies: ["Mistral-7B", "Qwen 2.5 Coder", "PEFT/LoRA", "LangChain", "Supabase", "Neo4j", "n8n", "SAP Fiori", "SAP CPI/CAPM", "RAG Systems"]
    },
    {
      title: "Working Student",
      company: "Manufacturing and ERP Companies",
      location: "Germany",
      period: "2022-2024",
      description: "Worked with manufacturing and ERP companies during Master's program, diving into data workflows and gaining practical experience in enterprise systems."
    }
  ],

  skills: {
    "AI/ML": [
      "LLM Fine-tuning (PEFT/LoRA)",
      "RAG Systems",
      "Multi-agent Systems",
      "LangChain",
      "LangGraph",
      "Vector Databases (Supabase)",
      "Graph Databases (Neo4j)",
      "Model Monitoring",
      "MLOps"
    ],
    "Backend": [
      "FastAPI",
      "Python",
      "SAP Integrations",
      "SAP CPI/CAPM",
      "SAP Fiori",
      "REST APIs",
      "WebSocket"
    ],
    "Frontend": [
      "React",
      "JavaScript",
      "CSS",
      "HTML"
    ],
    "Tools & Platforms": [
      "n8n",
      "OCR",
      "Docker",
      "Git",
      "Whisper (STT)",
      "gTTS (TTS)"
    ],
    "Languages": [
      "English",
      "German (Fluent)",
      "Tamil"
    ]
  },

  projects: [
    {
      name: "VentSpace",
      description: "A mental health venting app aiming to make therapy accessible and eventually replace traditional psychiatrists with AI-driven balance tools. Built from scratch with FastAPI, React, and agentic RAG.",
      technologies: ["FastAPI", "React", "RAG", "AI"],
      period: "2024 - Present",
      highlights: [
        "Moonshot side project built from scratch",
        "Blends tech with empathy to tackle real human challenges",
        "Uses agentic RAG for AI-driven mental health support"
      ]
    },
    {
      name: "SAP Multi-Agent Systems",
      description: "Built multi-agent systems for SAP integrations at IT Resonance, enabling autonomous agents that automate enterprise workflows.",
      technologies: ["LangChain", "Multi-agent Systems", "SAP", "Python"],
      period: "2025 - Present",
      highlights: [
        "Fine-tuned LLMs for SAP Fiori triage",
        "End-to-end RAG systems with vector and graph databases",
        "AI invoice automation via n8n/OCR"
      ]
    },
    {
      name: "AI Invoice Automation",
      description: "Developed continuous learning pipelines for invoice automation, integrating OCR with n8n workflows and SAP systems.",
      technologies: ["n8n", "OCR", "SAP CPI", "RAG", "Continuous Learning"],
      period: "2025",
      highlights: [
        "Automated invoice processing",
        "Integrated with SAP enterprise systems",
        "Continuous learning capabilities"
      ]
    }
  ],

  growthAreas: [
    "Multi-agent orchestration for collaborative AI systems, like scaling LangGraph workflows in production.",
    "Advanced MLOps for model monitoring and drift detection in real-world deployments.",
    "Ethical AI frameworks, ensuring bias mitigation in sensitive apps like mental health tools."
  ],

  interests: [
    "AI Automation",
    "Enterprise AI Integration",
    "Mental Health Technology",
    "Open Source Contribution",
    "Rapid Prototyping"
  ]
}

// Helper function to get all text content for chatbot context
export const getResumeContext = () => {
  return `
Personal Information:
- Name: ${resumeData.personal.name}
- Title: ${resumeData.personal.title}
- Location: ${resumeData.personal.location}

About:
- Life Story: ${resumeData.about.lifeStory}
- Superpower: ${resumeData.about.superpower}
- Misconception: ${resumeData.about.misconception}
- Boundary Pushing: ${resumeData.about.boundaryPushing}

Education:
${resumeData.education.map(edu => `- ${edu.degree} from ${edu.institution} (${edu.period}): ${edu.description}`).join('\n')}

Experience:
${resumeData.experience.map(exp => `- ${exp.title} at ${exp.company} (${exp.period}): ${exp.description}`).join('\n')}

Skills:
${Object.entries(resumeData.skills).map(([category, skills]) => `${category}: ${skills.join(', ')}`).join('\n')}

Projects:
${resumeData.projects.map(proj => `- ${proj.name}: ${proj.description}`).join('\n')}

Growth Areas:
${resumeData.growthAreas.map((area, i) => `${i + 1}. ${area}`).join('\n')}
  `.trim()
}

