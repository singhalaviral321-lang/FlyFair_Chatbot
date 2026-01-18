#!/bin/bash

# FlyFair Backend Startup Script

echo "🚀 Starting FlyFair Backend..."

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it if needed."
    fi
fi

# Start the server
echo "🌟 Starting FastAPI server..."
echo "📍 API will be available at http://localhost:8000"
echo "📚 API docs at http://localhost:8000/docs"
echo ""
python main.py
