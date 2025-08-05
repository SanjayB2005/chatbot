@echo off
echo ========================================
echo     🚀 HackRx ChatBot - Auto Start
echo ========================================
echo.
echo Starting all services automatically...
echo This will open 3 separate windows for each service.
echo.

REM Start AI Service
echo Starting AI Service...
start "HackRx AI Service" cmd /k "cd /d "c:\Users\ADMIN\Desktop\HackRx ChatBot\ai-service" && C:\Python312\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a bit
timeout /t 3 /nobreak >nul

REM Start Server
echo Starting Server...
start "HackRx Server" cmd /k "cd /d "c:\Users\ADMIN\Desktop\HackRx ChatBot\server" && npm run dev"

REM Wait a bit
timeout /t 3 /nobreak >nul

REM Start Client
echo Starting Client...
start "HackRx Client" cmd /k "cd /d "c:\Users\ADMIN\Desktop\HackRx ChatBot\client" && npm run dev"

echo.
echo ========================================
echo 🎉 All services are starting!
echo ========================================
echo.
echo Three windows should have opened:
echo 1. AI Service   - http://localhost:8000
echo 2. Server       - http://localhost:3003
echo 3. Client       - http://localhost:5173
echo.
echo ⏰ Wait about 30 seconds for all services to start
echo 🌐 Then open: http://localhost:5173
echo.
echo To stop all services, close the 3 command windows.
echo.
pause
