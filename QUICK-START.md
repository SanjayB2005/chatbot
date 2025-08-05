# 🚀 Quick Start Guide - Discovery Engine Edition

## Ready to Run Your HackRx ChatBot with Google Discovery Engine!

### 🔐 First Time Setup (Required)

**Setup Google Cloud Authentication:**
1. Install Google Cloud CLI: https://cloud.google.com/sdk/docs/install
2. Run: `gcloud auth login`
3. Run: `gcloud config set project 953445234871`  
4. Run: `gcloud auth application-default login`

*See GOOGLE-AUTH-SETUP.md for detailed instructions*

### 🚀 Start Your ChatBot

**Option 1: Auto Start (Recommended)**
1. Double-click: `START-ALL.bat`
2. Wait 30 seconds for all services to start
3. Open: http://localhost:5173

**Option 2: Manual Start (3 separate terminals)**
1. Run: `start-ai-service.bat`
2. Run: `start-server.bat`  
3. Run: `start-client.bat`

### 🌐 Access Points
- **Main App**: http://localhost:5173
- **API Server**: http://localhost:3001
- **AI Service**: http://localhost:8000

### 🧪 Test Your Discovery Engine API
```bash
curl -X POST http://localhost:8000/api/v1/hackrx/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-key" \
  -d '{"documents":"knowledge_base","questions":["What is the grace period for premium payment?"]}'
```

### 🎯 What's Different Now
- ✅ **No document uploads needed** - Your data is in Google Discovery Engine
- ✅ **Smart search** - Uses your trained dataset from Google Cloud
- ✅ **Gemini + Discovery Engine** - Best of both worlds
- ✅ **Same HackRx API format** - `/api/v1/hackrx/run` endpoint unchanged

### 🔧 Your Configuration
- ✅ Gemini API Key: Configured
- ✅ Discovery Engine: bajajai_1753609382263
- ✅ Project ID: 953445234871  
- ✅ All dependencies: Installed

**Your trained dataset is ready! Just authenticate with Google Cloud and start the services!** 🎉
