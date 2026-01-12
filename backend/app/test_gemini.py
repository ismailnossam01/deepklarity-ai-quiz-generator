"""
Test Gemini API and list available models
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file!")
    exit(1)

print(f"✅ API Key found: {api_key[:10]}...")

# Configure Gemini
genai.configure(api_key=api_key)

print("\n" + "="*60)
print("Available Models:")
print("="*60)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Methods: {model.supported_generation_methods}")
            print()
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\nTrying alternative API key format...")
    
print("\n" + "="*60)
print("Testing model access:")
print("="*60)

# Try different model names
model_names = [
    'gemini-pro',
    'gemini-1.5-pro',
    'gemini-1.5-flash',
    'gemini-1.5-flash-latest',
    'models/gemini-pro',
    'models/gemini-1.5-pro',
    'models/gemini-1.5-flash',
]

for model_name in model_names:
    try:
        print(f"\nTrying: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello'")
        print(f"   ✅ SUCCESS! Response: {response.text[:50]}")
        print(f"   👉 USE THIS MODEL: {model_name}")
        break
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")

print("\n" + "="*60)