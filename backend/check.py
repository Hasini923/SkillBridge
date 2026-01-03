#!/usr/bin/env python3
"""
Simple test using gemini-pro model
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

print(f"✅ API Key found: {API_KEY[:10]}...")
genai.configure(api_key=API_KEY)

# Use gemini-pro (most stable)
print("\n🚀 Testing gemini-pro model...\n")
model = genai.GenerativeModel("gemini-pro")

# Test 1: Hello world
print("TEST 1: Simple test")
print("-" * 60)
try:
    response = model.generate_content("Say 'Hello from Gemini Pro'")
    print(f"✅ Success: {response.text}\n")
except Exception as e:
    print(f"❌ Failed: {e}\n")
    exit(1)

# Test 2: Extract skills
print("TEST 2: Extract skills from resume")
print("-" * 60)

resume = """
John Doe - Senior Engineer
Python, JavaScript, React, Django, AWS, Docker
Leadership, Communication, Problem Solving
"""

prompt = f"""Extract skills from this resume and return as JSON.

Resume: {resume}

Return this format:
{{"technical": ["Python", "JavaScript"], "soft": ["Leadership"]}}
"""

try:
    response = model.generate_content(prompt)
    print("📥 Response:")
    print(response.text)
    print("\n✅ Success!\n")
except Exception as e:
    print(f"❌ Failed: {e}\n")

# Test 3: Skill gaps
print("TEST 3: Skill gaps for ML Engineer")
print("-" * 60)

prompt = """Current skills: Python, JavaScript, React

Target: Machine Learning Engineer

What 3 skills to learn?

Return: {"skills": ["skill1", "skill2"]}
"""

try:
    response = model.generate_content(prompt)
    print("📥 Response:")
    print(response.text)
    print("\n✅ Success!\n")
except Exception as e:
    print(f"❌ Failed: {e}\n")

# Test 4: Roadmap
print("TEST 4: 2-week learning roadmap")
print("-" * 60)

prompt = """Create a 2-week learning plan to become ML Engineer.

Return: {"week1": ["task1"], "week2": ["task2"]}
"""

try:
    response = model.generate_content(prompt)
    print("📥 Response:")
    print(response.text)
    print("\n✅ Success!\n")
except Exception as e:
    print(f"❌ Failed: {e}\n")

print("=" * 60)
print("✅ All tests completed!")
print("=" * 60)
print("\nNext: Run 'python app.py' to start Flask server")