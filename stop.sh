#!/bin/bash

echo "🛑 Stopping HackRx ChatBot Services..."

PID_FILE="hackrx_pids.txt"

if [ -f "$PID_FILE" ]; then
    echo "Found PID file, stopping services..."
    
    while IFS= read -r pid; do
        if [ ! -z "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo "Stopping process $pid..."
            kill "$pid"
        fi
    done < "$PID_FILE"
    
    rm "$PID_FILE"
    echo "✅ All services stopped!"
else
    echo "No PID file found. Attempting to stop services by name..."
    
    # Stop uvicorn processes
    pkill -f "uvicorn main:app"
    
    # Stop node processes (be careful with this in production)
    pkill -f "npm run dev"
    pkill -f "vite"
    
    echo "✅ Attempted to stop all services!"
fi

echo "🎉 HackRx ChatBot services have been stopped."
