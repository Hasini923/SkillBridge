#!/usr/bin/env python3
"""
Find which Gemini models are actually available and working
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env")
    exit(1)

print(f"✅ API Key found: {API_KEY[:10]}...")
print("\n" + "="*80)
print("FINDING AVAILABLE GEMINI MODELS")
print("="*80 + "\n")

client = genai.Client(api_key=API_KEY)

# First, list all models
print("📋 Listing all available models...\n")
try:
    models = client.models.list()
    print("Available models:")
    for model in models:
        print(f"  - {model.name}")
    print()
except Exception as e:
    print(f"⚠️ Could not list models: {e}\n")

# Test individual models
print("="*80)
print("TESTING MODELS")
print("="*80 + "\n")

# Ordered by likelihood to work
models_to_test = [
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash",
    "gemini-2.0-pro-exp",
    "gemini-2.0-pro",
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-1.5-pro-001",
    "gemini-1.5-pro-vision",
]

working_models = []

for model_name in models_to_test:
    try:
        print(f"Testing {model_name}...", end=" ")
        response = client.models.generate_content(
            model=model_name,
            contents="Say 'hello'"
        )
        print(f"✅ WORKS")
        working_models.append(model_name)
    except Exception as e:
        error_code = str(e)[:50]
        print(f"❌ {error_code}")

print("\n" + "="*80)
if working_models:
    print(f"✅ {len(working_models)} WORKING MODEL(S) FOUND:")
    print("="*80)
    for i, model in enumerate(working_models, 1):
        print(f"\n{i}. {model}")
        print("   Use this in your code:")
        print(f"   GEMINI_MODEL = \"{model}\"")
else:
    print("❌ NO WORKING MODELS FOUND")
    print("="*80)
    print("\nPossible solutions:")
    print("1. Your API key might not have access to any models")
    print("2. You might be rate limited")
    print("3. Try again in a few minutes")
    print("\nOr try using a different API key from:")
    print("https://makersuite.google.com/app/apikey")

print("\n" + "="*80)