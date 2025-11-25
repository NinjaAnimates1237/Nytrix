#!/bin/bash

# Kill any existing processes
echo "Stopping existing servers..."
lsof -ti:6767 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
pkill -f "python run.py" 2>/dev/null
pkill -f "vite" 2>/dev/null

# Wait a moment
sleep 2

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Build React frontend
echo "Building React frontend..."
cd client
npm run build
cd ..

# Start Flask server (which now serves the React build)
echo "Starting Flask server on http://localhost:6767..."
python run.py
