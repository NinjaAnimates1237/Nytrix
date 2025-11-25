#!/bin/bash

echo "🚀 Starting EchoForge Platform..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

# Install frontend dependencies if needed
if [ ! -d "client/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd client
    npm install
    cd ..
fi

# Start backend in background
echo "🔧 Starting backend server on port 6767..."
python run.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend on port 6767..."
cd client
npm run dev

# Cleanup on exit
trap "echo '🛑 Stopping servers...'; kill $BACKEND_PID 2>/dev/null; exit" INT TERM
