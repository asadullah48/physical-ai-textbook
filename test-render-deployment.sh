#!/bin/bash
# Test Render deployment

# Replace with YOUR Render URL
BACKEND_URL="https://physical-ai-backend.onrender.com"

echo "🧪 Testing Render Deployment..."
echo "================================"
echo ""

echo "Test 1: Health Check"
curl -s $BACKEND_URL/api/health | python -m json.tool
echo ""
echo ""

echo "Test 2: List Modules"
curl -s $BACKEND_URL/api/v1/modules | python -m json.tool | head -30
echo ""
echo ""

echo "Test 3: Chat - Helpful Mode"
curl -s -X POST $BACKEND_URL/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?", "mode": "helpful"}' | python -m json.tool | head -40
echo ""
echo ""

echo "Test 4: Chat - Socratic Mode"
curl -s -X POST $BACKEND_URL/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is inverse kinematics?", "mode": "socratic"}' | python -m json.tool | head -40
echo ""
echo ""

echo "Test 5: Chat - Embodiment Mode"
curl -s -X POST $BACKEND_URL/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about sensors", "mode": "embodiment"}' | python -m json.tool | head -40
echo ""
echo ""

echo "✅ All tests complete!"
echo ""
echo "If you see JSON responses above, your deployment is working!"
