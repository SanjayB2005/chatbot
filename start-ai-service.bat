@echo off
echo ========================================
echo  🤖 Starting HackRx ChatBot AI Service
echo ========================================
echo.
cd /d "c:\Users\ADMIN\Desktop\HackRx ChatBot\ai-service"
echo Current directory: %CD%
echo.
echo Starting AI Service on http://localhost:8000
echo API Endpoint: http://localhost:8000/api/v1/hackrx/run
echo.
C:\Python312\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
