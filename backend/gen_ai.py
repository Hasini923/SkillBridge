#!/usr/bin/env python3
"""
Test script using NEW google-genai package (not deprecated)
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

# Initialize client with new API
client = genai.Client(api_key=API_KEY)

print("\n🚀 Testing with google-genai package...\n")

# Test 1: Hello world
print("TEST 1: Simple test")
print("-" * 60)
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say 'Hello from Gemini 2.0 Flash'",
    )
    print(f"✅ Success: {response.text}\n")
except Exception as e:
    print(f"⚠️ gemini-2.0-flash failed: {str(e)[:50]}")
    print("Trying gemini-1.5-flash...\n")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Say 'Hello from Gemini'",
        )
        print(f"✅ Success with gemini-1.5-flash: {response.text}\n")
    except Exception as e2:
        print(f"❌ Both failed: {e2}\n")
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
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
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
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
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
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    print("📥 Response:")
    print(response.text)
    print("\n✅ Success!\n")
except Exception as e:
    print(f"❌ Failed: {e}\n")

print("=" * 60)
print("✅ All tests completed!")
print("=" * 60)
print("\nNext: Run 'python app.py' to start Flask server")