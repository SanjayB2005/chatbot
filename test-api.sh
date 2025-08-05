#!/bin/bash

echo "🧪 Testing HackRx ChatBot API Endpoints..."
echo "========================================"

# Configuration
AI_SERVICE_URL="http://localhost:8000"
SERVER_URL="http://localhost:3001"
API_KEY="test-api-key"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local url=$1
    local method=$2
    local data=$3
    local description=$4
    
    echo -e "\n${YELLOW}Testing: $description${NC}"
    echo "URL: $url"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$url")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $API_KEY" \
            -d "$data" \
            "$url")
    fi
    
    # Extract HTTP code from response
    http_code=$(echo "$response" | tail -n1)
    response_body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✅ SUCCESS (HTTP $http_code)${NC}"
        echo "Response: $response_body" | head -c 200
        echo "..."
    else
        echo -e "${RED}❌ FAILED (HTTP $http_code)${NC}"
        echo "Response: $response_body"
    fi
}

# Test AI Service Health
test_endpoint "$AI_SERVICE_URL/api/v1/health" "GET" "" "AI Service Health Check"

# Test Server Health  
test_endpoint "$SERVER_URL/api/v1/health" "GET" "" "Server Health Check"

# Test Document Processing (HackRx format)
echo -e "\n${YELLOW}Testing HackRx Document Processing...${NC}"
hackrx_data='{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?"
    ]
}'

test_endpoint "$AI_SERVICE_URL/api/v1/hackrx/run" "POST" "$hackrx_data" "AI Service - HackRx Document Processing"

# Test via Server (proxy)
test_endpoint "$SERVER_URL/api/v1/chat/hackrx/run" "POST" "$hackrx_data" "Server - HackRx Document Processing"

# Test Chat Session Creation
session_data='{"title": "Test Chat Session"}'
test_endpoint "$SERVER_URL/api/v1/chat/session" "POST" "$session_data" "Create Chat Session"

# Test Chat Message (you'd need to use actual session ID from above)
chat_data='{"sessionId": "test-session-id", "message": "Hello, can you help me?"}'
test_endpoint "$SERVER_URL/api/v1/chat/message" "POST" "$chat_data" "Send Chat Message"

# Test Get Sessions
test_endpoint "$SERVER_URL/api/v1/chat/sessions" "GET" "" "Get Chat Sessions"

echo -e "\n${GREEN}🎉 API Testing Complete!${NC}"
echo "========================================"
echo ""
echo "📝 Notes:"
echo "- Some tests may fail if services aren't running"
echo "- Chat message test needs a valid session ID"
echo "- HackRx document processing requires internet access"
echo "- Make sure all services are running before testing"
