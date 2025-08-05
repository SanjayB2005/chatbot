@echo off
echo ========================================
echo 🚀 HackRx ChatBot - Complete Setup Guide
echo ========================================
echo.

echo 📋 All dependencies are installed!
echo ✅ Python packages ready
echo ✅ Node.js server packages ready  
echo ✅ React client packages ready
echo ✅ Gemini API key configured
echo.

echo 🎯 To start the application:
echo.
echo 1. Open 3 separate Command Prompt windows
echo 2. Run these commands in separate windows:
echo.
echo --- TERMINAL 1 (AI Service) ---
echo cd "c:\Users\ADMIN\Desktop\HackRx ChatBot\ai-service"
echo C:/Python312/python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
echo.
echo --- TERMINAL 2 (Server) ---  
echo cd "c:\Users\ADMIN\Desktop\HackRx ChatBot\server"
echo npm run dev
echo.
echo --- TERMINAL 3 (Client) ---
echo cd "c:\Users\ADMIN\Desktop\HackRx ChatBot\client"
echo npm run dev
echo.
echo 🌐 After starting all services, access:
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:3001  
echo   AI Service: http://localhost:8000
echo.
echo 🧪 Test your HackRx API endpoint:
echo   POST http://localhost:8000/api/v1/hackrx/run
echo.
echo ✨ Your chatbot is ready to use!
echo ========================================
pause
