#!/usr/bin/env python3
"""
Simple Gemini API test - find working model first
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=API_KEY)

# Try different models
print("🔍 Finding available model...")

models_to_try = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-pro",
    "gemini-1.5-pro",
]

model = None
model_name = None

for m in models_to_try:
    try:
        test_model = genai.GenerativeModel(m)
        response = test_model.generate_content("Say hello")
        model = test_model
        model_name = m
        print(f"✅ Using model: {model_name}\n")
        break
    except Exception as e:
        print(f"❌ {m} failed: {str(e)[:50]}")

if not model:
    print("❌ No working model found!")
    exit(1)

# Test 1: Simple skill extraction
print("="*80)
print("TEST 1: Skill Extraction")
print("="*80)

resume = """
John Doe - Senior Software Engineer

Skills:
- Python, JavaScript, React, Django, Flask, Node.js
- PostgreSQL, MongoDB, Redis
- AWS, Docker, Kubernetes, Git
- Leadership, Communication, Problem Solving
"""

prompt = f"""Extract skills from this resume:

{resume}

Return ONLY JSON:
{{"technical": [], "soft": []}}
"""

try:
    response = model.generate_content(prompt)
    print("\n📥 Response:")
    print(response.text)
    print("\n✅ Success!")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Skill gaps
print("\n" + "="*80)
print("TEST 2: Skill Gaps Analysis")
print("="*80)

prompt2 = """Current skills: Python, JavaScript, React, Node.js
Target role: Machine Learning Engineer

What 5 skills should they learn?

Return ONLY JSON:
{"skill_gaps": []}
"""

try:
    response = model.generate_content(prompt2)
    print("\n📥 Response:")
    print(response.text)
    print("\n✅ Success!")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Roadmap
print("\n" + "="*80)
print("TEST 3: Learning Roadmap")
print("="*80)

prompt3 = """Create a 3-phase learning roadmap (4 weeks each) to become a Machine Learning Engineer.

Return ONLY JSON:
{"roadmap": []}
"""

try:
    response = model.generate_content(prompt3)
    print("\n📥 Response:")
    print(response.text)
    print("\n✅ Success!")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*80)
print("✅ All tests complete!")
print("="*80)