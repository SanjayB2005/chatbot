#!/usr/bin/env python3
import os
from dotenv import load_dotenv

print("Testing environment loading...")
print(f"Before load_dotenv: GOOGLE_PROJECT_ID = {os.getenv('GOOGLE_PROJECT_ID')}")

load_dotenv()
print(f"After load_dotenv: GOOGLE_PROJECT_ID = {os.getenv('GOOGLE_PROJECT_ID')}")

# Print all environment variables starting with GOOGLE
print("\nAll GOOGLE environment variables:")
for key, value in os.environ.items():
    if key.startswith('GOOGLE'):
        print(f"{key} = {value[:50]}...")

print(f"\nPath to .env file: {os.path.abspath('.env')}")
print(f"Does .env exist? {os.path.exists('.env')}")

# Read .env file directly
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        content = f.read()
        print(f"\n.env file content (first 500 chars):")
        print(content[:500])
