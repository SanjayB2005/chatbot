@echo off
echo 🧪 Testing HackRx ChatBot APIs...
echo.

REM Wait a bit for services to start
echo Waiting for services to initialize...
timeout /t 10 /nobreak >nul

echo Testing AI Service Health...
curl -X GET "http://localhost:8000/api/v1/health" -H "Accept: application/json"
echo.
echo.

echo Testing Server Health...
curl -X GET "http://localhost:3001/api/v1/health" -H "Accept: application/json"
echo.
echo.

echo Testing HackRx API with sample question...
curl -X POST "http://localhost:8000/api/v1/hackrx/run" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer test-key" ^
  -d "{\"documents\":\"knowledge_base\",\"questions\":[\"What is the grace period for premium payment?\"]}"
echo.
echo.

echo 🎉 Testing complete!
echo If you see JSON responses above, your APIs are working!
echo.
echo 🌐 Access your chatbot at: http://localhost:5173
pause
