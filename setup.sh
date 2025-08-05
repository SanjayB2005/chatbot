#!/bin/bash

echo "🚀 Starting HackRx ChatBot Application..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Setup AI Service
echo "🐍 Setting up AI Service..."
cd ai-service

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file for AI service..."
    cp .env.example .env
    echo "⚠️  Please edit ai-service/.env and add your GEMINI_API_KEY"
fi

echo "✅ AI Service setup complete!"
cd ..

# Setup Server
echo "🖥️  Setting up Server..."
cd server

if [ ! -d "node_modules" ]; then
    echo "Installing server dependencies..."
    npm install
fi

if [ ! -f ".env" ]; then
    echo "Creating .env file for server..."
    cp .env.example .env
    echo "⚠️  Please edit server/.env with your MongoDB URI if needed"
fi

echo "✅ Server setup complete!"
cd ..

# Setup Client
echo "⚛️  Setting up Client..."
cd client

if [ ! -d "node_modules" ]; then
    echo "Installing client dependencies..."
    npm install
fi

if [ ! -f ".env" ]; then
    echo "Creating .env file for client..."
    cp .env.example .env
fi

echo "✅ Client setup complete!"
cd ..

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit ai-service/.env and add your GEMINI_API_KEY"
echo "2. Make sure MongoDB is running (or update server/.env with your MongoDB URI)"
echo "3. Run the application using the start script:"
echo ""
echo "   ./start.sh"
echo ""
echo "Or start each service manually:"
echo "   Terminal 1: cd ai-service && source venv/bin/activate && uvicorn main:app --reload"
echo "   Terminal 2: cd server && npm run dev"
echo "   Terminal 3: cd client && npm run dev"
echo ""
echo "🌐 Access the application at: http://localhost:5173"
