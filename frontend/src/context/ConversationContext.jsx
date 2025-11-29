import { createContext, useContext } from 'react'
import { useConversation } from '../hooks/useConversation'

const ConversationContext = createContext(null)

export const ConversationProvider = ({ children }) => {
  const conversation = useConversation()

  return (
    <ConversationContext.Provider value={conversation}>
      {children}
    </ConversationContext.Provider>
  )
}

export const useConversationContext = () => {
  const context = useContext(ConversationContext)
  if (!context) {
    throw new Error('useConversationContext must be used within ConversationProvider')
  }
  return context
}

