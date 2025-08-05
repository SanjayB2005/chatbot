@echo off
echo 🚀 Starting HackRx ChatBot Services...

echo Starting AI Service...
start "AI Service" cmd /k "cd ai-service && venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 5 /nobreak >nul

echo Starting Server...
start "Server" cmd /k "cd server && npm run dev"

timeout /t 3 /nobreak >nul

echo Starting Client...
start "Client" cmd /k "cd client && npm run dev"

echo.
echo 🎉 All services are starting in separate windows!
echo.
echo 🌐 Application URLs:
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:3001
echo    AI Service: http://localhost:8000
echo.
echo 📋 Three command windows should have opened for each service.
echo 🛑 Close the command windows to stop the services.
echo.
pause
