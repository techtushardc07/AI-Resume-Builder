import { useState, useRef, useEffect } from 'react'
import './App.css'
import { v4 as uuidv4 } from 'uuid'

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I'm your Learning Assistant. I'm here to help you with Academic Support, Skill Development, or Mental & Learning Wellbeing. How can I assist you today?"
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const sessionIdRef = useRef(uuidv4())

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setLoading(true)

    // Add user message to UI
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])

    try {
      const response = await fetch(
        "https://ai-powered-resume-builder-3l98.onrender.com/chat",
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: userMessage,
            session_id: sessionIdRef.current
          }),
        }
      )
      

      if (!response.ok) {
        throw new Error('Failed to send message')
      }

      const data = await response.json()
      
      // Add assistant response to UI
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const startNewConversation = () => {
    // Generate new session ID
    sessionIdRef.current = uuidv4()

    // Reset messages to initial greeting
    setMessages([
      {
        role: 'assistant',
        content: "Hello! I'm your Learning Assistant. I'm here to help you with Academic Support, Skill Development, or Mental & Learning Wellbeing. How can I assist you today?"
      }
    ])

    // Clear input
    setInput('')

    // Stop any loading state
    setLoading(false)
  }

  return (
    <div className="app">
      <div className="chat-container">
        <div className="chat-header">
          <div className="header-content">
            <div>
              <h1>🎓 Learning Assistant</h1>
              <p>Supporting SDG 4 - Quality Education</p>
            </div>
            <button
              onClick={startNewConversation}
              className="new-user-button"
              title="Start new conversation"
            >
              New User
            </button>
          </div>
        </div>

        <div className="messages-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
            >
              <div className="message-content">
                {message.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message assistant-message">
              <div className="message-content">
                <span className="typing-indicator">...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            disabled={loading}
            className="message-input"
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="send-button"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  )
}

export default App
