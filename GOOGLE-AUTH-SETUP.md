# Google Cloud Authentication Setup

## Method 1: Using Google Cloud CLI (Recommended)

1. **Install Google Cloud CLI** (if not already installed):
   - Download from: https://cloud.google.com/sdk/docs/install

2. **Authenticate with your Google account**:
   ```bash
   gcloud auth login
   ```

3. **Set your project**:
   ```bash
   gcloud config set project 953445234871
   ```

4. **Enable Application Default Credentials**:
   ```bash
   gcloud auth application-default login
   ```

## Method 2: Using Service Account Key (Alternative)

1. **Create a service account**:
   - Go to Google Cloud Console → IAM & Admin → Service Accounts
   - Create a new service account
   - Grant "Discovery Engine Admin" role

2. **Download the key file**:
   - Create and download a JSON key file
   - Save it as `service-account-key.json` in the ai-service folder

3. **Set environment variable**:
   ```bash
   set GOOGLE_APPLICATION_CREDENTIALS=c:\Users\ADMIN\Desktop\HackRx ChatBot\ai-service\service-account-key.json
   ```

## Test Authentication

Run this to test if authentication works:
```bash
gcloud auth print-access-token
```

If you see a token, authentication is working!

## Your Discovery Engine Details
- Project ID: 953445234871
- Engine ID: bajajai_1753609382263
- Location: global
- Collection: default_collection

These are already configured in your .env file.
