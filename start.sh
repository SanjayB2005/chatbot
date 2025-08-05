#!/bin/bash

echo "🚀 Starting HackRx ChatBot Services..."

# Function to start service in background
start_service() {
    echo "Starting $1..."
    case $1 in
        "ai-service")
            cd ai-service
            source venv/bin/activate
            uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
            AI_PID=$!
            echo "AI Service started with PID: $AI_PID"
            cd ..
            ;;
        "server")
            cd server
            npm run dev &
            SERVER_PID=$!
            echo "Server started with PID: $SERVER_PID"
            cd ..
            ;;
        "client")
            cd client
            npm run dev &
            CLIENT_PID=$!
            echo "Client started with PID: $CLIENT_PID"
            cd ..
            ;;
    esac
}

# Create PID file to track processes
PID_FILE="hackrx_pids.txt"
echo "" > $PID_FILE

# Start services
start_service "ai-service"
echo $AI_PID >> $PID_FILE

sleep 3
start_service "server"
echo $SERVER_PID >> $PID_FILE

sleep 3
start_service "client"
echo $CLIENT_PID >> $PID_FILE

echo ""
echo "🎉 All services started successfully!"
echo ""
echo "🌐 Application URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:3001"
echo "   AI Service: http://localhost:8000"
echo ""
echo "📋 Service PIDs:"
echo "   AI Service: $AI_PID"
echo "   Server: $SERVER_PID"
echo "   Client: $CLIENT_PID"
echo ""
echo "🛑 To stop all services, run: ./stop.sh"
echo ""

# Keep script running
echo "Press Ctrl+C to stop all services..."
wait
