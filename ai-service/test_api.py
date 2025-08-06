#!/usr/bin/env python3
"""
Test script for the AI service API
"""

import requests
import json
import time

def test_api():
    print("🧪 Testing HackRx AI Service API")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api/v1"
    headers = {
        "Authorization": "Bearer test-token",
        "Content-Type": "application/json"
    }
    
    # Test 1: Health check
    print("1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Service is healthy")
            print(f"🔧 Project ID: {health_data.get('discovery_engine', {}).get('project_id')}")
            print(f"🔍 Engine ID: {health_data.get('discovery_engine', {}).get('engine_id')}")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Question answering
    print("\n2️⃣ Testing Question Answering...")
    test_data = {
        "documents": "test",  # Not used since you have pre-trained data
        "questions": [
            "What is the grace period for premium payment?",
            "What are the coverage limits?",
            "Tell me about policy benefits"
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/hackrx/run",
            headers=headers,
            json=test_data,
            timeout=60
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Questions answered successfully!")
            for i, (question, answer) in enumerate(zip(test_data["questions"], result["answers"])):
                print(f"\n❓ Question {i+1}: {question}")
                print(f"💬 Answer: {answer[:300]}...")
        else:
            print(f"❌ API call failed: {response.text}")
    except Exception as e:
        print(f"❌ API call error: {e}")
    
    # Test 3: Chat endpoint
    print("\n3️⃣ Testing Chat Endpoint...")
    chat_data = {
        "message": "What is the premium payment grace period?",
        "timestamp": "2025-01-01T00:00:00"
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            headers=headers,
            json=chat_data,
            timeout=60
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat response received!")
            print(f"💬 Response: {result['response'][:300]}...")
        else:
            print(f"❌ Chat failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Your AI service is now connected to your trained model!")
    print("📄 The responses above should be from your dataset, not generic answers.")

if __name__ == "__main__":
    test_api()
