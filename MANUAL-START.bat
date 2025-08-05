@echo off
echo ========================================
echo    🚀 HackRx ChatBot Startup Guide
echo ========================================
echo.
echo This will start all three services for your chatbot:
echo 1. AI Service (Python/FastAPI) - Port 8000
echo 2. Server (Node.js/Express) - Port 3001  
echo 3. Client (React/Vite) - Port 5173
echo.
echo ========================================
echo Step 1: Starting AI Service...
echo ========================================
echo.
echo Open a NEW command prompt and run:
echo cd "c:\Users\ADMIN\Desktop\HackRx ChatBot\ai-service"
echo C:\Python312\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
echo.
pause
echo.
echo ========================================
echo Step 2: Starting Server...
echo ========================================
echo.
echo Open ANOTHER command prompt and run:
echo cd "c:\Users\ADMIN\Desktop\HackRx ChatBot\server"
echo npm run dev
echo.
pause
echo.
echo ========================================
echo Step 3: Starting Client...
echo ========================================
echo.
echo Open a THIRD command prompt and run:
echo cd "c:\Users\ADMIN\Desktop\HackRx ChatBot\client"
echo npm run dev
echo.
pause
echo.
echo ========================================
echo 🎉 Your HackRx ChatBot will be running on:
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:3001
echo AI Service: http://localhost:8000
echo.
echo Press any key to exit this guide...
pause >nul
