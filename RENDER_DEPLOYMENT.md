# 🚀 Render Deployment Guide - AI Service

## Quick Deploy Configuration

### **Build Command:**
```bash
pip install -r requirements.txt
```

### **Start Command:**
```bash
python main.py
```

### **Python Version:**
```
3.11
```

## Environment Variables for Render

### **Required Variables:**
```bash
# Gemini AI API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Server Configuration
PORT=8000
HOST=0.0.0.0
DEBUG=False

# Google Discovery Engine
GOOGLE_PROJECT_ID=953445234871
DISCOVERY_ENGINE_ID=bajajai_1753609382263
DISCOVERY_LOCATION=global
DISCOVERY_COLLECTION=default_collection
```

### **Google Cloud Authentication - Choose One Method:**

#### **Method 1: Environment Variables (Recommended for Render)**
```bash
# Service Account Credentials
GOOGLE_SERVICE_ACCOUNT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----
GOOGLE_SERVICE_ACCOUNT_PROJECT_ID=953445234871
```

#### **Method 2: Service Account File**
```bash
# Upload service-account-key.json to Render and set:
GOOGLE_APPLICATION_CREDENTIALS=/opt/render/project/src/service-account-key.json
```

### **CORS Configuration:**
```bash
# Update with your actual frontend domain
CORS_ORIGINS=["https://your-frontend.onrender.com", "https://your-custom-domain.com"]
```

## 📋 Step-by-Step Render Deployment

### 1. **Prepare Your Repository**
- Make sure your code is pushed to GitHub
- Verify `requirements.txt` includes all dependencies
- Ensure no secrets are in the repository

### 2. **Create Render Web Service**
- Go to [Render Dashboard](https://dashboard.render.com)
- Click "New" → "Web Service"
- Connect your GitHub repository
- Select the `ai-service` directory as root directory

### 3. **Configure Build Settings**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python main.py`
- **Environment:** `Python 3.11`

### 4. **Set Environment Variables**
- Add all the environment variables listed above
- For service account key: Copy the content from your local `service-account-key.json`

### 5. **Deploy**
- Click "Create Web Service"
- Wait for deployment to complete
- Your API will be available at: `https://your-service-name.onrender.com`

## 🔗 API Endpoints

After deployment, your API will be available at:
- **Health Check:** `GET /api/v1/health`
- **Chat:** `POST /api/v1/chat`
- **Questions:** `POST /api/v1/hackrx/run`

## 🔧 Testing Your Deployment

Test your deployed service:
```bash
curl https://your-service-name.onrender.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ai-service",
  "timestamp": "2025-08-05T...",
  "discovery_engine": {
    "project_id": "953445234871",
    "engine_id": "bajajai_1753609382263",
    "location": "global"
  }
}
```

## 🎯 Next Steps

1. **Deploy AI Service** to Render
2. **Update Frontend** to use the Render API URL
3. **Deploy Backend** (Node.js) to Render 
4. **Deploy Frontend** to Render or Vercel
5. **Update CORS origins** with production URLs

Your HackRx ChatBot will be live! 🚀
