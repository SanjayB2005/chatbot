# 🔐 Simple Google Cloud Authentication

## Quick Setup (No CLI needed)

### Step 1: Create Service Account Key
1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=953445234871
2. Click "Create Service Account"
3. Name: `hackrx-chatbot-service`
4. Grant role: "Discovery Engine Admin" and "Cloud Platform"
5. Click "Create Key" → Choose JSON
6. Download the JSON file

### Step 2: Save the Key File
1. Save the downloaded JSON file as: 
   `c:\Users\ADMIN\Desktop\HackRx ChatBot\ai-service\service-account-key.json`

### Step 3: Update Environment
Add this line to your `ai-service\.env` file:
```
GOOGLE_APPLICATION_CREDENTIALS=c:\Users\ADMIN\Desktop\HackRx ChatBot\ai-service\service-account-key.json
```

### Step 4: Test & Run
Then run `START-ALL.bat` to start your chatbot!

## Alternative: Use gcloud CLI
If you have gcloud CLI installed:
```bash
gcloud auth login
gcloud config set project 953445234871
gcloud auth application-default login
```

That's it! Your chatbot will now use your trained Discovery Engine data.
