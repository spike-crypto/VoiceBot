import { ConversationProvider } from './context/ConversationContext'
import VoiceBot from './components/VoiceBot/VoiceBot'
import './App.css'

const App = () => {
  return (
    <ConversationProvider>
      <VoiceBot />
    </ConversationProvider>
  )
}

export default App
