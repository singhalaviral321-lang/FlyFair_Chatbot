'use client'

import { useState, useRef, useEffect } from 'react'
import Image from 'next/image'
import ChatInterface from '@/components/ChatInterface'
import ScenarioSelector from '@/components/ScenarioSelector'
import GuidedButtons from '@/components/GuidedButtons'

export default function Home() {
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null)
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
            <div className="w-10 h-10 flex items-center justify-center">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="w-8 h-8"
              >
                <path d="M12 2L2 7l10 5 10-5-10-5z" />
                <path d="M2 17l10 5 10-5" />
                <path d="M2 12l10 5 10-5" />
              </svg>
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
