@echo off
echo 🚀 Starting HackRx ChatBot Application...

REM Function to check if command exists
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

REM Setup AI Service
echo 🐍 Setting up AI Service...
cd ai-service

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt

if not exist ".env" (
    echo Creating .env file for AI service...
    copy .env.example .env
    echo ⚠️  Please edit ai-service\.env and add your GEMINI_API_KEY
)

echo ✅ AI Service setup complete!
cd ..

REM Setup Server
echo 🖥️  Setting up Server...
cd server

if not exist "node_modules" (
    echo Installing server dependencies...
    npm install
)

if not exist ".env" (
    echo Creating .env file for server...
    copy .env.example .env
    echo ⚠️  Please edit server\.env with your MongoDB URI if needed
)

echo ✅ Server setup complete!
cd ..

REM Setup Client
echo ⚛️  Setting up Client...
cd client

if not exist "node_modules" (
    echo Installing client dependencies...
    npm install
)

if not exist ".env" (
    echo Creating .env file for client...
    copy .env.example .env
)

echo ✅ Client setup complete!
cd ..

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Edit ai-service\.env and add your GEMINI_API_KEY
echo 2. Make sure MongoDB is running (or update server\.env with your MongoDB URI)
echo 3. Run the application using the start script:
echo.
echo    start.bat
echo.
echo Or start each service manually:
echo    Terminal 1: cd ai-service ^&^& venv\Scripts\activate.bat ^&^& uvicorn main:app --reload
echo    Terminal 2: cd server ^&^& npm run dev
echo    Terminal 3: cd client ^&^& npm run dev
echo.
echo 🌐 Access the application at: http://localhost:5173
pause
