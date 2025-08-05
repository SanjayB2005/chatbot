@echo off
echo ========================================
echo  🖥️  Starting HackRx ChatBot Server
echo ========================================
echo.
cd /d "c:\Users\ADMIN\Desktop\HackRx ChatBot\server"
echo Current directory: %CD%
echo.
echo Starting Server on http://localhost:3003
echo API Base: http://localhost:3003/api/v1
echo.
npm run dev
