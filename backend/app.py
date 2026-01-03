from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import os
import uuid
import pdfplumber
import json
import time
import requests
from firebase_admin import credentials, firestore, initialize_app

# ================== LOAD ENV ==================
load_dotenv()

app = Flask(__name__)
CORS(app)

# ================== ROLE SKILL MAP ==================
ROLE_SKILL_MAP = {
    "Machine Learning Engineer": [
        "Python", "NumPy", "Pandas", "Scikit-learn",
        "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch",
        "Statistics", "Linear Algebra",
        "Model Deployment", "MLOps"
    ],
    "Data Scientist": [
        "Python", "Pandas", "NumPy",
        "Data Analysis", "Statistics",
        "Machine Learning", "SQL",
        "Data Visualization", "Power BI"
    ],
    "Backend Engineer": [
        "Python", "Java", "Node.js",
        "APIs", "Databases",
        "SQL", "System Design",
        "Docker", "Cloud"
    ]
}

# ================== FIREBASE ==================
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized")
except Exception as e:
    print(f"⚠️ Firebase error: {e}")
    db = None

# ================== CLOUDINARY ==================
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# ================== GEMINI ==================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)

# ================== HELPERS ==================

def normalize_skill(skill):
    return skill.lower().replace("-", " ").strip()

def normalize_skills(skills):
    return set(normalize_skill(s) for s in skills if isinstance(s, str))

def parse_json_response(text):
    try:
        if "```" in text:
            text = text.split("```")[1]
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end+1]
        return json.loads(text)
    except:
        return {}

def call_gemini_api(prompt, retries=3):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1024
        }
    }

    for _ in range(retries):
        try:
            r = requests.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                json=payload,
                timeout=30
            )
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            time.sleep(1)
    return ""

# ================== CORE LOGIC ==================

def extract_skills_from_resume(resume_text):
    prompt = f"""
Return ONLY JSON.

Extract skills from this resume:
{resume_text[:2000]}

Format:
{{
  "technical": ["Python"],
  "tools": ["Git"],
  "soft": ["Communication"],
  "languages": ["Python"]
}}
"""
    text = call_gemini_api(prompt)
    result = parse_json_response(text)

    return result if result else {
        "technical": ["Python"],
        "tools": ["Git"],
        "soft": [],
        "languages": []
    }

def generate_role_skills_from_gemini(role):
    prompt = f"""
Return ONLY JSON.

List 8–12 core skills for role: {role}

Format:
{{ "skills": ["Skill1", "Skill2"] }}
"""
    text = call_gemini_api(prompt)
    result = parse_json_response(text)
    return result.get("skills", [])

def analyze_skill_gaps(current_skills, target_role):
    target_role = target_role.strip()
    role_skills = ROLE_SKILL_MAP.get(target_role)

    if not role_skills:
        role_skills = generate_role_skills_from_gemini(target_role)
        if db and role_skills:
            db.collection("role_skills").document(target_role).set({
                "skills": role_skills,
                "source": "gemini",
                "timestamp": firestore.SERVER_TIMESTAMP
            })

    if not role_skills:
        return []

    resume_skills = normalize_skills(
        current_skills.get("technical", []) +
        current_skills.get("tools", [])
    )

    gaps = []
    for skill in role_skills:
        if normalize_skill(skill) not in resume_skills:
            gaps.append({
                "skill": skill,
                "importance": "High" if skill in role_skills[:6] else "Medium",
                "proficiency": 0,
                "learning_resource": f"Learn {skill} (Coursera / YouTube)"
            })

    return gaps

def calculate_match_score(skill_gaps):
    score = max(30, 100 - len(skill_gaps) * 5)
    return {
        "match_score": score,
        "readiness": "Moderate",
        "timeline_months": 3,
        "difficulty": "Moderate"
    }

def generate_roadmap(skill_gaps, target_role):
    gaps = [g["skill"] for g in skill_gaps[:5]]

    if not gaps:
        return [{
            "week": "1–12",
            "phase": "Job Readiness",
            "focus": f"Strengthen profile for {target_role}",
            "tasks": ["Advanced project", "Interview prep"]
        }]

    prompt = f"""
Return ONLY JSON.

Create a 12-week roadmap for {target_role}
Missing skills: {", ".join(gaps)}

Format:
{{ "roadmap": [{{ "week": "1-3", "phase": "Foundations", "focus": "...", "tasks": ["..."] }}] }}
"""
    text = call_gemini_api(prompt)
    result = parse_json_response(text)

    if result.get("roadmap"):
        return result["roadmap"]

    return [{
        "week": "1–3",
        "phase": "Foundations",
        "focus": f"Learn {gaps[0]}",
        "tasks": [f"Study {gaps[0]}", "Build mini project"]
    }]


def generate_weekly_tasks(skill_gaps, target_role):
    """
    Generate AI-driven weekly tasks based on skill gaps.
    Always returns tasks.
    """

    gap_skills = [gap["skill"] for gap in skill_gaps[:5]]

    # If no gaps, still give improvement tasks
    if not gap_skills:
        return [
            {
                "week": 1,
                "task": f"Build an advanced project related to {target_role}",
                "outcome": "Strengthen existing skills"
            },
            {
                "week": 2,
                "task": "Refactor and optimize an old project",
                "outcome": "Improve code quality"
            }
        ]

    prompt = f"""
Return ONLY valid JSON.

Target role: {target_role}
Skills to improve: {", ".join(gap_skills)}

Create 6 weekly tasks.
Each task must include:
- week (number)
- task (actionable)
- outcome (what user gains)

Format:
{{
  "weekly_tasks": [
    {{
      "week": 1,
      "task": "Learn NumPy basics and solve 20 problems",
      "outcome": "Comfort with numerical computing"
    }}
  ]
}}
"""

    try:
        text = call_gemini_api(prompt)
        result = parse_json_response(text)

        tasks = result.get("weekly_tasks")
        if isinstance(tasks, list) and len(tasks) > 0:
            return tasks

    except Exception as e:
        print("Weekly task generation failed:", e)

    # 🔒 FINAL FALLBACK (NEVER EMPTY)
    tasks = []
    for i, skill in enumerate(gap_skills[:3], start=1):
        tasks.append({
            "week": i,
            "task": f"Study and practice {skill}",
            "outcome": f"Basic proficiency in {skill}"
        })

    return tasks


def identify_strengths():
    return {
        "strengths": ["Strong programming foundation", "Fast learner"],
        "advantages": ["Resume-driven AI analysis"]
    }

# ================== ROUTES ==================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "SkillBridge API running"}), 200

@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    resume_text = data.get("resume_text")
    target_role = data.get("target_role")

    if not resume_text:
        return jsonify({"error": "resume_text is required"}), 400

    if not target_role:
        return jsonify({"error": "target_role is required"}), 400

    current_skills = extract_skills_from_resume(resume_text)
    skill_gaps = analyze_skill_gaps(current_skills, target_role)
    match = calculate_match_score(skill_gaps)
    roadmap = generate_roadmap(skill_gaps, target_role) 
    weekly_tasks = generate_weekly_tasks(skill_gaps, target_role)
    
    user_id = data.get("user_id", "anonymous")

    if db and weekly_tasks:
        progress_doc = {
            "user_id": user_id,
            "target_role": target_role,
            "weeklyTasks": [
                {**task, "completed": False} for task in weekly_tasks
            ],
            "completedCount": 0,
            "totalTasks": len(weekly_tasks),
            "progressPercent": 0,
            "updatedAt": firestore.SERVER_TIMESTAMP
        }

        db.collection("user_progress").document(user_id).set(progress_doc)

    strengths = identify_strengths()

    return jsonify({
    "targetRole": target_role,
    "currentSkills": current_skills,
    "skillGaps": skill_gaps,
    "matchScore": match["match_score"],
    "readiness": match["readiness"],
    "timelineMonths": match["timeline_months"],
    "difficulty": match["difficulty"],
    "roadmap": roadmap,
    "weeklyTasks": weekly_tasks,   # 👈 ADD THIS
    "strengths": strengths["strengths"],
    "competitiveAdvantages": strengths["advantages"]
}), 200
    
@app.route("/complete-task", methods=["POST"])
def complete_task():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json(silent=True)
    user_id = data.get("user_id")
    week = data.get("week")

    if not user_id or week is None:
        return jsonify({"error": "user_id and week required"}), 400

    doc_ref = db.collection("user_progress").document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"error": "Progress not found"}), 404

    progress = doc.to_dict()
    tasks = progress.get("weeklyTasks", [])

    completed = 0
    for task in tasks:
        if task["week"] == week:
            task["completed"] = True
        if task.get("completed"):
            completed += 1

    total = len(tasks)
    percent = int((completed / total) * 100) if total else 0

    doc_ref.update({
        "weeklyTasks": tasks,
        "completedCount": completed,
        "progressPercent": percent,
        "updatedAt": firestore.SERVER_TIMESTAMP
    })

    return jsonify({
        "message": "Task marked as completed",
        "progressPercent": percent
    }), 200
    
@app.route("/progress/<user_id>", methods=["GET"])
def get_progress(user_id):
    doc = db.collection("user_progress").document(user_id).get()

    if not doc.exists:
        return jsonify({"error": "Progress not found"}), 404

    return jsonify(doc.to_dict()), 200




@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# ================== RUN ==================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

















# from flask import Flask, request, jsonify
# from firebase_admin import credentials, firestore, initialize_app
# from flask_cors import CORS
# from dotenv import load_dotenv
# import cloudinary
# import cloudinary.uploader
# import os
# import uuid
# import pdfplumber
# import json
# import time
# import requests

# # ================== LOAD ENV ==================
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# # ================== ROLE SKILL MAP ==================
# ROLE_SKILL_MAP = {
#     "Machine Learning Engineer": [
#         "Python", "NumPy", "Pandas", "Scikit-learn",
#         "Machine Learning", "Deep Learning",
#         "TensorFlow", "PyTorch",
#         "Statistics", "Linear Algebra",
#         "Model Deployment", "MLOps"
#     ],
#     "Data Scientist": [
#         "Python", "Pandas", "NumPy",
#         "Data Analysis", "Statistics",
#         "Machine Learning", "SQL",
#         "Data Visualization", "Power BI"
#     ],
#     "Backend Engineer": [
#         "Python", "Java", "Node.js",
#         "APIs", "Databases",
#         "SQL", "System Design",
#         "Docker", "Cloud"
#     ]
# }

# # ================== FIREBASE ==================
# try:
#     cred = credentials.Certificate("serviceAccountKey.json")
#     initialize_app(cred)
#     db = firestore.client()
#     print("✅ Firebase initialized")
# except Exception as e:
#     print(f"⚠️ Firebase error: {e}")
#     db = None

# # ================== CLOUDINARY ==================
# cloudinary.config(
#     cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
#     api_key=os.getenv("CLOUDINARY_API_KEY"),
#     api_secret=os.getenv("CLOUDINARY_API_SECRET")
# )
# print("✅ Cloudinary configured")

# # ================== GEMINI ==================
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY missing")

# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
# print("✅ Gemini API configured")

# # ================== HELPERS ==================

# def normalize_skill(skill):
#     return skill.lower().replace("-", " ").strip()

# def normalize_skills(skills):
#     return set(normalize_skill(s) for s in skills if isinstance(s, str))

# def parse_json_response(text):
#     try:
#         if "```" in text:
#             text = text.split("```")[1]
#         start = text.find("{")
#         end = text.rfind("}")
#         if start != -1 and end != -1:
#             text = text[start:end+1]
#         return json.loads(text)
#     except:
#         return {}

# def call_gemini_api(prompt, retries=3):
#     payload = {
#         "contents": [{"parts": [{"text": prompt}]}],
#         "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}
#     }
#     for _ in range(retries):
#         try:
#             r = requests.post(
#                 f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
#                 json=payload,
#                 timeout=30
#             )
#             if r.status_code == 200:
#                 return r.json()["candidates"][0]["content"]["parts"][0]["text"]
#         except:
#             time.sleep(1)
#     return ""

# # ================== CORE AI LOGIC ==================

# def extract_skills_from_resume(resume_text):
#     prompt = f"""
# Return ONLY JSON.

# Extract technical skills, tools, soft skills from this resume:

# {resume_text[:2000]}

# Format:
# {{
#   "technical": ["Python"],
#   "tools": ["Git"],
#   "soft": ["Communication"],
#   "languages": ["Python"]
# }}
# """
#     try:
#         text = call_gemini_api(prompt)
#         result = parse_json_response(text)
#         return result if result else {
#             "technical": ["Python"],
#             "tools": ["Git"],
#             "soft": [],
#             "languages": []
#         }
#     except:
#         return {"technical": ["Python"], "tools": ["Git"], "soft": [], "languages": []}

# def generate_role_skills_from_gemini(role):
#     prompt = f"""
# Return ONLY JSON.

# List 8–12 core skills required for role: {role}

# Format:
# {{ "skills": ["Skill1", "Skill2"] }}
# """
#     try:
#         text = call_gemini_api(prompt)
#         result = parse_json_response(text)
#         return result.get("skills", [])
#     except:
#         return []

# def analyze_skill_gaps(current_skills, target_role):
#     target_role = target_role.strip()

#     role_skills = ROLE_SKILL_MAP.get(target_role)

#     if not role_skills:
#         role_skills = generate_role_skills_from_gemini(target_role)
#         if db and role_skills:
#             db.collection("role_skills").document(target_role).set({
#                 "skills": role_skills,
#                 "source": "gemini",
#                 "timestamp": firestore.SERVER_TIMESTAMP
#             })

#     if not role_skills:
#         return []

#     resume_skills = normalize_skills(
#         current_skills.get("technical", []) +
#         current_skills.get("tools", [])
#     )

#     gaps = []
#     for skill in role_skills:
#         if normalize_skill(skill) not in resume_skills:
#             gaps.append({
#                 "skill": skill,
#                 "importance": "High" if skill in role_skills[:6] else "Medium",
#                 "proficiency": 0,
#                 "learning_resource": f"Learn {skill} (Coursera / YouTube)"
#             })

#     return gaps

# def calculate_match_score(current_skills, skill_gaps, target_role):
#     return {
#         "match_score": max(30, 100 - len(skill_gaps) * 5),
#         "readiness": "Moderate",
#         "timeline_months": 3,
#         "difficulty": "Moderate"
#     }

# def generate_roadmap(current_skills, skill_gaps, target_role):
#     gaps = [g["skill"] for g in skill_gaps[:5]]

#     if not gaps:
#         return [{
#             "week": "1-12",
#             "phase": "Job Readiness",
#             "focus": f"Strengthen profile for {target_role}",
#             "tasks": ["Build advanced project", "Prepare interviews"]
#         }]

#     prompt = f"""
# Return ONLY JSON.

# Create a 12-week roadmap for {target_role}
# Missing skills: {", ".join(gaps)}

# Format:
# {{ "roadmap": [{{ "week": "1-3", "phase": "Foundations", "focus": "...", "tasks": ["..."] }}] }}
# """
#     try:
#         text = call_gemini_api(prompt)
#         result = parse_json_response(text)
#         if result.get("roadmap"):
#             return result["roadmap"]
#     except:
#         pass

#     return [{
#         "week": "1-3",
#         "phase": "Foundations",
#         "focus": f"Learn {gaps[0]}",
#         "tasks": [f"Study {gaps[0]}", f"Build mini project"]
#     }]

# def identify_strengths(resume_text, current_skills, target_role):
#     return {
#         "strengths": ["Strong programming foundation", "Good learning ability"],
#         "advantages": ["Resume-driven AI analysis"]
#     }

# # ================== ROUTES ==================

# @app.route("/health")
# def health():
#     return jsonify({"status": "ok"})

# @app.route("/analyze-resume", methods=["POST"])
# def analyze_resume():
#     data = request.get_json()
#     resume_text = data.get("resume_text", "")
#     target_role = data.get("target_role", "")

#     current_skills = extract_skills_from_resume(resume_text)
#     skill_gaps = analyze_skill_gaps(current_skills, target_role)
#     match = calculate_match_score(current_skills, skill_gaps, target_role)
#     roadmap = generate_roadmap(current_skills, skill_gaps, target_role)
#     strengths = identify_strengths(resume_text, current_skills, target_role)

#     return jsonify({
#         "targetRole": target_role,
#         "currentSkills": current_skills,
#         "skillGaps": skill_gaps,
#         "matchScore": match["match_score"],
#         "readiness": match["readiness"],
#         "timelineMonths": match["timeline_months"],
#         "difficulty": match["difficulty"],
#         "roadmap": roadmap,
#         "strengths": strengths["strengths"],
#         "competitiveAdvantages": strengths["advantages"]
#     })

# # ================== RUN ==================
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)





















































# ROLE_SKILL_MAP = {
#     "Machine Learning Engineer": [
#         "Python", "NumPy", "Pandas", "Scikit-learn",
#         "Machine Learning", "Deep Learning",
#         "TensorFlow", "PyTorch",
#         "Statistics", "Linear Algebra",
#         "Model Deployment", "MLOps"
#     ],
#     "Data Scientist": [
#         "Python", "Pandas", "NumPy",
#         "Data Analysis", "Statistics",
#         "Machine Learning", "SQL",
#         "Data Visualization", "Power BI"
#     ],
#     "Backend Engineer": [
#         "Python", "Java", "Node.js",
#         "APIs", "Databases",
#         "SQL", "System Design",
#         "Docker", "Cloud"
#     ]
# }

# from flask import Flask, request, jsonify
# from firebase_admin import credentials, firestore, initialize_app
# from flask_cors import CORS
# from dotenv import load_dotenv
# import cloudinary
# import cloudinary.uploader
# import os
# import uuid
# import pdfplumber
# import json
# import time
# import requests

# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# # ================== FIREBASE ==================
# try:
#     cred = credentials.Certificate("serviceAccountKey.json")
#     initialize_app(cred)
#     db = firestore.client()
#     print("✅ Firebase initialized")
# except Exception as e:
#     print(f"⚠️ Firebase error: {e}")
#     db = None

# # ================== CLOUDINARY ==================
# cloudinary.config(
#     cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
#     api_key=os.getenv("CLOUDINARY_API_KEY"),
#     api_secret=os.getenv("CLOUDINARY_API_SECRET")
# )
# print("✅ Cloudinary configured")

# # ================== GEMINI API (REST) ==================
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY not found in environment")

# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
# print("✅ Gemini API configured (REST)")

# UPLOAD_LIMIT = 3


# # ================== UTILITY FUNCTIONS ==================

# def parse_json_response(response_text):
#     """Safely parse JSON from API response"""
#     try:
#         # Remove markdown code blocks
#         if '```json' in response_text:
#             response_text = response_text.split('```json')[1].split('```')[0]
#         elif '```' in response_text:
#             response_text = response_text.split('```')[1].split('```')[0]
        
#         response_text = response_text.strip()
        
#         # Try to find JSON object if wrapped in text
#         if not response_text.startswith('{'):
#             # Find first { and last }
#             start = response_text.find('{')
#             end = response_text.rfind('}')
#             if start != -1 and end != -1:
#                 response_text = response_text[start:end+1]
        
#         result = json.loads(response_text)
#         print(f"✅ Parsed JSON: {str(result)[:100]}")
#         return result
#     except json.JSONDecodeError as e:
#         print(f"❌ JSON Parse Error: {str(e)}")
#         print(f"Response was: {response_text[:300]}")
#         return {}


# def call_gemini_api(prompt, retry_count=3):
#     """Call Gemini API via REST with retry logic"""
#     headers = {
#         "Content-Type": "application/json",
#     }
    
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {
#                         "text": prompt
#                     }
#                 ]
#             }
#         ],
#         "generationConfig": {
#             "temperature": 0.3,
#             "maxOutputTokens": 1024,
#         }
#     }
    
#     for attempt in range(retry_count):
#         try:
#             response = requests.post(
#                 f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
#                 headers=headers,
#                 json=payload,
#                 timeout=30
#             )
            
#             if response.status_code == 200:
#                 result = response.json()
#                 if "candidates" in result and len(result["candidates"]) > 0:
#                     return result["candidates"][0]["content"]["parts"][0]["text"]
#                 else:
#                     raise Exception("No candidates in response")
#             elif response.status_code == 429:  # Rate limited
#                 if attempt < retry_count - 1:
#                     wait_time = (attempt + 1) * 2
#                     print(f"⏱️ Rate limited. Waiting {wait_time}s...")
#                     time.sleep(wait_time)
#                     continue
#                 else:
#                     raise Exception(f"Rate limited after {retry_count} attempts")
#             else:
#                 error_msg = response.text
#                 print(f"API Error ({response.status_code}): {error_msg[:200]}")
#                 raise Exception(f"API Error: {response.status_code}")
#         except requests.exceptions.Timeout:
#             if attempt < retry_count - 1:
#                 print(f"Timeout, retrying... ({attempt + 1}/{retry_count})")
#                 time.sleep(2)
#                 continue
#             raise
#         except Exception as e:
#             if attempt < retry_count - 1:
#                 print(f"Attempt {attempt + 1} failed: {str(e)[:50]}")
#                 time.sleep(1)
#                 continue
#             raise
    
#     return None


# def extract_skills_from_resume(resume_text):
#     """Extract current skills using Gemini"""
#     prompt = f"""IMPORTANT: You MUST return ONLY valid JSON. No other text.

# Extract ALL skills from this resume:

# RESUME:
# {resume_text[:2000]}

# Find:
# 1. All programming languages and technical frameworks
# 2. All soft skills
# 3. All tools and platforms
# 4. All programming languages

# Return ONLY this JSON:
# {{"technical": ["Python", "JavaScript", "React", "Django", "SQL", "AWS", "Docker"], "soft": ["Leadership", "Communication", "Problem Solving", "Team Work"], "tools": ["Git", "Docker", "VS Code", "Jira"], "languages": ["Python", "JavaScript", "SQL"]}}

# CRITICAL: Start with {{ and end with }}. No text before or after JSON."""
    
#     try:
#         response_text = call_gemini_api(prompt)
#         result = parse_json_response(response_text)
#         if not result or not result.get('technical'):
#             print("⚠️ Empty skills, using defaults")
#             return {
#                 "technical": ["Python", "JavaScript", "React"],
#                 "soft": ["Communication", "Problem Solving"],
#                 "tools": ["Git", "Docker"],
#                 "languages": ["Python", "JavaScript"]
#             }
#         return result
#     except Exception as e:
#         print(f"Error extracting skills: {e}")
#         return {"technical": ["Python", "JavaScript"], "soft": ["Communication"], "tools": ["Git"], "languages": ["Python"]}

# def normalize_skills(skills):
#     return set(skill.lower().strip() for skill in skills)

# def normalize_skills(skills):
#     if not skills:
#         return set()
#     return set(skill.lower().strip() for skill in skills if isinstance(skill, str))

# def analyze_skill_gaps(current_skills, target_role):
#     target_role = target_role.strip()
#     role_skills = ROLE_SKILL_MAP.get(target_role)

#     if not role_skills:
#         role_skills = generate_role_skills_from_gemini(target_role)

        
#         if db and role_skills:
#             db.collection("role_skills").document(target_role).set({
#                 "skills": role_skills,
#                 "source": "gemini",
#                 "timestamp": firestore.SERVER_TIMESTAMP
#             })

#     if not current_skills or not role_skills:
#         return []

#     resume_skills = normalize_skills(
#         current_skills.get("technical", []) +
#         current_skills.get("tools", [])
#     )

#     gaps = []
#     for skill in role_skills:
#         if skill.lower() not in resume_skills:
#             gaps.append({
#                 "skill": skill,
#                 "importance": "High" if skill in role_skills[:6] else "Medium",
#                 "proficiency": 0,
#                 "learning_resource": f"Learn {skill} (Coursera / YouTube)"
#             })

#     return gaps




# def calculate_match_score(current_skills, skill_gaps, target_role):
#     """Calculate match score"""
#     current_count = len(current_skills.get('technical', []))
#     gaps_count = len(skill_gaps)
#     high_gaps = sum(1 for gap in skill_gaps if gap.get('importance') == 'High')
    
#     prompt = f"""Candidate Profile:
# - Technical skills: {current_count}
# - Target role: {target_role}
# - Skills to learn: {gaps_count} ({high_gaps} high priority)

# Calculate a realistic match score (0-100) for this {target_role} position.

# Return ONLY JSON:
# {{
#     "match_score": 65,
#     "readiness": "Moderate",
#     "timeline_months": 3,
#     "difficulty": "Moderate"
# }}

# readiness: "High", "Moderate", or "Low"
# difficulty: "Easy", "Moderate", or "Hard"
# Return ONLY JSON."""
    
#     try:
#         response_text = call_gemini_api(prompt)
#         result = parse_json_response(response_text)
#         return result
#     except Exception as e:
#         print(f"Error calculating score: {e}")
#         return {"match_score": 50, "readiness": "Moderate", "timeline_months": 3, "difficulty": "Moderate"}


# def generate_roadmap(current_skills, skill_gaps, target_role):
#     """
#     Generate a 12-week roadmap. Always returns a roadmap.
#     """

#     # Extract missing skills safely
#     gaps_list = [gap["skill"] for gap in skill_gaps[:5]]
#     gaps_str = ", ".join(gaps_list)

#     # If no gaps, create an improvement roadmap
#     if not gaps_list:
#         return [
#             {
#                 "week": "1-4",
#                 "phase": "Skill Enhancement",
#                 "focus": f"Strengthen existing skills for {target_role}",
#                 "tasks": [
#                     "Revise core concepts",
#                     "Build one advanced project",
#                     "Optimize existing projects"
#                 ]
#             },
#             {
#                 "week": "5-8",
#                 "phase": "Advanced Practice",
#                 "focus": "Real-world problem solving",
#                 "tasks": [
#                     "Solve real datasets",
#                     "Improve performance & scalability",
#                     "Write technical documentation"
#                 ]
#             },
#             {
#                 "week": "9-12",
#                 "phase": "Job Readiness",
#                 "focus": "Portfolio & interviews",
#                 "tasks": [
#                     "Polish resume",
#                     "Mock interviews",
#                     "Apply to jobs"
#                 ]
#             }
#         ]

#     prompt = f"""IMPORTANT: Return ONLY valid JSON.

# Target role: {target_role}
# Missing skills: {gaps_str}

# Create a detailed 12-week roadmap.
# Split into 4 phases.
# Each phase must include:
# - week
# - phase
# - focus
# - tasks (list)

# Return ONLY JSON:
# {{
#   "roadmap": [
#     {{
#       "week": "1-2",
#       "phase": "Foundations",
#       "focus": "Core fundamentals",
#       "tasks": ["Task 1", "Task 2"]
#     }}
#   ]
# }}
# """

#     try:
#         response_text = call_gemini_api(prompt)
#         result = parse_json_response(response_text)

#         roadmap = result.get("roadmap")

#         # HARD GUARANTEE
#         if isinstance(roadmap, list) and len(roadmap) > 0:
#             return roadmap

#     except Exception as e:
#         print("Roadmap generation failed:", e)

#     # 🔒 FINAL FALLBACK (NEVER EMPTY)
#     return [
#         {
#             "week": "1-3",
#             "phase": "Foundations",
#             "focus": f"Learn {gaps_list[0]}",
#             "tasks": [
#                 f"Study basics of {gaps_list[0]}",
#                 f"Build a small project using {gaps_list[0]}"
#             ]
#         },
#         {
#             "week": "4-6",
#             "phase": "Core Skills",
#             "focus": f"Apply {gaps_list[1] if len(gaps_list) > 1 else gaps_list[0]}",
#             "tasks": [
#                 "Practice with datasets",
#                 "Implement algorithms"
#             ]
#         },
#         {
#             "week": "7-12",
#             "phase": "Job Readiness",
#             "focus": "Portfolio + Interview Prep",
#             "tasks": [
#                 "Build capstone project",
#                 "Prepare interview questions"
#             ]
#         }
#     ]


# def identify_strengths(resume_text, current_skills, target_role):
#     """Identify candidate's key strengths"""
#     current_tech = ", ".join(current_skills.get('technical', [])[:5])
    
#     prompt = f"""IMPORTANT: You MUST return ONLY valid JSON. No other text.

# Analyze candidate strengths for {target_role}.

# Resume: {resume_text[:1000]}
# Skills: {current_tech}

# Identify 4-5 key strengths and 2-3 competitive advantages.

# Return ONLY this JSON:
# {{"strengths": ["Strong foundation in multiple languages", "Experience with cloud platforms", "Proven ability to learn new technologies", "Good problem-solving skills", "Leadership experience"], "advantages": ["Already familiar with ML basics", "Strong software engineering foundation", "DevOps experience helps with deployment"]}}

# CRITICAL: Start with {{ and end with }}. No text before or after JSON."""
    
#     try:
#         response_text = call_gemini_api(prompt)
#         result = parse_json_response(response_text)
#         if not result.get('strengths'):
#             return {
#                 "strengths": [
#                     f"Strong foundation in {current_tech}",
#                     "Proven learning ability",
#                     "Relevant experience",
#                     "Problem-solving skills"
#                 ],
#                 "advantages": ["Good foundation", "Quick learner", "Relevant skills"]
#             }
#         return result
#     except Exception as e:
#         print(f"Error identifying strengths: {e}")
#         return {"strengths": ["Technical skills", "Learning ability", "Relevant experience"], "advantages": ["Learning ability", "Technical background"]}


# # ================== API ROUTES ==================

# @app.route("/health", methods=["GET"])
# def health_check():
#     return jsonify({"status": "SkillBridge API is running"}), 200


# @app.route("/upload-resume", methods=["POST"])
# def upload_resume():
#     """Upload resume to Cloudinary and extract text"""
#     try:
#         user_id = request.form.get("user_id", "anonymous")
#         file = request.files.get("resume")
#         target_role = request.form.get("target_role", "")

#         if not file:
#             return jsonify({"error": "Missing resume file"}), 400

#         # Upload to Cloudinary
#         upload_result = cloudinary.uploader.upload(
#             file,
#             resource_type="raw",
#             folder=f"resumes/{user_id}",
#             public_id=str(uuid.uuid4())
#         )
#         file_url = upload_result["secure_url"]

#         # Extract text from PDF
#         extracted_text = ""
#         file.seek(0)
#         try:
#             with pdfplumber.open(file) as pdf:
#                 for page in pdf.pages:
#                     extracted_text += page.extract_text() or ""
#         except Exception as pdf_error:
#             print(f"PDF extraction error: {pdf_error}")

#         # Save to Firebase if available
#         if db:
#             db.collection("resumes").add({
#                 "user_id": user_id,
#                 "file_url": file_url,
#                 "text": extracted_text,
#                 "target_role": target_role
#             })

#         return jsonify({
#             "message": "Resume uploaded successfully",
#             "file_url": file_url,
#             "extracted_text": extracted_text[:500],
#             "text_length": len(extracted_text)
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def generate_role_skills_from_gemini(target_role):
#     prompt = f"""Return ONLY JSON.

# List 8–12 core skills required for the role: {target_role}

# Format:
# {{ "skills": ["Skill1", "Skill2", "Skill3"] }}
# """

#     try:
#         response = call_gemini_api(prompt)
#         result = parse_json_response(response)
#         return result.get("skills", [])
#     except:
#         return []


# @app.route("/analyze-resume", methods=["POST"])
# def analyze_resume():
#     """Complete skill analysis pipeline"""
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "Invalid JSON"}), 400

#         resume_text = data.get("resume_text", "")
#         target_role = data.get("target_role", "")

#         if not resume_text or not target_role:
#             return jsonify({"error": "Missing resume_text or target_role"}), 400

#         print(f"\n🔄 Analyzing resume for: {target_role}")

#         # STEP 1: Extract skills ONCE
#         print("📍 Step 1: Extracting current skills...")
#         current_skills = extract_skills_from_resume(resume_text) or {
#             "technical": [],
#             "tools": [],
#             "languages": [],
#             "soft": []
#         }
#         print(f"   ✅ Found {len(current_skills.get('technical', []))} technical skills")

#         # STEP 2: Analyze skill gaps (deterministic)
#         print("📍 Step 2: Analyzing skill gaps...")
#         skill_gaps = analyze_skill_gaps(current_skills, target_role) or []
#         print("FINAL SKILL GAPS:", skill_gaps)

#         # STEP 3: Calculate match score
#         print("📍 Step 3: Calculating match score...")
#         match_info = calculate_match_score(current_skills, skill_gaps, target_role)
#         print(f"   ✅ Match score: {match_info.get('match_score', 'N/A')}%")

#         # STEP 4: Generate roadmap (AI, grounded)
#         print("📍 Step 4: Generating learning roadmap...")
#         roadmap = generate_roadmap(current_skills, skill_gaps, target_role)
#         print(f"   ✅ Created {len(roadmap)} learning phases")

#         # STEP 5: Identify strengths
#         print("📍 Step 5: Identifying strengths...")
#         strengths = identify_strengths(resume_text, current_skills, target_role)
#         print(f"   ✅ Found {len(strengths.get('strengths', []))} key strengths")

#         # FINAL RESPONSE
#         analysis = {
#             "targetRole": target_role,
#             "currentSkills": current_skills,
#             "skillGaps": skill_gaps,
#             "matchScore": match_info.get("match_score", 50),
#             "readiness": match_info.get("readiness", "Moderate"),
#             "timelineMonths": match_info.get("timeline_months", 3),
#             "difficulty": match_info.get("difficulty", "Moderate"),
#             "roadmap": roadmap,
#             "strengths": strengths.get("strengths", []),
#             "competitiveAdvantages": strengths.get("advantages", [])
#         }

#         print("✅ Analysis complete!\n")
#         return jsonify(analysis), 200

#     except Exception as e:
#         print(f"❌ Error: {e}")
#         return jsonify({"error": str(e)}), 500



# @app.route("/full-analysis", methods=["POST"])
# def full_analysis():
#     """Combined upload + analyze in one request"""
#     try:
#         user_id = request.form.get("user_id", "anonymous")
#         file = request.files.get("resume")
#         target_role = request.form.get("target_role", "")

#         if not file or not target_role:
#             return jsonify({"error": "Missing resume file or target_role"}), 400

#         # Upload to Cloudinary
#         upload_result = cloudinary.uploader.upload(
#             file,
#             resource_type="raw",
#             folder=f"resumes/{user_id}",
#             public_id=str(uuid.uuid4())
#         )
#         file_url = upload_result["secure_url"]

#         # Extract text
#         extracted_text = ""
#         file.seek(0)
#         try:
#             with pdfplumber.open(file) as pdf:
#                 for page in pdf.pages:
#                     extracted_text += page.extract_text() or ""
#         except:
#             pass

#         # Run full analysis
#         current_skills = extract_skills_from_resume(extracted_text)
#         skill_gaps = analyze_skill_gaps(current_skills, target_role)
#         match_info = calculate_match_score(current_skills, skill_gaps, target_role)
#         roadmap = generate_roadmap(current_skills, skill_gaps, target_role)
#         strengths = identify_strengths(extracted_text, current_skills, target_role)

#         # Save to Firebase if available
#         if db:
#             db.collection("analyses").add({
#                 "user_id": user_id,
#                 "target_role": target_role,
#                 "file_url": file_url,
#                 "timestamp": firestore.SERVER_TIMESTAMP
#             })

#         return jsonify({
#             "resumeUrl": file_url,
#             "targetRole": target_role,
#             "currentSkills": current_skills,
#             "skillGaps": skill_gaps,
#             "matchScore": match_info.get('match_score', 50),
#             "readiness": match_info.get('readiness', 'Moderate'),
#             "timelineMonths": match_info.get('timeline_months', 3),
#             "difficulty": match_info.get('difficulty', 'Moderate'),
#             "roadmap": roadmap,
#             "strengths": strengths.get('strengths', []),
#             "competitiveAdvantages": strengths.get('advantages', [])
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({"error": "Endpoint not found"}), 404


# @app.errorhandler(500)
# def server_error(error):
#     return jsonify({"error": "Internal server error"}), 500


# if __name__ == "__main__":
#     print("\n" + "="*80)
#     print("🚀 SkillBridge Backend - Production Mode (Gemini REST API)")
#     print("="*80 + "\n")
#     app.run(debug=True, host="0.0.0.0", port=5000)