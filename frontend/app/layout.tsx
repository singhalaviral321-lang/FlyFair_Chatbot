import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'FlyFair - Because flying should be fair',
  description: 'Know your rights as an Indian domestic air passenger',
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
