'use client'

interface ScenarioSelectorProps {
  onSelect: (scenario: string) => void
}

const scenarios = [
  {
    id: 'delay',
    title: 'Flight Delay',
    description: 'Delayed flights and your rights',
    query: 'What are my rights if my domestic flight is delayed?'
  },
  {
    id: 'cancellation',
    title: 'Flight Cancellation',
    description: 'Cancelled flights and compensation',
    query: 'What are my rights if my domestic flight is cancelled?'
  },
  {
    id: 'denied_boarding',
    title: 'Denied Boarding',
    description: 'Overbooking and denied boarding',
    query: 'What are my rights if I am denied boarding on a domestic flight?'
  },
  {
    id: 'refund',
    title: 'Refunds',
    description: 'Refund policies and timelines',
    query: 'What are my rights regarding refunds for domestic flights?'
  },
  {
    id: 'baggage',
    title: 'Baggage Issues',
    description: 'Lost, delayed, or damaged baggage',
    query: 'What are my rights if my baggage is lost or delayed on a domestic flight?'
  },
  {
    id: 'assistance',
    title: 'Special Assistance',
    description: 'Disabilities and special needs',
    query: 'What assistance is available for passengers with disabilities on domestic flights?'
  }
]

export default function ScenarioSelector({ onSelect }: ScenarioSelectorProps) {
  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">
        What can we help you with?
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {scenarios.map((scenario) => (
          <button
            key={scenario.id}
            onClick={() => onSelect(scenario.query)}
            className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow border border-gray-200 text-left"
          >
            <h3 className="text-lg font-semibold text-flyfair-blue mb-2">
              {scenario.title}
            </h3>
            <p className="text-gray-600 text-sm">{scenario.description}</p>
          </button>
        ))}
      </div>
    </div>
  )
}
