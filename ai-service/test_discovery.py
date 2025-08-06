#!/usr/bin/env python3
"""
Simple test script to verify Discovery Engine connection
"""

import os
import asyncio
from dotenv import load_dotenv
from services.gemini_service import GeminiService

# Load environment variables
load_dotenv()

async def test_discovery_engine():
    """Test Discovery Engine with a sample query"""
    print("🧪 Testing Discovery Engine Connection")
    print("=" * 50)
    
    try:
        # Initialize the service
        service = GeminiService()
        print(f"✅ Service initialized")
        print(f"📋 Project ID: {service.project_id}")
        print(f"🔍 Engine ID: {service.engine_id}")
        print(f"🌍 Location: {service.location}")
        
        # Test authentication
        print("\n🔐 Testing Google Cloud Authentication...")
        token = await service.get_google_access_token()
        if token:
            print("✅ Authentication successful")
        else:
            print("❌ Authentication failed")
            return
        
        # Test Discovery Engine search
        print("\n🔍 Testing Discovery Engine Search...")
        test_queries = [
            "What is the premium payment grace period?",
            "What are the coverage limits?",
            "Tell me about policy benefits"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            result = await service.search_discovery_engine(query)
            print(f"📄 Result: {result[:200]}...")
        
        # Test complete Q&A
        print("\n🎯 Testing Complete Q&A Process...")
        questions = ["What is the grace period for premium payment?"]
        answers = await service.answer_questions("", questions)
        
        print(f"❓ Question: {questions[0]}")
        print(f"💬 Answer: {answers[0][:300]}...")
        
        print("\n" + "=" * 50)
        print("🎉 Test Complete!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_discovery_engine())
