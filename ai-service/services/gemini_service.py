import os
import google.generativeai as genai
import requests
import asyncio
from typing import List
from dotenv import load_dotenv
import google.auth
from google.auth.transport.requests import Request

load_dotenv('.env.local')  # Load local secrets first
load_dotenv()  # Load .env as fallback

class GeminiService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Google Discovery Engine configuration
        self.project_id = os.getenv("GOOGLE_PROJECT_ID", "953445234871")
        self.engine_id = os.getenv("DISCOVERY_ENGINE_ID", "bajajai_1753609382263")
        self.location = os.getenv("DISCOVERY_LOCATION", "global")
        self.collection = os.getenv("DISCOVERY_COLLECTION", "default_collection")
        
        # Discovery Engine endpoint
        self.discovery_endpoint = f"https://discoveryengine.googleapis.com/v1alpha/projects/{self.project_id}/locations/{self.location}/collections/{self.collection}/engines/{self.engine_id}/servingConfigs/default_search:search"
    
    async def get_google_access_token(self):
        """Get Google Cloud access token"""
        try:
            credentials = None
            
            # Option 1: Try environment variables first (for Render deployment)
            if os.getenv("GOOGLE_SERVICE_ACCOUNT_EMAIL") and os.getenv("GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY"):
                from google.oauth2 import service_account
                import json
                
                service_account_info = {
                    "type": "service_account",
                    "project_id": os.getenv("GOOGLE_SERVICE_ACCOUNT_PROJECT_ID", self.project_id),
                    "private_key_id": os.getenv("GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY_ID", ""),
                    "private_key": os.getenv("GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY").replace('\\n', '\n'),
                    "client_email": os.getenv("GOOGLE_SERVICE_ACCOUNT_EMAIL"),
                    "client_id": os.getenv("GOOGLE_SERVICE_ACCOUNT_CLIENT_ID", ""),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL')}"
                }
                
                credentials = service_account.Credentials.from_service_account_info(
                    service_account_info,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                print("✅ Using service account credentials from environment variables")
            
            # Option 2: Try service account key file
            elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
                if os.path.exists(service_account_path):
                    from google.oauth2 import service_account
                    credentials = service_account.Credentials.from_service_account_file(
                        service_account_path,
                        scopes=['https://www.googleapis.com/auth/cloud-platform']
                    )
                    print("✅ Using service account credentials from file")
            
            # Option 3: Try default credentials (ADC)
            else:
                credentials, project = google.auth.default(
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                print("✅ Using default application credentials")
            
            if credentials:
                credentials.refresh(Request())
                return credentials.token
            else:
                raise Exception("No valid credentials found")
            
        except Exception as e:
            print(f"❌ Error getting Google access token: {str(e)}")
            print("Please set up Google Cloud authentication:")
            print("1. Set environment variables for service account")
            print("2. Or set GOOGLE_APPLICATION_CREDENTIALS to key file path")
            print("3. Or run: gcloud auth application-default login")
            return None
    
    async def search_discovery_engine(self, query: str) -> str:
        """Search your trained Discovery Engine"""
        try:
            access_token = await self.get_google_access_token()
            if not access_token:
                return "Unable to authenticate with Google Cloud"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "query": query,
                "pageSize": 10,
                "queryExpansionSpec": {"condition": "AUTO"},
                "spellCorrectionSpec": {"mode": "AUTO"},
                "languageCode": "en-US",
                "contentSearchSpec": {
                    "extractiveContentSpec": {
                        "maxExtractiveAnswerCount": 1
                    }
                },
                "userInfo": {"timeZone": "Asia/Calcutta"},
                "session": f"projects/{self.project_id}/locations/{self.location}/collections/{self.collection}/engines/{self.engine_id}/sessions/-"
            }
            
            print(f"🔍 Searching Discovery Engine with query: '{query}'")
            print(f"📡 Discovery Engine payload: {payload}")
            
            response = requests.post(
                self.discovery_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"📥 Discovery Engine response status: {response.status_code}")
            print(f"📥 Discovery Engine response: {response.text[:500]}...")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Discovery Engine result structure: {list(result.keys())}")
                
                # Extract the most relevant content
                if 'results' in result and result['results']:
                    print(f"📊 Found {len(result['results'])} results")
                    
                    # Get extractive answers first
                    if 'extractiveAnswers' in result['results'][0].get('document', {}):
                        extractive_answers = result['results'][0]['document']['extractiveAnswers']
                        if extractive_answers:
                            answer = extractive_answers[0].get('content', '')
                            print(f"🎯 Using extractive answer: {answer[:100]}...")
                            return answer
                    
                    # Fallback to document content
                    if 'derivedStructData' in result['results'][0].get('document', {}):
                        derived_data = result['results'][0]['document']['derivedStructData']
                        if 'extractive_answers' in derived_data:
                            answer = derived_data['extractive_answers'][0].get('content', '')
                            print(f"🎯 Using derived extractive answer: {answer[:100]}...")
                            return answer
                        elif 'snippets' in derived_data:
                            answer = derived_data['snippets'][0].get('snippet', '')
                            print(f"🎯 Using snippet: {answer[:100]}...")
                            return answer
                
                print("⚠️ No relevant information found in the knowledge base.")
                return "No relevant information found in the knowledge base."
            else:
                print(f"❌ Discovery Engine API error: {response.status_code} - {response.text}")
                return f"Search service error: {response.status_code}"
                
        except Exception as e:
            print(f"Error searching Discovery Engine: {str(e)}")
            return f"Search error: {str(e)}"
    
    async def answer_questions(self, document_url: str, questions: List[str]) -> List[str]:
        """Process questions using your trained Discovery Engine and Gemini"""
        try:
            answers = []
            
            for question in questions:
                # First, search your Discovery Engine for relevant context
                search_context = await self.search_discovery_engine(question)
                
                # Then use Gemini to generate a comprehensive answer
                prompt = f"""
                Based on the following context from the knowledge base, please provide a clear and accurate answer to the question.
                
                Context from Knowledge Base:
                {search_context}
                
                Question: {question}
                
                Please provide a comprehensive answer based on the context. If the context doesn't contain enough information, please state that clearly.
                """
                
                try:
                    response = self.model.generate_content(prompt)
                    answer = response.text.strip()
                    answers.append(answer)
                except Exception as e:
                    print(f"Error generating answer for question '{question}': {str(e)}")
                    # Fallback to just the search result
                    answers.append(search_context if search_context else "Unable to generate answer for this question.")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.1)
            
            return answers
            
        except Exception as e:
            print(f"Error in answer_questions: {str(e)}")
            return [f"Error processing questions: {str(e)}"] * len(questions)
    
    async def chat_response(self, message: str) -> str:
        """Generate a chat response using Discovery Engine + Gemini"""
        try:
            print(f"💬 Processing chat message: '{message}'")
            
            # Search your knowledge base for relevant context
            search_context = await self.search_discovery_engine(message)
            print(f"🔍 Knowledge base context: {search_context[:200]}...")
            
            # Generate response using Gemini with the context
            prompt = f"""
            You are a helpful AI assistant with access to a specialized knowledge base. 
            
            Context from Knowledge Base:
            {search_context}
            
            User Message: {message}
            
            Please provide a helpful response. If the knowledge base contains relevant information, use it. 
            Otherwise, provide a general helpful response while mentioning that you can search the knowledge base for specific topics.
            """
            
            print(f"🧠 Sending prompt to Gemini (length: {len(prompt)} characters)")
            
            response = self.model.generate_content(prompt)
            final_response = response.text.strip()
            
            print(f"✅ Generated final response: {final_response[:200]}...")
            return final_response
            
        except Exception as e:
            print(f"❌ Error generating chat response: {str(e)}")
            return "I'm sorry, I encountered an error while processing your message. Please try again."
