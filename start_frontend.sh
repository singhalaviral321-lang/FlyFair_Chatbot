#!/bin/bash

# FlyFair Frontend Startup Script

echo "🚀 Starting FlyFair Frontend..."

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  No .env.local file found. Creating..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    echo "✅ Created .env.local file."
fi

# Start the development server
echo "🌟 Starting Next.js development server..."
echo "📍 App will be available at http://localhost:3000"
echo ""
npm run dev
