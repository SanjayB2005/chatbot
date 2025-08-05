# 🔐 Security Setup Instructions

## ⚠️ Important: GitHub Push Protection

Your push was blocked because the `service-account-key.json` file contains sensitive Google Cloud credentials. This is a security feature to protect your secrets.

## 🛠️ How to Fix This

### Step 1: Set Up Environment Variables

1. **Copy the example environment file:**
   ```bash
   cp ai-service/.env.example ai-service/.env
   ```

2. **Add your actual credentials to `ai-service/.env`:**
   ```bash
   # Required: Your Gemini API Key
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   
   # Required: Google Cloud Authentication
   GOOGLE_APPLICATION_CREDENTIALS=ai-service/service-account-key.json
   ```

### Step 2: Keep Your Service Account Key Secure

The `service-account-key.json` file is now in `.gitignore` and will not be committed to GitHub. You have two options:

#### Option A: Keep the Local File (Recommended for Development)
- Keep your `service-account-key.json` file locally
- Set `GOOGLE_APPLICATION_CREDENTIALS=ai-service/service-account-key.json` in your `.env` file
- The file will be ignored by git and not pushed to GitHub

#### Option B: Use Environment Variables (Recommended for Production)
- Extract the contents of your service account key and set them as environment variables
- This is more secure for production deployments

### Step 3: Configure Your Environment

1. **Make sure you have your actual Gemini API key**
2. **Update the `.env` file with your real credentials**
3. **Test the connection:**
   ```bash
   cd ai-service
   python -c "from services.gemini_service import GeminiService; print('✅ Service configured successfully')"
   ```

## 🚀 Resume Development

After setting up your environment variables:

1. **Commit the security fixes:**
   ```bash
   git add .
   git commit -m "chore: remove service account key from git and add security setup"
   ```

2. **Push to GitHub:**
   ```bash
   git push origin main
   ```

3. **Start your services:**
   ```bash
   # Terminal 1: AI Service
   cd ai-service
   python main.py

   # Terminal 2: Backend
   cd server
   npm run dev

   # Terminal 3: Frontend  
   cd client
   npm run dev
   ```

## 📋 Project Configuration

Your Discovery Engine is already configured:
- **Project ID:** 953445234871
- **Engine ID:** bajajai_1753609382263
- **Location:** global

The chatbot will work with your pre-trained dataset once the authentication is properly set up!
