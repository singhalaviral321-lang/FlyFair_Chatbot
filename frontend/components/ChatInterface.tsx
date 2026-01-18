'use client'

import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ChatInterfaceProps {
  initialQuery?: string
  onBack?: () => void
}

export default function ChatInterface({ initialQuery = '', onBack }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState(initialQuery)
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    if (initialQuery) {
      handleSend(initialQuery)
    }
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSend = async (query?: string) => {
    const userMessage = query || input.trim()
    if (!userMessage) return

    // Add user message
    const newUserMessage: Message = {
      role: 'user',
      content: userMessage,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, newUserMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await axios.post(`${API_URL}/query`, {
        query: userMessage,
        use_llm: false  // RAG-only mode for production
      })

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const formatResponse = (text: string) => {
    // Parse the structured response format
    const sections = text.split(/\n(?=Applicable Scenario:|Conditions:|Passenger Rights:|Source:)/)
    const formatted: { [key: string]: string } = {}

    sections.forEach(section => {
      const lines = section.split('\n').filter(l => l.trim())
      if (lines.length > 0) {
        const header = lines[0].replace(':', '').trim()
        const content = lines.slice(1).join('\n').trim()
        if (header && content) {
          formatted[header] = content
        }
      }
    })

    return formatted
  }

  return (
    <div className="flex flex-col h-[calc(100vh-180px)] max-h-[800px]">
      {/* Back Button */}
      {onBack && (
        <button
          onClick={onBack}
          className="mb-4 text-flyfair-blue hover:underline flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            Ask me about your rights as an Indian domestic air passenger
          </div>
        )}

        {messages.map((message, idx) => (
          <div
            key={idx}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] md:max-w-[70%] rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-flyfair-blue text-white'
                  : 'bg-white border border-gray-200 shadow-sm'
              }`}
            >
              {message.role === 'assistant' ? (
                <div className="space-y-3">
                  {message.content === 'This is out of my Scope.' ? (
                    <p className="text-gray-600 italic">{message.content}</p>
                  ) : (
                    (() => {
                      const formatted = formatResponse(message.content)
                      return (
                        <>
                          {formatted['Applicable Scenario'] && (
                            <div>
                              <h4 className="font-semibold text-flyfair-blue mb-1">
                                Applicable Scenario:
                              </h4>
                              <p className="text-gray-700">
                                {formatted['Applicable Scenario']}
                              </p>
                            </div>
                          )}
                          {formatted['Conditions'] && (
                            <div>
                              <h4 className="font-semibold text-flyfair-blue mb-1">
                                Conditions:
                              </h4>
                              <p className="text-gray-700">{formatted['Conditions']}</p>
                            </div>
                          )}
                          {formatted['Passenger Rights'] && (
                            <div>
                              <h4 className="font-semibold text-flyfair-blue mb-1">
                                Passenger Rights:
                              </h4>
                              <p className="text-gray-700">{formatted['Passenger Rights']}</p>
                            </div>
                          )}
                          {formatted['Source'] && (
                            <div className="pt-2 border-t border-gray-200">
                              <p className="text-sm text-gray-500">
                                <span className="font-semibold">Source:</span>{' '}
                                {formatted['Source']}
                              </p>
                            </div>
                          )}
                          {Object.keys(formatted).length === 0 && (
                            <p className="text-gray-700 whitespace-pre-wrap">{message.content}</p>
                          )}
                        </>
                      )
                    })()
                  )}
                </div>
              ) : (
                <p className="whitespace-pre-wrap">{message.content}</p>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg px-4 py-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about your rights..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-flyfair-blue focus:border-transparent"
          disabled={isLoading}
        />
        <button
          onClick={() => handleSend()}
          disabled={isLoading || !input.trim()}
          className="px-6 py-3 bg-flyfair-blue text-white rounded-lg hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          Send
        </button>
      </div>
    </div>
  )
}
