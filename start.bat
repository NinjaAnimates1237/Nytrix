@echo off
echo Starting EchoForge Platform...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install backend dependencies
echo Installing backend dependencies...
pip install -q -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

REM Install frontend dependencies if needed
if not exist "client\node_modules" (
    echo Installing frontend dependencies...
    cd client
    call npm install
    cd ..
)

REM Start backend
echo Starting backend server on port 6767...
start /B python run.py

REM Wait for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend
echo Starting frontend on port 6767...
cd client
call npm run dev
