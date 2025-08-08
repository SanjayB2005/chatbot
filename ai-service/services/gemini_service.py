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
        # Reload environment variables
        load_dotenv()
        load_dotenv('.env.local')  # Load local secrets as override
        
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Google Discovery Engine configuration - MUST match your actual setup
        self.project_id = os.getenv("GOOGLE_PROJECT_ID")
        self.engine_id = os.getenv("DISCOVERY_ENGINE_ID")
        self.location = os.getenv("DISCOVERY_LOCATION", "global")
        self.collection = os.getenv("DISCOVERY_COLLECTION", "default_collection")
        
        # Validate required environment variables
        if not self.project_id:
            raise ValueError("GOOGLE_PROJECT_ID environment variable is required")
        if not self.engine_id:
            raise ValueError("DISCOVERY_ENGINE_ID environment variable is required")
        
        print(f"🔧 Initialized with Project ID: {self.project_id}")
        print(f"🔧 Engine ID: {self.engine_id}")
        print(f"🔧 Location: {self.location}")
        print(f"🔧 Collection: {self.collection}")
        
        # Discovery Engine endpoint
        self.discovery_endpoint = f"https://discoveryengine.googleapis.com/v1alpha/projects/{self.project_id}/locations/{self.location}/collections/{self.collection}/engines/{self.engine_id}/servingConfigs/default_search:search"
        print(f"🔗 Discovery Endpoint: {self.discovery_endpoint}")
    
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
                print(f"🔧 Service account project: {service_account_info['project_id']}")
                
                # Use the service account's project ID for Discovery Engine
                self.project_id = service_account_info['project_id']
                print(f"🔄 Updated project ID to: {self.project_id}")
                
                # Update the discovery endpoint with correct project ID
                self.discovery_endpoint = f"https://discoveryengine.googleapis.com/v1alpha/projects/{self.project_id}/locations/{self.location}/collections/{self.collection}/engines/{self.engine_id}/servingConfigs/default_search:search"
            
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
                "pageSize": 5,  # Reduced to get more focused results
                "queryExpansionSpec": {"condition": "AUTO"},
                "spellCorrectionSpec": {"mode": "AUTO"},
                "languageCode": "en-US",
                "contentSearchSpec": {
                    "extractiveContentSpec": {
                        "maxExtractiveAnswerCount": 3,
                        "maxExtractiveSegmentCount": 1,
                        "returnExtractiveSegmentScore": True
                    },
                    "summarySpec": {
                        "summaryResultCount": 3,
                        "includeCitations": True
                    }
                },
                "userInfo": {"timeZone": "Asia/Calcutta"}
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
                
                # Extract the most relevant content from your trained data
                if 'results' in result and result['results']:
                    print(f"📊 Found {len(result['results'])} results")
                    
                    # Try to get summary first (most relevant)
                    if 'summary' in result and result['summary'].get('summaryText'):
                        summary_text = result['summary']['summaryText']
                        print(f"🎯 Using summary: {summary_text[:100]}...")
                        return summary_text
                    
                    # Get extractive answers from your documents
                    for result_item in result['results']:
                        document = result_item.get('document', {})
                        
                        # Check for extractive answers
                        if 'extractiveAnswers' in document and document['extractiveAnswers']:
                            extractive_answer = document['extractiveAnswers'][0].get('content', '')
                            if extractive_answer.strip():
                                print(f"🎯 Using extractive answer: {extractive_answer[:100]}...")
                                return extractive_answer
                        
                        # Check derived structure data
                        if 'derivedStructData' in document:
                            derived_data = document['derivedStructData']
                            
                            # Try extractive answers from derived data
                            if 'extractive_answers' in derived_data and derived_data['extractive_answers']:
                                answer = derived_data['extractive_answers'][0].get('content', '')
                                if answer.strip():
                                    print(f"🎯 Using derived extractive answer: {answer[:100]}...")
                                    return answer
                            
                            # Try snippets as fallback
                            if 'snippets' in derived_data and derived_data['snippets']:
                                snippet = derived_data['snippets'][0].get('snippet', '')
                                if snippet.strip():
                                    print(f"🎯 Using snippet: {snippet[:100]}...")
                                    return snippet
                        
                        # Try struct data as last resort
                        if 'structData' in document and document['structData']:
                            struct_data = document['structData']
                            if isinstance(struct_data, dict):
                                # Look for common content fields
                                for field in ['content', 'text', 'description', 'body']:
                                    if field in struct_data and struct_data[field]:
                                        content = str(struct_data[field])
                                        if content.strip():
                                            print(f"🎯 Using struct data {field}: {content[:100]}...")
                                            return content
                
                print("⚠️ No relevant information found in your knowledge base.")
                return "I couldn't find specific information about this in the knowledge base. Please ensure your question relates to the uploaded documents."
            else:
                print(f"❌ Discovery Engine API error: {response.status_code} - {response.text}")
                return f"Search service error: {response.status_code}"
                
        except Exception as e:
            print(f"Error searching Discovery Engine: {str(e)}")
            return f"Search error: {str(e)}"
    
    async def answer_questions(self, document_url: str, questions: List[str]) -> List[str]:
        """Process questions using ONLY your trained Discovery Engine data"""
        try:
            answers = []
            
            for question in questions:
                print(f"🔍 Processing question: {question}")
                
                # Search your Discovery Engine for relevant context
                search_context = await self.search_discovery_engine(question)
                
                # Only provide answers if we have relevant content from your knowledge base
                if search_context and search_context.strip() and \
                   not search_context.startswith("I couldn't find specific information"):
                    
                    # Use Gemini to refine the answer but stay strictly within the context
                    prompt = f"""
                    You are an AI assistant that ONLY answers based on the provided context from a specific knowledge base.
                    
                    STRICT INSTRUCTIONS:
                    1. Answer ONLY using information from the context below
                    2. If the context doesn't contain enough information, say "The knowledge base doesn't contain enough information to answer this question"
                    3. Do NOT add general knowledge or assumptions
                    4. Keep answers concise and directly related to the context
                    
                    Context from Knowledge Base:
                    {search_context}
                    
                    Question: {question}
                    
                    Answer based STRICTLY on the context above:
                    """
                    
                    try:
                        response = self.model.generate_content(prompt)
                        answer = response.text.strip()
                        
                        # Validate that the answer seems to be based on the context
                        if "knowledge base doesn't contain" in answer.lower() or \
                           "don't have information" in answer.lower():
                            answers.append("The knowledge base doesn't contain specific information to answer this question.")
                        else:
                            answers.append(answer)
                            
                    except Exception as e:
                        print(f"Error generating answer for question '{question}': {str(e)}")
                        answers.append(search_context)  # Use the raw search result
                else:
                    # No relevant content found in your knowledge base
                    answers.append("The knowledge base doesn't contain specific information to answer this question.")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.1)
            
            return answers
            
        except Exception as e:
            print(f"Error in answer_questions: {str(e)}")
            return [f"Error processing questions: {str(e)}"] * len(questions)
    
    async def chat_response(self, message: str) -> str:
        """Generate a chat response using ONLY your Discovery Engine knowledge base"""
        try:
            print(f"💬 Processing chat message: '{message}'")
            
            # Search your knowledge base for relevant context
            search_context = await self.search_discovery_engine(message)
            print(f"🔍 Knowledge base context: {search_context[:200]}...")
            
            # Only respond if we have relevant content from your knowledge base
            if search_context and search_context.strip() and \
               not search_context.startswith("I couldn't find specific information"):
                
                # Generate response using Gemini but stay within the knowledge base context
                prompt = f"""
                You are a helpful AI assistant that answers ONLY based on a specific knowledge base.
                
                STRICT INSTRUCTIONS:
                1. Answer ONLY using information from the context below
                2. If the context doesn't fully answer the question, say "I can only provide information based on the knowledge base. Here's what I found:" and then provide what's available
                3. Do NOT add general knowledge or make assumptions beyond the context
                4. Be helpful but stay within the boundaries of the provided context
                
                Context from Knowledge Base:
                {search_context}
                
                User Message: {message}
                
                Response based STRICTLY on the context above:
                """
                
                print(f"🧠 Sending prompt to Gemini (length: {len(prompt)} characters)")
                
                response = self.model.generate_content(prompt)
                final_response = response.text.strip()
                
                print(f"✅ Generated final response: {final_response[:200]}...")
                return final_response
            else:
                # No relevant content found in knowledge base
                return "I can only provide information based on the specific knowledge base I have access to. Your question doesn't match any content in the knowledge base. Please ask questions related to the uploaded documents or try rephrasing your question."
            
        except Exception as e:
            print(f"❌ Error generating chat response: {str(e)}")
            return "I'm sorry, I encountered an error while searching the knowledge base. Please try again."
