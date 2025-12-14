@echo off
REM Test Render deployment (Windows)

REM Replace with YOUR Render URL
set BACKEND_URL=https://physical-ai-backend.onrender.com

echo.
echo ========================================
echo 🧪 Testing Render Deployment
echo ========================================
echo.

echo Test 1: Health Check
curl -s %BACKEND_URL%/api/health
echo.
echo.

echo Test 2: List Modules
curl -s %BACKEND_URL%/api/v1/modules
echo.
echo.

echo Test 3: Chat - Helpful Mode
curl -s -X POST %BACKEND_URL%/api/v1/chat -H "Content-Type: application/json" -d "{\"message\": \"What is Physical AI?\", \"mode\": \"helpful\"}"
echo.
echo.

echo Test 4: Chat - Socratic Mode
curl -s -X POST %BACKEND_URL%/api/v1/chat -H "Content-Type: application/json" -d "{\"message\": \"What is inverse kinematics?\", \"mode\": \"socratic\"}"
echo.
echo.

echo Test 5: Chat - Embodiment Mode
curl -s -X POST %BACKEND_URL%/api/v1/chat -H "Content-Type: application/json" -d "{\"message\": \"Tell me about sensors\", \"mode\": \"embodiment\"}"
echo.
echo.

echo ========================================
echo ✅ All tests complete!
echo ========================================
echo.
pause
