'use client'

import { useState, useRef, useEffect } from 'react'
import Image from 'next/image'
import ChatInterface from '@/components/ChatInterface'
import ScenarioSelector from '@/components/ScenarioSelector'
import GuidedButtons from '@/components/GuidedButtons'

export default function Home() {
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null)
  const [manualQuery, setManualQuery] = useState('')
  const [showChat, setShowChat] = useState(false)



  const handleScenarioSelect = (scenario: string) => {
    setSelectedScenario(scenario)
    setShowChat(true)
  }

  const handleGuidedButtonClick = (query: string) => {
    setSelectedScenario(query)
    setShowChat(true)
  }

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header with Logo */}
      <header className="bg-flyfair-blue text-flyfair-white py-4 px-4 shadow-md">
        <div className="max-w-4xl mx-auto flex items-center justify-center gap-3">
          <div className="flex items-center gap-2">
            <div className="relative w-12 h-8 flex items-center justify-center">
              <Image
                src="/logo.png"
                alt="FlyFair Logo"
                fill
                className="object-contain"
                priority
              />
            </div>
            <h1 className="text-xl md:text-2xl font-bold">FlyFair</h1>
          </div>
        </div>
        <p className="text-center text-sm mt-1 opacity-90">
          Because flying should be fair.
        </p>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-6">
      {!showChat ? (
        <>
          {/* Search Bar */}
          <div className="mb-6">
            <div className="flex gap-2">
              <input
                type="text"
                value={manualQuery}
                onChange={(e) => setManualQuery(e.target.value)}
                placeholder="Ask about your flight issue..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-flyfair-blue"
              />

              {manualQuery && (
                <button
                  onClick={() => {
                    setManualQuery('')
                    setSelectedScenario(null)
                  }}
                  className="px-3 text-gray-500 hover:text-gray-800"
                  aria-label="Clear"
                >
                  ✕
                </button>
              )}

              <button
                onClick={() => {
                  setSelectedScenario(manualQuery)
                  setShowChat(true)
                }}
                disabled={!manualQuery.trim()}
                className="px-4 py-3 bg-flyfair-blue text-white rounded-lg disabled:opacity-50"
              >
                Ask
              </button>
            </div>
          </div>

          {/* Scenario Selector Cards */}
          <ScenarioSelector onSelect={handleScenarioSelect} />

          {/* Guided Buttons */}
          <GuidedButtons onButtonClick={handleGuidedButtonClick} />
        </>
      ) : (
          <ChatInterface
            initialQuery={selectedScenario || ''}
            onBack={() => setShowChat(false)}
          />
        )}
      </div>
    </main>
  )
}
