#!/usr/bin/env python3
"""
Test script for SkillBridge Flask API endpoints
Run this after starting Flask server: python app.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# ==================== TEST DATA ====================

SAMPLE_RESUME = """
John Doe
Senior Software Engineer | 5 years experience

Technical Skills:
- Languages: Python, JavaScript, Java, SQL, TypeScript
- Frontend: React, Vue.js, HTML5, CSS3, Tailwind
- Backend: Django, Flask, Node.js, Express, FastAPI
- Databases: PostgreSQL, MongoDB, MySQL, Redis
- Cloud: AWS (EC2, S3, Lambda), Google Cloud Platform
- DevOps: Docker, Kubernetes, GitHub Actions, Jenkins
- Tools: Git, Jira, VS Code, Postman, Linux

Experience:
- Senior Developer at TechCorp (2 years)
  * Led team of 5 engineers building microservices
  * Improved API performance by 40%
  * Mentored junior developers

- Full Stack Developer at StartupXYZ (3 years)
  * Built scalable web applications
  * Deployed to AWS and managed infrastructure
  * Collaborated with product and design teams

Education:
- BS Computer Science from State University
- AWS Certified Solutions Architect

Certifications:
- AWS Certified Solutions Architect Professional
- Google Cloud Professional Data Engineer (in progress)

Languages:
- English (native)
- Spanish (conversational)
"""

# ==================== TEST FUNCTIONS ====================

def test_health_check():
    """Test if API is running"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_analyze_resume():
    """Test skill analysis from resume text"""
    print("\n" + "="*60)
    print("TEST 2: Analyze Resume (JSON endpoint)")
    print("="*60)
    
    payload = {
        "resume_text": SAMPLE_RESUME,
        "target_role": "Machine Learning Engineer"
    }
    
    try:
        print("Sending request with target role: Machine Learning Engineer")
        response = requests.post(
            f"{BASE_URL}/analyze-resume",
            json=payload,
            timeout=60
        )
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nAnalysis Results:")
            print(f"  Match Score: {data.get('matchScore')}%")
            print(f"  Readiness: {data.get('readiness')}")
            print(f"  Timeline: {data.get('timelineMonths')} months")
            print(f"  Current Skills: {len(data.get('currentSkills', {}).get('technical', []))} technical")
            print(f"  Skill Gaps: {len(data.get('skillGaps', []))} gaps to fill")
            print(f"  Strengths: {len(data.get('strengths', []))} identified")
            print(f"  Roadmap Phases: {len(data.get('roadmap', []))} phases")
            print(f"  Weekly Tasks: {len(data.get('weeklyTasks', []))} tasks")
            print("\nWeekly Tasks:")
            for task in data.get("weeklyTasks", []):
             print(f"  Week {task['week']}: {task['task']}")

            
            print("\n📊 Full Response:")
            print(json.dumps(data, indent=2)[:1000] + "...")
        else:
            print(f"❌ Error: {response.json()}")
    except requests.Timeout:
        print("⏱️ Request timed out - Gemini API might be slow. Try again.")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_analyze_with_different_role():
    """Test with different target role"""
    print("\n" + "="*60)
    print("TEST 3: Analyze Resume (Different Role)")
    print("="*60)
    
    payload = {
        "resume_text": SAMPLE_RESUME,
        "target_role": "Data Scientist"
    }
    
    try:
        print("Sending request with target role: Data Scientist")
        response = requests.post(
            f"{BASE_URL}/analyze-resume",
            json=payload,
            timeout=60
        )
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nAnalysis Results:")
            print(f"  Target Role: {data.get('targetRole')}")
            print(f"  Match Score: {data.get('matchScore')}%")
            print(f"  Readiness: {data.get('readiness')}")
            print(f"  Timeline: {data.get('timelineMonths')} months")
        else:
            print(f"❌ Error: {response.json()}")
    except requests.Timeout:
        print("⏱️ Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_error_handling():
    """Test error handling"""
    print("\n" + "="*60)
    print("TEST 4: Error Handling")
    print("="*60)
    
    # Missing target role
    print("\nTest 4a: Missing target_role")
    payload = {"resume_text": SAMPLE_RESUME}
    response = requests.post(f"{BASE_URL}/analyze-resume", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Missing resume text
    print("\nTest 4b: Missing resume_text")
    payload = {"target_role": "Engineer"}
    response = requests.post(f"{BASE_URL}/analyze-resume", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Invalid JSON
    print("\nTest 4c: Invalid JSON")
    response = requests.post(
        f"{BASE_URL}/analyze-resume",
        data="invalid",
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


def test_multiple_roles():
    """Test analysis for multiple target roles"""
    print("\n" + "="*60)
    print("TEST 5: Multiple Target Roles Comparison")
    print("="*60)
    
    roles = [
        "Backend Engineer",
        "DevOps Engineer",
        "Cloud Architect",
        "Full Stack Developer"
    ]
    
    for role in roles:
        print(f"\n→ Analyzing for: {role}")
        payload = {
            "resume_text": SAMPLE_RESUME,
            "target_role": role
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/analyze-resume",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                score = data.get('matchScore', 'N/A')
                readiness = data.get('readiness', 'N/A')
                print(f"  ✅ Match: {score}% | Readiness: {readiness}")
            else:
                print(f"  ❌ Error: {response.json().get('error')}")
        except Exception as e:
            print(f"  ❌ Error: {e}")


def print_menu():
    """Print test menu"""
    print("\n" + "="*60)
    print("SkillBridge Flask API Test Suite")
    print("="*60)
    print("""
Choose a test:
1. Health Check
2. Analyze Resume (ML Engineer)
3. Analyze Resume (Data Scientist)
4. Error Handling
5. Multiple Roles Comparison
6. Run All Tests
0. Exit
""")


# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n🚀 SkillBridge API Test Suite")
    print(f"Target: {BASE_URL}")
    print("\nMake sure Flask server is running: python app.py")
    
    while True:
        print_menu()
        choice = input("Enter choice (0-6): ").strip()
        
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            test_health_check()
        elif choice == "2":
            test_analyze_resume()
        elif choice == "3":
            test_analyze_with_different_role()
        elif choice == "4":
            test_error_handling()
        elif choice == "5":
            test_multiple_roles()
        elif choice == "6":
            test_health_check()
            test_analyze_resume()
            test_analyze_with_different_role()
            test_error_handling()
            test_multiple_roles()
        else:
            print("Invalid choice")