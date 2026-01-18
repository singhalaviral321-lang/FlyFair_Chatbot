'use client'

interface GuidedButtonsProps {
  onButtonClick: (query: string) => void
}

const guidedQueries = [
  'My flight is delayed by 3 hours',
  'My flight was cancelled',
  'I was denied boarding',
  'I want a refund',
  'My baggage is lost'
]

export default function GuidedButtons({ onButtonClick }: GuidedButtonsProps) {
  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">
        Quick Questions
      </h3>
      <div className="flex flex-wrap gap-2">
        {guidedQueries.map((query, idx) => (
          <button
            key={idx}
            onClick={() => onButtonClick(query)}
            className="px-4 py-2 bg-white border border-gray-300 rounded-full text-sm text-gray-700 hover:bg-flyfair-blue hover:text-white hover:border-flyfair-blue transition-colors"
          >
            {query}
          </button>
        ))}
      </div>
    </div>
  )
}
