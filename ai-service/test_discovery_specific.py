"""
Test script to verify Discovery Engine configuration and responses
Run this to test if your Discovery Engine is returning specific answers from your trained data
"""

import asyncio
import os
from services.gemini_service import GeminiService
from dotenv import load_dotenv

async def test_discovery_engine():
    # Load environment variables
    load_dotenv('.env.local')
    load_dotenv()
    
    print("🧪 Testing Discovery Engine Configuration")
    print("=" * 50)
    
    try:
        # Initialize service
        service = GeminiService()
        
        print(f"✅ Service initialized successfully")
        print(f"📋 Project ID: {service.project_id}")
        print(f"📋 Engine ID: {service.engine_id}")
        print(f"📋 Location: {service.location}")
        print(f"📋 Discovery Endpoint: {service.discovery_endpoint}")
        print()
        
        # Test queries - replace these with questions that should be answered by your trained data
        test_queries = [
            "What is Bajaj Auto?",  # Replace with a question from your documents
            "Tell me about the company",  # Replace with another question from your documents
            "What are the main products?",  # Replace with relevant questions
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"🔍 Test {i}: {query}")
            print("-" * 30)
            
            # Test direct Discovery Engine search
            search_result = await service.search_discovery_engine(query)
            print(f"📄 Raw Discovery Result:")
            print(f"   {search_result[:200]}...")
            print()
            
            # Test processed answer
            answers = await service.answer_questions("", [query])
            print(f"🤖 Processed Answer:")
            print(f"   {answers[0][:200]}...")
            print()
            
            # Test chat response
            chat_response = await service.chat_response(query)
            print(f"💬 Chat Response:")
            print(f"   {chat_response[:200]}...")
            print()
            print("=" * 50)
            
        print("✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_discovery_engine())
