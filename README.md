# HackRx ChatBot

A comprehensive AI-powered chatbot application built with React.js frontend, Node.js/Express backend, and Python/FastAPI AI service using Google's Gemini 2.0 Flash model.

## 🏗️ Architecture

```
HackRx ChatBot/
├── client/          # React.js Frontend
├── server/          # Node.js/Express Backend  
├── ai-service/      # Python/FastAPI AI Service
└── README.md
```

## 🚀 Features

- **Interactive Chat Interface**: Real-time conversations with AI
- **Document Processing**: Upload documents and ask questions (HackRx API format)
- **Session Management**: Persistent chat sessions with history
- **Modern UI**: Clean, responsive interface with Tailwind CSS
- **RESTful APIs**: Well-structured API endpoints
- **MongoDB Integration**: Chat history and session storage
- **Gemini 2.0 Flash**: Latest Google AI model integration

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (local or cloud instance)
- **Google Gemini API Key**

## 🛠️ Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd "HackRx ChatBot"
```

### 2. AI Service Setup (Python/FastAPI)
```bash
cd ai-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Server Setup (Node.js/Express)
```bash
cd ../server

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env with your configurations:
# PORT=3001
# MONGODB_URI=mongodb://localhost:27017/hackrx-chatbot
# AI_SERVICE_URL=http://localhost:8000
# CORS_ORIGIN=http://localhost:5173
```

### 4. Client Setup (React.js)
```bash
cd ../client

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env:
# VITE_API_URL=http://localhost:3001
```

## 🏃‍♂️ Running the Application

### Start AI Service (Terminal 1)
```bash
cd ai-service
# Activate virtual environment first
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Server (Terminal 2)
```bash
cd server
npm run dev
```

### Start Client (Terminal 3)
```bash
cd client
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:3001
- **AI Service**: http://localhost:8000

## 📡 API Endpoints

### HackRx Document Processing
```
POST /api/v1/hackrx/run
Content-Type: application/json
Authorization: Bearer <api_key>

{
    "documents": "https://example.com/document.pdf",
    "questions": ["Question 1?", "Question 2?"]
}

Response: {
    "answers": ["Answer 1", "Answer 2"]
}
```

### Chat Endpoints
- `POST /api/v1/chat/session` - Create new session
- `POST /api/v1/chat/message` - Send message
- `GET /api/v1/chat/history/:sessionId` - Get chat history
- `GET /api/v1/chat/sessions` - Get all sessions

### Health Check
- `GET /api/v1/health` - Service health status

## 🔧 Configuration

### Environment Variables

**AI Service (.env)**
```
GEMINI_API_KEY=your_gemini_api_key
PORT=8000
HOST=0.0.0.0
DEBUG=True
```

**Server (.env)**
```
PORT=3001
MONGODB_URI=mongodb://localhost:27017/hackrx-chatbot
AI_SERVICE_URL=http://localhost:8000
CORS_ORIGIN=http://localhost:5173
NODE_ENV=development
```

**Client (.env)**
```
VITE_API_URL=http://localhost:3001
VITE_APP_TITLE=HackRx ChatBot
VITE_APP_VERSION=1.0.0
```

## 🏗️ Project Structure

### AI Service (Python)
```
ai-service/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── models/
│   └── schemas.py         # Pydantic models
├── services/
│   └── gemini_service.py  # Gemini AI integration
└── routes/
    └── api_routes.py      # API route handlers
```

### Server (Node.js)
```
server/
├── index.js               # Express app entry point
├── package.json           # Node dependencies
├── models/
│   ├── ChatMessage.js     # Chat message schema
│   └── ChatSession.js     # Chat session schema
├── routes/
│   ├── chatRoutes.js      # Chat API routes
│   └── healthRoutes.js    # Health check routes
└── services/
    └── aiService.js       # AI service client
```

### Client (React)
```
client/
├── src/
│   ├── App.jsx            # Main app component
│   ├── services/
│   │   └── api.js         # API client
│   └── components/
│       ├── ChatInterface.jsx      # Chat UI
│       ├── Sidebar.jsx           # Session sidebar
│       └── DocumentProcessor.jsx # Document Q&A
├── public/
└── package.json
```

## 🔒 Security Features

- API key authentication for AI service
- CORS configuration
- Request validation with Pydantic/Express
- Error handling and logging
- Rate limiting ready

## 🚀 Deployment

### AI Service
```bash
# Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Using Docker (create Dockerfile)
docker build -t hackrx-ai-service .
docker run -p 8000:8000 hackrx-ai-service
```

### Server
```bash
npm start

# Using PM2
pm2 start index.js --name hackrx-server
```

### Client
```bash
npm run build
# Deploy dist/ folder to your hosting service
```

## 🧪 Testing

### Test HackRx API Format
```bash
curl -X POST http://localhost:8000/api/v1/hackrx/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": ["What is the grace period for premium payment?"]
  }'
```

## 🐛 Troubleshooting

### Common Issues

1. **Gemini API Key**: Ensure your API key is correctly set in ai-service/.env
2. **MongoDB Connection**: Check if MongoDB is running and connection string is correct
3. **Port Conflicts**: Make sure ports 3001, 5173, and 8000 are available
4. **CORS Issues**: Verify CORS_ORIGIN in server environment matches client URL

### Logs
- AI Service: Check uvicorn console output
- Server: Check node.js console output  
- Client: Check browser developer console

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

For support and questions, please open an issue in the repository.

---

**Built with ❤️ using React, Node.js, Python, and Google Gemini 2.0 Flash**
