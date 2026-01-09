from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import time
import requests
import re
from firebase_admin import credentials, firestore, initialize_app

load_dotenv()

app = Flask(__name__)
CORS(app)

# ================== COMPREHENSIVE ROLE SKILL MAP (50+ ROLES) ==================
ROLE_SKILL_MAP = {
    # WEB DEVELOPMENT
    "frontend engineer": [
        "JavaScript", "React", "Vue.js", "Angular", "TypeScript",
        "HTML", "CSS", "SASS", "Tailwind CSS", "Bootstrap",
        "Webpack", "Babel", "REST APIs", "GraphQL", "Redux",
        "State Management", "Responsive Design", "Web Performance",
        "Accessibility", "Jest", "Testing Library"
    ],
    "backend engineer": [
        "Python", "Java", "C#", "Node.js", "Go", "Ruby",
        "Django", "Flask", "Spring Boot", "Express.js", "Laravel",
        "APIs", "REST", "GraphQL", "Databases", "SQL", "MongoDB",
        "PostgreSQL", "MySQL", "Docker", "Kubernetes", "System Design",
        "Authentication", "Authorization", "Security"
    ],
    "full stack developer": [
        "JavaScript", "Python", "React", "Node.js", "Vue.js",
        "Angular", "TypeScript", "HTML", "CSS", "SQL", "MongoDB",
        "Django", "Flask", "Express.js", "PostgreSQL", "MySQL",
        "Docker", "APIs", "REST", "GraphQL", "Git", "DevOps",
        "Deployment", "AWS", "Heroku", "Firebase"
    ],
    "web developer": [
        "HTML", "CSS", "JavaScript", "React", "Vue.js", "Angular",
        "TypeScript", "Bootstrap", "Tailwind CSS", "Responsive Design",
        "Web Accessibility", "SEO", "Performance Optimization",
        "APIs", "REST", "Git", "Webpack", "NPM", "Package Management"
    ],
    
    # DATA & AI/ML
    "machine learning engineer": [
        "Python", "NumPy", "Pandas", "Scikit-learn", "TensorFlow",
        "PyTorch", "Keras", "OpenCV", "NLP", "Deep Learning",
        "Neural Networks", "Machine Learning", "Statistics", "Linear Algebra",
        "Data Preprocessing", "Model Training", "Model Evaluation",
        "Feature Engineering", "MLOps", "Model Deployment", "SQL"
    ],
    "data scientist": [
        "Python", "R", "SQL", "Pandas", "NumPy", "Scikit-learn",
        "TensorFlow", "PyTorch", "Matplotlib", "Seaborn", "Plotly",
        "Data Analysis", "Data Visualization", "Statistics", "Probability",
        "Machine Learning", "Deep Learning", "Tableau", "Power BI",
        "Excel", "Big Data", "Apache Spark"
    ],
    "data analyst": [
        "SQL", "Python", "R", "Tableau", "Power BI", "Excel",
        "Data Visualization", "Statistics", "Data Cleaning",
        "Data Mining", "Data Interpretation", "Pandas", "Matplotlib",
        "Google Analytics", "Dashboard Creation", "Report Writing",
        "Business Intelligence", "Google Sheets"
    ],
    "ai engineer": [
        "Python", "TensorFlow", "PyTorch", "Transformers", "BERT",
        "GPT", "NLP", "Computer Vision", "Deep Learning", "Machine Learning",
        "Neural Networks", "Prompt Engineering", "LLM Fine-tuning",
        "Model Deployment", "CUDA", "Hugging Face", "Langchain"
    ],
    
    # SECURITY
    "cybersecurity analyst": [
        "Network Security", "Firewalls", "VPN", "Encryption", "SSL/TLS",
        "Python", "Bash", "Linux", "Windows Security", "Penetration Testing",
        "SIEM", "IDS/IPS", "Malware Analysis", "Threat Detection",
        "Security Auditing", "Vulnerability Assessment", "Risk Management",
        "Compliance", "OWASP", "Ethical Hacking"
    ],
    "security engineer": [
        "Python", "Java", "C++", "Linux", "Windows", "Network Security",
        "Cryptography", "Encryption", "TLS/SSL", "OAuth", "JWT",
        "Secure Coding", "Application Security", "API Security",
        "Cloud Security", "AWS Security", "Azure Security", "Infrastructure",
        "Security Architecture", "Zero Trust"
    ],
    "penetration tester": [
        "Python", "Bash", "Linux", "Networking", "Web Security",
        "Kali Linux", "Metasploit", "Burp Suite", "Wireshark",
        "Network Scanning", "Vulnerability Exploitation", "Social Engineering",
        "Report Writing", "Security Assessment", "Firewall Bypass",
        "SQL Injection", "XSS", "OWASP Top 10"
    ],
    
    # CLOUD & DEVOPS
    "devops engineer": [
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "CI/CD",
        "Jenkins", "GitLab CI", "GitHub Actions", "Linux", "Bash",
        "Python", "Terraform", "Ansible", "CloudFormation", "Infrastructure as Code",
        "Monitoring", "Logging", "ELK Stack", "Prometheus", "Grafana"
    ],
    "cloud architect": [
        "AWS", "Azure", "Google Cloud", "Cloud Design", "Cloud Architecture",
        "Microservices", "Containers", "Kubernetes", "Docker", "Serverless",
        "Cloud Security", "Scalability", "High Availability", "Disaster Recovery",
        "Cost Optimization", "Infrastructure Design", "Load Balancing"
    ],
    "aws engineer": [
        "AWS", "EC2", "S3", "Lambda", "RDS", "DynamoDB", "API Gateway",
        "CloudFront", "Route 53", "IAM", "VPC", "CloudFormation",
        "SAM", "Python", "Node.js", "Terraform", "Infrastructure as Code",
        "Security", "Monitoring", "CloudWatch"
    ],
    
    # EMBEDDED & IOT
    "iot engineer": [
        "C", "C++", "Python", "Arduino", "ESP32", "Raspberry Pi",
        "Embedded Systems", "IoT", "RFID", "Bluetooth", "WiFi",
        "Microcontrollers", "Sensors", "Hardware Programming", "Firmware",
        "Real-time Systems", "Low-power Design", "Communication Protocols"
    ],
    "embedded systems engineer": [
        "C", "C++", "Assembly", "Real-time OS", "FreeRTOS", "Linux",
        "Microcontrollers", "ARM", "Embedded Linux", "Device Drivers",
        "Hardware Debugging", "JTAG", "GDB", "Build Systems", "Make",
        "Version Control", "Testing", "System Architecture"
    ],
    
    # MOBILE
    "ios developer": [
        "Swift", "Objective-C", "iOS", "Xcode", "UIKit", "SwiftUI",
        "Core Data", "Network Requests", "REST APIs", "JSON",
        "Git", "Cocoapods", "SPM", "Testing", "XCTest",
        "App Store Deployment", "iOS Guidelines", "Performance Optimization"
    ],
    "android developer": [
        "Java", "Kotlin", "Android Studio", "Android SDK", "XML",
        "Activities", "Fragments", "Services", "Content Providers",
        "Room Database", "SQLite", "REST APIs", "Retrofit", "Volley",
        "Firebase", "Push Notifications", "Google Play", "Material Design"
    ],
    "mobile app developer": [
        "React Native", "Flutter", "Dart", "JavaScript", "TypeScript",
        "Cross-platform Development", "iOS", "Android", "Firebase",
        "REST APIs", "GraphQL", "State Management", "Redux",
        "Navigation", "Testing", "App Store Deployment", "Google Play"
    ],
    
    # DATABASE
    "database administrator": [
        "SQL", "MySQL", "PostgreSQL", "Oracle", "MSSQL", "MongoDB",
        "Database Design", "Backup & Recovery", "Performance Tuning",
        "Indexing", "Query Optimization", "Replication", "High Availability",
        "Security", "Access Control", "Monitoring", "Troubleshooting"
    ],
    "database engineer": [
        "SQL", "NoSQL", "MongoDB", "Cassandra", "Redis", "Elasticsearch",
        "Database Design", "Schema Design", "Query Optimization", "Indexing",
        "Replication", "Clustering", "Sharding", "Data Warehousing",
        "ETL", "Performance Tuning", "Python", "Java"
    ],
    
    # QA & TESTING
    "qa engineer": [
        "Test Planning", "Test Case Design", "Manual Testing", "Automation Testing",
        "Selenium", "Cypress", "Appium", "JUnit", "TestNG", "Mocha",
        "Python", "Java", "JavaScript", "Bug Tracking", "JIRA",
        "Regression Testing", "Performance Testing", "Security Testing"
    ],
    "test automation engineer": [
        "Selenium", "Cypress", "Appium", "Python", "Java", "JavaScript",
        "Page Object Model", "Testing Frameworks", "Continuous Integration",
        "Jenkins", "GitHub Actions", "Performance Testing", "Load Testing",
        "JMeter", "Postman", "API Testing", "Test Data Management"
    ],
    
    # DEVREL & PRODUCT
    "developer advocate": [
        "Technical Writing", "Speaking", "Community Building", "Content Creation",
        "JavaScript", "Python", "APIs", "SDKs", "Documentation",
        "Blogging", "Video Creation", "Social Media", "Event Hosting",
        "Networking", "Public Relations", "Product Knowledge"
    ],
    "product manager": [
        "Product Strategy", "User Research", "Market Analysis", "Roadmapping",
        "Analytics", "Metrics", "A/B Testing", "User Experience",
        "Agile", "Scrum", "Communication", "Leadership", "Data Analysis",
        "SQL", "Tableau", "Competitive Analysis"
    ],
    "technical writer": [
        "Technical Writing", "Documentation", "API Documentation", "Markdown",
        "Git", "Sphinx", "MkDocs", "Asciidoc", "LaTeX", "Adobe Suite",
        "SEO", "UX Writing", "Content Strategy", "User Testing",
        "English", "Grammar", "Information Architecture"
    ],
    
    # AI/PROMPT ENGINEERING
    "prompt engineer": [
        "Prompt Engineering", "LLM", "ChatGPT", "GPT-4", "Claude",
        "BERT", "Transformers", "NLP", "Python", "Machine Learning",
        "Prompt Optimization", "Fine-tuning", "Model Evaluation",
        "Langchain", "Semantic Search", "Retrieval Augmented Generation",
        "Natural Language Processing"
    ],
    "llm engineer": [
        "Large Language Models", "Transformers", "PyTorch", "TensorFlow",
        "Hugging Face", "Fine-tuning", "Model Training", "CUDA",
        "Prompt Engineering", "Few-shot Learning", "In-context Learning",
        "Model Deployment", "API Development", "Python", "GPU Optimization"
    ],
    
    # SYSTEMS & INFRASTRUCTURE
    "systems engineer": [
        "Linux", "Windows", "System Administration", "Networking", "TCP/IP",
        "DNS", "DHCP", "Cloud Platforms", "AWS", "Azure", "Automation",
        "Bash", "Python", "Infrastructure", "Monitoring", "Troubleshooting",
        "Performance Analysis", "Capacity Planning"
    ],
    "site reliability engineer": [
        "Linux", "Kubernetes", "Docker", "Monitoring", "Logging",
        "Python", "Go", "Bash", "Incident Response", "On-call Management",
        "Reliability", "Scalability", "Performance", "Automation",
        "Infrastructure as Code", "CI/CD", "Disaster Recovery"
    ],
    
    # BUSINESS & ENTERPRISE
    "solutions architect": [
        "Solution Design", "Architecture Patterns", "Cloud Architecture",
        "AWS", "Azure", "System Design", "Microservices", "API Design",
        "Security Design", "Scalability", "Business Analysis", "Communication",
        "Requirements Gathering", "Documentation", "Project Management"
    ],
    "enterprise architect": [
        "Enterprise Architecture", "System Design", "Business Process Design",
        "Technology Strategy", "Cloud Architecture", "Integration Patterns",
        "Security Architecture", "Scalability", "Cost Optimization",
        "Change Management", "Governance", "Compliance", "Documentation"
    ],
    
    # DATA ENGINEERING
    "data engineer": [
        "Python", "Scala", "Java", "SQL", "Apache Spark", "Hadoop",
        "ETL", "Data Pipelines", "Kafka", "Airflow", "BigQuery",
        "Data Warehousing", "Data Lakes", "Snowflake", "Cloud Platforms",
        "Streaming Data", "Real-time Processing", "Data Quality"
    ],
    "analytics engineer": [
        "SQL", "dbt", "Python", "R", "Data Warehousing", "Snowflake",
        "BigQuery", "Data Modeling", "ETL", "Analytics", "Tableau",
        "Looker", "Git", "Version Control", "Testing", "Documentation"
    ],
    
    # GAME DEVELOPMENT
    "game developer": [
        "Unity", "Unreal Engine", "C#", "C++", "Game Design", "Game Physics",
        "3D Graphics", "Game Audio", "Animation", "Networking",
        "Multiplayer Development", "Performance Optimization", "Debugging",
        "Version Control", "Agile Development"
    ],
    
    # BLOCKCHAIN
    "blockchain developer": [
        "Solidity", "Ethereum", "Bitcoin", "Web3", "Smart Contracts",
        "Cryptocurrency", "DeFi", "NFTs", "JavaScript", "Python",
        "Blockchain Architecture", "Consensus Mechanisms", "Gas Optimization",
        "Testing", "Security", "Hardhat", "Truffle"
    ],
    
    # AR/VR
    "ar/vr developer": [
        "Unity", "Unreal Engine", "C#", "C++", "3D Graphics",
        "AR Kit", "ARCore", "VR Development", "3D Modeling",
        "Animation", "Spatial Computing", "Real-time Rendering",
        "Performance Optimization", "User Experience", "Mobile Development"
    ],
    
    # AUTOMATION
    "automation engineer": [
        "Python", "Bash", "Scripting", "RPA", "UiPath", "Blue Prism",
        "Process Automation", "Workflow Automation", "Testing Automation",
        "CI/CD", "Jenkins", "Configuration Management", "Infrastructure",
        "Linux", "System Administration"
    ],
    
    # SUPPORT & OPERATIONS
    "support engineer": [
        "Technical Support", "Customer Service", "Troubleshooting",
        "Linux", "Windows", "Networking", "Databases", "Problem Solving",
        "Documentation", "Git", "Python", "Bash", "API Knowledge",
        "Communication", "Patience", "Time Management"
    ],
    "devops technician": [
        "Linux", "Windows", "Docker", "Kubernetes", "Bash",
        "Scripting", "Networking", "Monitoring", "Logging",
        "CI/CD", "Jenkins", "Git", "Cloud Platforms", "Troubleshooting"
    ]
}

# ================== FIREBASE ==================
try:
    service_account_info = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
    cred = credentials.Certificate(service_account_info)
    initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized")
except Exception as e:
    print(f"⚠️ Firebase error: {e}")
    db = None

# ================== GEMINI ==================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# ================== HELPERS ==================

def normalize_role(role):
    return role.strip().lower()

def normalize_skill(skill):
    return skill.lower().replace("-", " ").strip()

def normalize_skills(skills):
    return set(normalize_skill(s) for s in skills if isinstance(s, str))

def parse_json_flexible(text):
    """
    FLEXIBLE JSON parser with multiple strategies
    """
    print(f"\n🔍 Attempting to parse JSON...")
    print(f"📄 Raw text length: {len(text)} chars")
    print(f"📄 First 300 chars: {text[:300]}")
    
    # Strategy 1: Try direct JSON parse
    try:
        result = json.loads(text)
        print(f"✅ Strategy 1 SUCCESS: Direct JSON parse")
        return result
    except:
        print(f"❌ Strategy 1 failed: Not direct JSON")
    
    # Strategy 2: Remove markdown code blocks
    try:
        cleaned = text
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0]
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0]
        
        result = json.loads(cleaned.strip())
        print(f"✅ Strategy 2 SUCCESS: Removed markdown")
        return result
    except:
        print(f"❌ Strategy 2 failed")
    
    # Strategy 3: Find JSON object with regex
    try:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            result = json.loads(json_str)
            print(f"✅ Strategy 3 SUCCESS: Regex extraction")
            return result
    except:
        print(f"❌ Strategy 3 failed")
    
    # Strategy 4: Find between first { and last }
    try:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = text[start:end+1]
            result = json.loads(json_str)
            print(f"✅ Strategy 4 SUCCESS: Bracket extraction")
            return result
    except:
        print(f"❌ Strategy 4 failed")
    
    print(f"❌ ALL PARSING STRATEGIES FAILED")
    print(f"📄 Failed text: {text[:500]}")
    return None

def call_gemini_api(prompt, retries=3):
    """Call Gemini API with retries"""
    print(f"\n🚀 Calling Gemini API...")
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
        }
    }

    for attempt in range(retries):
        try:
            print(f"📡 Attempt {attempt + 1}/{retries}")
            
            r = requests.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                json=payload,
                timeout=30
            )
            
            print(f"📊 Status: {r.status_code}")
            
            if r.status_code == 200:
                data = r.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"✅ Got response: {len(text)} chars")
                    return text
            
            elif r.status_code == 429:
                wait = (attempt + 1) * 2
                print(f"⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:100]}")
            if attempt < retries - 1:
                time.sleep(2)
    
    return None

def extract_skills_from_resume(resume_text):
    """
    ROBUST skill extraction with multiple strategies
    """
    print(f"\n{'='*80}")
    print(f"🎯 STARTING SKILL EXTRACTION")
    print(f"{'='*80}")
    print(f"📄 Resume length: {len(resume_text)} characters")
    
    # Use substantial portion of resume
    resume_sample = resume_text[:10000]
    
    # IMPROVED PROMPT - Simpler and clearer
    prompt = f"""Extract all skills from this resume. Be thorough and extract EVERYTHING you find.

RESUME:
{resume_sample}

Find and list:
- Programming languages (Python, JavaScript, Java, C++, etc.)
- Frameworks and libraries (React, Django, TensorFlow, etc.)
- Tools and platforms (Git, Docker, AWS, etc.)
- Soft skills (Leadership, Communication, etc.)
- Spoken/programming languages

Return as JSON:
{{
  "technical": ["Python", "JavaScript", "React"],
  "soft": ["Leadership", "Communication"],
  "tools": ["Git", "Docker", "AWS"],
  "languages": ["English", "Python", "Spanish"]
}}

If you find NO skills in a category, use empty array: []
Extract ONLY skills that are explicitly mentioned in the resume."""

    try:
        # Call API
        response_text = call_gemini_api(prompt)
        
        if not response_text:
            print("❌ No API response")
            # Try keyword extraction as fallback
            return extract_skills_keyword_fallback(resume_text)
        
        print(f"\n📝 API Response received")
        print(f"First 500 chars: {response_text[:500]}")
        
        # Parse with flexible parser
        result = parse_json_flexible(response_text)
        
        if not result:
            print("❌ JSON parsing failed")
            # Try keyword extraction as fallback
            return extract_skills_keyword_fallback(resume_text)
        
        # Extract and validate
        skills = {
            "technical": result.get("technical", []),
            "soft": result.get("soft", []),
            "tools": result.get("tools", []),
            "languages": result.get("languages", [])
        }
        
        # Ensure lists
        for key in skills:
            if not isinstance(skills[key], list):
                skills[key] = []
        
        total = sum(len(v) for v in skills.values())
        
        print(f"\n✅ EXTRACTION SUCCESSFUL!")
        print(f"📊 Total skills: {total}")
        print(f"   Technical: {len(skills['technical'])}")
        print(f"   Soft: {len(skills['soft'])}")
        print(f"   Tools: {len(skills['tools'])}")
        print(f"   Languages: {len(skills['languages'])}")
        
        if skills['technical']:
            print(f"💻 Technical: {', '.join(skills['technical'][:5])}...")
        if skills['tools']:
            print(f"🔧 Tools: {', '.join(skills['tools'][:5])}...")
        
        # If we got absolutely nothing, try keyword fallback
        if total == 0:
            print("⚠️ Got 0 skills, trying keyword fallback...")
            return extract_skills_keyword_fallback(resume_text)
        
        print(f"{'='*80}\n")
        return skills
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback to keyword extraction
        return extract_skills_keyword_fallback(resume_text)

def extract_skills_keyword_fallback(resume_text):
    """
    FALLBACK: Keyword-based extraction if API fails
    """
    print(f"\n🔄 FALLBACK: Keyword-based extraction")
    
    resume_lower = resume_text.lower()
    
    # Common skills to look for
    tech_keywords = [
        "python", "javascript", "java", "c++", "c#", "ruby", "php", "swift", "kotlin",
        "react", "angular", "vue", "node.js", "django", "flask", "spring", "express",
        "html", "css", "typescript", "sql", "mongodb", "postgresql", "mysql",
        "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn",
        "machine learning", "deep learning", "data analysis", "ai", "ml"
    ]
    
    tool_keywords = [
        "git", "github", "gitlab", "docker", "kubernetes", "aws", "azure", "gcp",
        "jenkins", "jira", "linux", "bash", "terraform", "ansible",
        "vs code", "visual studio", "intellij", "eclipse", "jupyter"
    ]
    
    soft_keywords = [
        "leadership", "communication", "teamwork", "problem solving",
        "critical thinking", "creativity", "time management", "collaboration",
        "presentation", "public speaking", "mentoring", "agile", "scrum"
    ]
    
    found_technical = []
    found_tools = []
    found_soft = []
    
    # Search for keywords
    for skill in tech_keywords:
        if skill in resume_lower:
            # Capitalize properly
            found_technical.append(skill.title())
    
    for tool in tool_keywords:
        if tool in resume_lower:
            found_tools.append(tool.title())
    
    for soft in soft_keywords:
        if soft in resume_lower:
            found_soft.append(soft.title())
    
    # Remove duplicates and sort
    skills = {
        "technical": sorted(list(set(found_technical))),
        "soft": sorted(list(set(found_soft))),
        "tools": sorted(list(set(found_tools))),
        "languages": ["English"]  # Default assumption
    }
    
    total = sum(len(v) for v in skills.values())
    print(f"✅ Keyword extraction found {total} skills")
    print(f"   Technical: {len(skills['technical'])}")
    print(f"   Tools: {len(skills['tools'])}")
    print(f"   Soft: {len(skills['soft'])}")
    
    return skills

def analyze_skill_gaps(current_skills, target_role):
    role_key = normalize_role(target_role)
    role_skills = ROLE_SKILL_MAP.get(role_key)

    if not role_skills:
        role_skills = generate_role_skills_from_gemini(target_role)
        if db and role_skills:
            try:
                db.collection("role_skills").document(role_key).set({
                    "original_role": target_role,
                    "skills": role_skills,
                    "source": "gemini",
                    "timestamp": firestore.SERVER_TIMESTAMP
                })
            except:
                pass

    if not role_skills:
        return []

    resume_skills = set(normalize_skill(s) for s in (
        current_skills.get("technical", []) +
        current_skills.get("tools", [])
    ) if isinstance(s, str))

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
        "readiness": "Moderate" if score < 70 else "High" if score > 80 else "Moderate",
        "timeline_months": 2 if score > 80 else 3 if score > 60 else 6,
        "difficulty": "Easy" if score > 80 else "Hard" if score < 50 else "Moderate"
    }

def generate_roadmap(skill_gaps, target_role):
    gaps = [g["skill"] for g in skill_gaps[:5]]

    if not gaps:
        return [
            {"week": "1-4", "phase": "Advanced Practice", "focus": f"Master advanced concepts for {target_role}", "tasks": ["Build advanced project", "Optimize performance"]},
            {"week": "5-8", "phase": "Project Development", "focus": "Create portfolio projects", "tasks": ["Develop capstone project", "Document code"]},
            {"week": "9-12", "phase": "Job Preparation", "focus": "Interview prep and applications", "tasks": ["Mock interviews", "Apply to positions"]}
        ]

    prompt = f"""Create a 12-week roadmap for {target_role}.
Missing: {", ".join(gaps)}
Return JSON: {{ "roadmap": [{{ "week": "1-3", "phase": "Name", "focus": "Focus", "tasks": ["Task1"] }}] }}"""
    
    text = call_gemini_api(prompt)
    if text:
        result = parse_json_flexible(text)
        if result and result.get("roadmap"):
            return result["roadmap"]
    
    return [{"week": "1-4", "phase": "Foundations", "focus": f"Learn {gaps[0]}", "tasks": ["Study", "Practice"]}]

def generate_weekly_tasks(skill_gaps, target_role):
    gap_skills = [gap["skill"] for gap in skill_gaps[:8]]

    if not gap_skills:
        return [
            {"week": i, "task": f"Week {i}: Build {target_role} project", "outcome": f"Milestone {i}"}
            for i in range(1, 13)
        ]

    prompt = f"""Create 12 weekly tasks for {target_role}.
Skills: {", ".join(gap_skills)}
Return JSON: {{ "weekly_tasks": [{{ "week": 1, "task": "Task", "outcome": "Result" }}] }}"""

    text = call_gemini_api(prompt)
    if text:
        result = parse_json_flexible(text)
        if result:
            tasks = result.get("weekly_tasks", [])
            if len(tasks) >= 8:
                return tasks
    
    return [
        {"week": i, "task": f"Week {i}: Learn {gap_skills[i % len(gap_skills)]}", "outcome": f"Master {gap_skills[i % len(gap_skills)]}"}
        for i in range(1, 13)
    ]

def identify_strengths():
    return {
        "strengths": [
            "Diverse technical foundation",
            "Hands-on project experience",
            "Strong problem-solving ability",
            "Proven learning capability"
        ],
        "advantages": [
            "Multiple technology expertise",
            "Real-world project experience",
            "Continuous learning mindset"
        ]
    }

def generate_role_skills_from_gemini(role):
    prompt = f"""List 12-15 skills for: {role}
Return JSON: {{ "skills": ["Skill1", "Skill2"] }}"""
    text = call_gemini_api(prompt)
    if text:
        result = parse_json_flexible(text)
        if result:
            return result.get("skills", [])
    return []

# ================== ROUTES ==================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "SkillBridge API running"}), 200

@app.route("/search-roles", methods=["GET"])
def search_roles():
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify({"roles": []})
    
    matching = [role.title() for role in ROLE_SKILL_MAP.keys() if query in role.lower()]
    return jsonify({"roles": sorted(matching)[:10]})

@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    resume_text = data.get("resume_text")
    target_role = data.get("target_role")
    user_id = data.get("user_id", "anonymous")

    if not resume_text:
        return jsonify({"error": "resume_text required"}), 400
    if not target_role:
        return jsonify({"error": "target_role required"}), 400

    target_role_normalized = target_role.strip()

    print(f"\n📊 Analyzing for: {target_role_normalized}")
    
    current_skills = extract_skills_from_resume(resume_text)
    skill_gaps = analyze_skill_gaps(current_skills, target_role_normalized)
    match = calculate_match_score(skill_gaps)
    roadmap = generate_roadmap(skill_gaps, target_role_normalized)
    weekly_tasks = generate_weekly_tasks(skill_gaps, target_role_normalized)
    strengths = identify_strengths()

    if db and user_id != "anonymous":
        try:
            db.collection("user_analyses").add({
                "user_id": user_id,
                "target_role": target_role_normalized,
                "current_skills": current_skills,
                "match_score": match["match_score"],
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            print(f"Firebase error: {e}")

    return jsonify({
        "targetRole": target_role_normalized,
        "currentSkills": current_skills,
        "skillGaps": skill_gaps,
        "matchScore": match["match_score"],
        "readiness": match["readiness"],
        "timelineMonths": match["timeline_months"],
        "difficulty": match["difficulty"],
        "roadmap": roadmap,
        "weeklyTasks": weekly_tasks,
        "strengths": strengths["strengths"],
        "competitiveAdvantages": strengths["advantages"]
    }), 200

@app.route("/delete-resume/<user_id>/<resume_id>", methods=["DELETE"])
def delete_resume(user_id, resume_id):
    if not db:
        return jsonify({"error": "Database unavailable"}), 500
    try:
        db.collection("user_resumes").document(resume_id).delete()
        return jsonify({"message": "Deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/", methods=["GET"])
def health_check():
    return {"status": "SkillBridge backend running"}, 200


@app.route("/get-resumes/<user_id>", methods=["GET"])
def get_resumes(user_id):
    if not db:
        return jsonify({"error": "Database unavailable"}), 500
    try:
        docs = db.collection("user_resumes").where("user_id", "==", user_id).stream()
        resumes = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            resumes.append(data)
        return jsonify({"resumes": resumes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 SkillBridge - ROBUST EXTRACTION with FALLBACK")
    print("="*80 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)





# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# import json
# import time
# import requests
# from firebase_admin import credentials, firestore, initialize_app

# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# # ================== COMPREHENSIVE ROLE SKILL MAP (50+ ROLES) ==================
# ROLE_SKILL_MAP = {
#     # WEB DEVELOPMENT
#     "frontend engineer": [
#         "JavaScript", "React", "Vue.js", "Angular", "TypeScript",
#         "HTML", "CSS", "SASS", "Tailwind CSS", "Bootstrap",
#         "Webpack", "Babel", "REST APIs", "GraphQL", "Redux",
#         "State Management", "Responsive Design", "Web Performance",
#         "Accessibility", "Jest", "Testing Library"
#     ],
#     "backend engineer": [
#         "Python", "Java", "C#", "Node.js", "Go", "Ruby",
#         "Django", "Flask", "Spring Boot", "Express.js", "Laravel",
#         "APIs", "REST", "GraphQL", "Databases", "SQL", "MongoDB",
#         "PostgreSQL", "MySQL", "Docker", "Kubernetes", "System Design",
#         "Authentication", "Authorization", "Security"
#     ],
#     "full stack developer": [
#         "JavaScript", "Python", "React", "Node.js", "Vue.js",
#         "Angular", "TypeScript", "HTML", "CSS", "SQL", "MongoDB",
#         "Django", "Flask", "Express.js", "PostgreSQL", "MySQL",
#         "Docker", "APIs", "REST", "GraphQL", "Git", "DevOps",
#         "Deployment", "AWS", "Heroku", "Firebase"
#     ],
#     "web developer": [
#         "HTML", "CSS", "JavaScript", "React", "Vue.js", "Angular",
#         "TypeScript", "Bootstrap", "Tailwind CSS", "Responsive Design",
#         "Web Accessibility", "SEO", "Performance Optimization",
#         "APIs", "REST", "Git", "Webpack", "NPM", "Package Management"
#     ],
    
#     # DATA & AI/ML
#     "machine learning engineer": [
#         "Python", "NumPy", "Pandas", "Scikit-learn", "TensorFlow",
#         "PyTorch", "Keras", "OpenCV", "NLP", "Deep Learning",
#         "Neural Networks", "Machine Learning", "Statistics", "Linear Algebra",
#         "Data Preprocessing", "Model Training", "Model Evaluation",
#         "Feature Engineering", "MLOps", "Model Deployment", "SQL"
#     ],
#     "data scientist": [
#         "Python", "R", "SQL", "Pandas", "NumPy", "Scikit-learn",
#         "TensorFlow", "PyTorch", "Matplotlib", "Seaborn", "Plotly",
#         "Data Analysis", "Data Visualization", "Statistics", "Probability",
#         "Machine Learning", "Deep Learning", "Tableau", "Power BI",
#         "Excel", "Big Data", "Apache Spark"
#     ],
#     "data analyst": [
#         "SQL", "Python", "R", "Tableau", "Power BI", "Excel",
#         "Data Visualization", "Statistics", "Data Cleaning",
#         "Data Mining", "Data Interpretation", "Pandas", "Matplotlib",
#         "Google Analytics", "Dashboard Creation", "Report Writing",
#         "Business Intelligence", "Google Sheets"
#     ],
#     "ai engineer": [
#         "Python", "TensorFlow", "PyTorch", "Transformers", "BERT",
#         "GPT", "NLP", "Computer Vision", "Deep Learning", "Machine Learning",
#         "Neural Networks", "Prompt Engineering", "LLM Fine-tuning",
#         "Model Deployment", "CUDA", "Hugging Face", "Langchain"
#     ],
    
#     # SECURITY
#     "cybersecurity analyst": [
#         "Network Security", "Firewalls", "VPN", "Encryption", "SSL/TLS",
#         "Python", "Bash", "Linux", "Windows Security", "Penetration Testing",
#         "SIEM", "IDS/IPS", "Malware Analysis", "Threat Detection",
#         "Security Auditing", "Vulnerability Assessment", "Risk Management",
#         "Compliance", "OWASP", "Ethical Hacking"
#     ],
#     "security engineer": [
#         "Python", "Java", "C++", "Linux", "Windows", "Network Security",
#         "Cryptography", "Encryption", "TLS/SSL", "OAuth", "JWT",
#         "Secure Coding", "Application Security", "API Security",
#         "Cloud Security", "AWS Security", "Azure Security", "Infrastructure",
#         "Security Architecture", "Zero Trust"
#     ],
#     "penetration tester": [
#         "Python", "Bash", "Linux", "Networking", "Web Security",
#         "Kali Linux", "Metasploit", "Burp Suite", "Wireshark",
#         "Network Scanning", "Vulnerability Exploitation", "Social Engineering",
#         "Report Writing", "Security Assessment", "Firewall Bypass",
#         "SQL Injection", "XSS", "OWASP Top 10"
#     ],
    
#     # CLOUD & DEVOPS
#     "devops engineer": [
#         "Docker", "Kubernetes", "AWS", "Azure", "GCP", "CI/CD",
#         "Jenkins", "GitLab CI", "GitHub Actions", "Linux", "Bash",
#         "Python", "Terraform", "Ansible", "CloudFormation", "Infrastructure as Code",
#         "Monitoring", "Logging", "ELK Stack", "Prometheus", "Grafana"
#     ],
#     "cloud architect": [
#         "AWS", "Azure", "Google Cloud", "Cloud Design", "Cloud Architecture",
#         "Microservices", "Containers", "Kubernetes", "Docker", "Serverless",
#         "Cloud Security", "Scalability", "High Availability", "Disaster Recovery",
#         "Cost Optimization", "Infrastructure Design", "Load Balancing"
#     ],
#     "aws engineer": [
#         "AWS", "EC2", "S3", "Lambda", "RDS", "DynamoDB", "API Gateway",
#         "CloudFront", "Route 53", "IAM", "VPC", "CloudFormation",
#         "SAM", "Python", "Node.js", "Terraform", "Infrastructure as Code",
#         "Security", "Monitoring", "CloudWatch"
#     ],
    
#     # EMBEDDED & IOT
#     "iot engineer": [
#         "C", "C++", "Python", "Arduino", "ESP32", "Raspberry Pi",
#         "Embedded Systems", "IoT", "RFID", "Bluetooth", "WiFi",
#         "Microcontrollers", "Sensors", "Hardware Programming", "Firmware",
#         "Real-time Systems", "Low-power Design", "Communication Protocols"
#     ],
#     "embedded systems engineer": [
#         "C", "C++", "Assembly", "Real-time OS", "FreeRTOS", "Linux",
#         "Microcontrollers", "ARM", "Embedded Linux", "Device Drivers",
#         "Hardware Debugging", "JTAG", "GDB", "Build Systems", "Make",
#         "Version Control", "Testing", "System Architecture"
#     ],
    
#     # MOBILE
#     "ios developer": [
#         "Swift", "Objective-C", "iOS", "Xcode", "UIKit", "SwiftUI",
#         "Core Data", "Network Requests", "REST APIs", "JSON",
#         "Git", "Cocoapods", "SPM", "Testing", "XCTest",
#         "App Store Deployment", "iOS Guidelines", "Performance Optimization"
#     ],
#     "android developer": [
#         "Java", "Kotlin", "Android Studio", "Android SDK", "XML",
#         "Activities", "Fragments", "Services", "Content Providers",
#         "Room Database", "SQLite", "REST APIs", "Retrofit", "Volley",
#         "Firebase", "Push Notifications", "Google Play", "Material Design"
#     ],
#     "mobile app developer": [
#         "React Native", "Flutter", "Dart", "JavaScript", "TypeScript",
#         "Cross-platform Development", "iOS", "Android", "Firebase",
#         "REST APIs", "GraphQL", "State Management", "Redux",
#         "Navigation", "Testing", "App Store Deployment", "Google Play"
#     ],
    
#     # DATABASE
#     "database administrator": [
#         "SQL", "MySQL", "PostgreSQL", "Oracle", "MSSQL", "MongoDB",
#         "Database Design", "Backup & Recovery", "Performance Tuning",
#         "Indexing", "Query Optimization", "Replication", "High Availability",
#         "Security", "Access Control", "Monitoring", "Troubleshooting"
#     ],
#     "database engineer": [
#         "SQL", "NoSQL", "MongoDB", "Cassandra", "Redis", "Elasticsearch",
#         "Database Design", "Schema Design", "Query Optimization", "Indexing",
#         "Replication", "Clustering", "Sharding", "Data Warehousing",
#         "ETL", "Performance Tuning", "Python", "Java"
#     ],
    
#     # QA & TESTING
#     "qa engineer": [
#         "Test Planning", "Test Case Design", "Manual Testing", "Automation Testing",
#         "Selenium", "Cypress", "Appium", "JUnit", "TestNG", "Mocha",
#         "Python", "Java", "JavaScript", "Bug Tracking", "JIRA",
#         "Regression Testing", "Performance Testing", "Security Testing"
#     ],
#     "test automation engineer": [
#         "Selenium", "Cypress", "Appium", "Python", "Java", "JavaScript",
#         "Page Object Model", "Testing Frameworks", "Continuous Integration",
#         "Jenkins", "GitHub Actions", "Performance Testing", "Load Testing",
#         "JMeter", "Postman", "API Testing", "Test Data Management"
#     ],
    
#     # DEVREL & PRODUCT
#     "developer advocate": [
#         "Technical Writing", "Speaking", "Community Building", "Content Creation",
#         "JavaScript", "Python", "APIs", "SDKs", "Documentation",
#         "Blogging", "Video Creation", "Social Media", "Event Hosting",
#         "Networking", "Public Relations", "Product Knowledge"
#     ],
#     "product manager": [
#         "Product Strategy", "User Research", "Market Analysis", "Roadmapping",
#         "Analytics", "Metrics", "A/B Testing", "User Experience",
#         "Agile", "Scrum", "Communication", "Leadership", "Data Analysis",
#         "SQL", "Tableau", "Competitive Analysis"
#     ],
#     "technical writer": [
#         "Technical Writing", "Documentation", "API Documentation", "Markdown",
#         "Git", "Sphinx", "MkDocs", "Asciidoc", "LaTeX", "Adobe Suite",
#         "SEO", "UX Writing", "Content Strategy", "User Testing",
#         "English", "Grammar", "Information Architecture"
#     ],
    
#     # AI/PROMPT ENGINEERING
#     "prompt engineer": [
#         "Prompt Engineering", "LLM", "ChatGPT", "GPT-4", "Claude",
#         "BERT", "Transformers", "NLP", "Python", "Machine Learning",
#         "Prompt Optimization", "Fine-tuning", "Model Evaluation",
#         "Langchain", "Semantic Search", "Retrieval Augmented Generation",
#         "Natural Language Processing"
#     ],
#     "llm engineer": [
#         "Large Language Models", "Transformers", "PyTorch", "TensorFlow",
#         "Hugging Face", "Fine-tuning", "Model Training", "CUDA",
#         "Prompt Engineering", "Few-shot Learning", "In-context Learning",
#         "Model Deployment", "API Development", "Python", "GPU Optimization"
#     ],
    
#     # SYSTEMS & INFRASTRUCTURE
#     "systems engineer": [
#         "Linux", "Windows", "System Administration", "Networking", "TCP/IP",
#         "DNS", "DHCP", "Cloud Platforms", "AWS", "Azure", "Automation",
#         "Bash", "Python", "Infrastructure", "Monitoring", "Troubleshooting",
#         "Performance Analysis", "Capacity Planning"
#     ],
#     "site reliability engineer": [
#         "Linux", "Kubernetes", "Docker", "Monitoring", "Logging",
#         "Python", "Go", "Bash", "Incident Response", "On-call Management",
#         "Reliability", "Scalability", "Performance", "Automation",
#         "Infrastructure as Code", "CI/CD", "Disaster Recovery"
#     ],
    
#     # BUSINESS & ENTERPRISE
#     "solutions architect": [
#         "Solution Design", "Architecture Patterns", "Cloud Architecture",
#         "AWS", "Azure", "System Design", "Microservices", "API Design",
#         "Security Design", "Scalability", "Business Analysis", "Communication",
#         "Requirements Gathering", "Documentation", "Project Management"
#     ],
#     "enterprise architect": [
#         "Enterprise Architecture", "System Design", "Business Process Design",
#         "Technology Strategy", "Cloud Architecture", "Integration Patterns",
#         "Security Architecture", "Scalability", "Cost Optimization",
#         "Change Management", "Governance", "Compliance", "Documentation"
#     ],
    
#     # DATA ENGINEERING
#     "data engineer": [
#         "Python", "Scala", "Java", "SQL", "Apache Spark", "Hadoop",
#         "ETL", "Data Pipelines", "Kafka", "Airflow", "BigQuery",
#         "Data Warehousing", "Data Lakes", "Snowflake", "Cloud Platforms",
#         "Streaming Data", "Real-time Processing", "Data Quality"
#     ],
#     "analytics engineer": [
#         "SQL", "dbt", "Python", "R", "Data Warehousing", "Snowflake",
#         "BigQuery", "Data Modeling", "ETL", "Analytics", "Tableau",
#         "Looker", "Git", "Version Control", "Testing", "Documentation"
#     ],
    
#     # GAME DEVELOPMENT
#     "game developer": [
#         "Unity", "Unreal Engine", "C#", "C++", "Game Design", "Game Physics",
#         "3D Graphics", "Game Audio", "Animation", "Networking",
#         "Multiplayer Development", "Performance Optimization", "Debugging",
#         "Version Control", "Agile Development"
#     ],
    
#     # BLOCKCHAIN
#     "blockchain developer": [
#         "Solidity", "Ethereum", "Bitcoin", "Web3", "Smart Contracts",
#         "Cryptocurrency", "DeFi", "NFTs", "JavaScript", "Python",
#         "Blockchain Architecture", "Consensus Mechanisms", "Gas Optimization",
#         "Testing", "Security", "Hardhat", "Truffle"
#     ],
    
#     # AR/VR
#     "ar/vr developer": [
#         "Unity", "Unreal Engine", "C#", "C++", "3D Graphics",
#         "AR Kit", "ARCore", "VR Development", "3D Modeling",
#         "Animation", "Spatial Computing", "Real-time Rendering",
#         "Performance Optimization", "User Experience", "Mobile Development"
#     ],
    
#     # AUTOMATION
#     "automation engineer": [
#         "Python", "Bash", "Scripting", "RPA", "UiPath", "Blue Prism",
#         "Process Automation", "Workflow Automation", "Testing Automation",
#         "CI/CD", "Jenkins", "Configuration Management", "Infrastructure",
#         "Linux", "System Administration"
#     ],
    
#     # SUPPORT & OPERATIONS
#     "support engineer": [
#         "Technical Support", "Customer Service", "Troubleshooting",
#         "Linux", "Windows", "Networking", "Databases", "Problem Solving",
#         "Documentation", "Git", "Python", "Bash", "API Knowledge",
#         "Communication", "Patience", "Time Management"
#     ],
#     "devops technician": [
#         "Linux", "Windows", "Docker", "Kubernetes", "Bash",
#         "Scripting", "Networking", "Monitoring", "Logging",
#         "CI/CD", "Jenkins", "Git", "Cloud Platforms", "Troubleshooting"
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

# # ================== GEMINI ==================
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# # ================== IMPROVED HELPERS ==================

# def normalize_role(role):
#     """Normalize role name for case-insensitive matching"""
#     return role.strip().lower()

# def normalize_skill(skill):
#     return skill.lower().replace("-", " ").strip()

# def normalize_skills(skills):
#     return set(normalize_skill(s) for s in skills if isinstance(s, str))

# def parse_json_response(text):
#     """
#     IMPROVED JSON parser with better error handling and logging
#     """
#     print(f"\n🔍 Parsing JSON response...")
#     print(f"📄 Raw response (first 500 chars): {text[:500]}")
    
#     try:
#         # Remove markdown code blocks
#         if "```json" in text:
#             text = text.split("```json")[1].split("```")[0]
#             print("✂️ Removed ```json markers")
#         elif "```" in text:
#             text = text.split("```")[1].split("```")[0]
#             print("✂️ Removed ``` markers")
        
#         # Find JSON object
#         start = text.find("{")
#         end = text.rfind("}")
        
#         if start == -1 or end == -1:
#             print("❌ No JSON object found in response")
#             return None
            
#         text = text[start:end+1]
#         print(f"✂️ Extracted JSON: {text[:200]}...")
        
#         result = json.loads(text)
#         print(f"✅ Successfully parsed JSON with keys: {result.keys()}")
#         return result
        
#     except json.JSONDecodeError as e:
#         print(f"❌ JSON Decode Error: {e}")
#         print(f"📄 Failed text: {text[:500]}")
#         return None
#     except Exception as e:
#         print(f"❌ Unexpected error parsing JSON: {e}")
#         return None

# def call_gemini_api(prompt, retries=3):
#     """
#     IMPROVED Gemini API caller with better error handling
#     """
#     print(f"\n🚀 Calling Gemini API...")
    
#     payload = {
#         "contents": [{"parts": [{"text": prompt}]}],
#         "generationConfig": {
#             "temperature": 0.3,
#             "maxOutputTokens": 2048  # Increased for longer responses
#         }
#     }

#     for attempt in range(retries):
#         try:
#             print(f"📡 Attempt {attempt + 1}/{retries}")
            
#             r = requests.post(
#                 f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
#                 json=payload,
#                 timeout=30
#             )
            
#             print(f"📊 Response status: {r.status_code}")
            
#             if r.status_code == 200:
#                 response_data = r.json()
                
#                 if "candidates" not in response_data:
#                     print("❌ No candidates in response")
#                     continue
                    
#                 if len(response_data["candidates"]) == 0:
#                     print("❌ Empty candidates array")
#                     continue
                
#                 response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
#                 print(f"✅ Got response ({len(response_text)} chars)")
#                 return response_text
                
#             elif r.status_code == 429:
#                 wait_time = (attempt + 1) * 2
#                 print(f"⏳ Rate limited, waiting {wait_time}s...")
#                 time.sleep(wait_time)
#                 continue
#             else:
#                 print(f"❌ API Error {r.status_code}: {r.text[:200]}")
                
#         except requests.exceptions.Timeout:
#             print(f"⏱️ Request timeout on attempt {attempt + 1}")
#             if attempt < retries - 1:
#                 time.sleep(2)
#                 continue
#         except Exception as e:
#             print(f"❌ Exception: {str(e)[:200]}")
#             if attempt < retries - 1:
#                 time.sleep(1)
#                 continue
    
#     print("❌ All API attempts failed")
#     return None

# # ================== FIXED SKILL EXTRACTION ==================

# def extract_skills_from_resume(resume_text):
#     """
#     COMPLETELY FIXED skill extraction with proper error handling
#     NO MORE DEFAULT FALLBACKS TO PYTHON
#     """
    
#     print(f"\n{'='*80}")
#     print(f"🎯 SKILL EXTRACTION STARTING")
#     print(f"{'='*80}")
#     print(f"📄 Resume length: {len(resume_text)} characters")
#     print(f"📄 First 300 chars: {resume_text[:300]}...")
    
#     # Use MORE of the resume (not just 2000 chars)
#     resume_sample = resume_text[:8000]  # Increased from 2000 to 8000
    
#     prompt = f"""You are an expert resume analyzer. Extract ALL skills from this resume.

# RESUME TEXT:
# {resume_sample}

# INSTRUCTIONS:
# 1. Read the ENTIRE resume carefully
# 2. Extract EVERY skill mentioned - programming languages, frameworks, tools, soft skills, spoken languages
# 3. Do NOT make up skills that aren't in the resume
# 4. Do NOT add generic skills like "Python" unless explicitly mentioned
# 5. Look in ALL sections: summary, experience, projects, education, skills, certifications
# 6. Include variations (e.g., if "JS" is mentioned, include "JavaScript")

# Return ONLY this exact JSON format with NO additional text:
# {{
#   "technical": ["skill1", "skill2"],
#   "soft": ["skill1", "skill2"],
#   "tools": ["tool1", "tool2"],
#   "languages": ["language1", "language2"]
# }}

# CRITICAL: If a category has NO skills, use an empty array []. Do NOT invent skills."""

#     try:
#         # Call API
#         response_text = call_gemini_api(prompt)
        
#         if not response_text:
#             print("❌ No response from API")
#             return {
#                 "technical": [],
#                 "soft": [],
#                 "tools": [],
#                 "languages": []
#             }
        
#         # Parse JSON
#         result = parse_json_response(response_text)
        
#         if not result:
#             print("❌ Failed to parse JSON response")
#             return {
#                 "technical": [],
#                 "soft": [],
#                 "tools": [],
#                 "languages": []
#             }
        
#         # Validate result
#         extracted_skills = {
#             "technical": result.get("technical", []),
#             "soft": result.get("soft", []),
#             "tools": result.get("tools", []),
#             "languages": result.get("languages", [])
#         }
        
#         # Count total skills
#         total_skills = sum(len(v) for v in extracted_skills.values())
#         print(f"\n✅ EXTRACTION SUCCESSFUL")
#         print(f"📊 Total skills extracted: {total_skills}")
#         print(f"   - Technical: {len(extracted_skills['technical'])}")
#         print(f"   - Soft: {len(extracted_skills['soft'])}")
#         print(f"   - Tools: {len(extracted_skills['tools'])}")
#         print(f"   - Languages: {len(extracted_skills['languages'])}")
        
#         # Log actual skills
#         if extracted_skills['technical']:
#             print(f"💻 Technical skills: {', '.join(extracted_skills['technical'][:10])}...")
#         if extracted_skills['tools']:
#             print(f"🔧 Tools: {', '.join(extracted_skills['tools'][:10])}...")
        
#         print(f"{'='*80}\n")
        
#         return extracted_skills
        
#     except Exception as e:
#         print(f"❌ CRITICAL ERROR in skill extraction: {e}")
#         import traceback
#         traceback.print_exc()
        
#         # Return empty instead of defaults
#         return {
#             "technical": [],
#             "soft": [],
#             "tools": [],
#             "languages": []
#         }

# # ================== SKILL GAP ANALYSIS ==================

# def analyze_skill_gaps(current_skills, target_role):
#     role_key = normalize_role(target_role)
#     role_skills = ROLE_SKILL_MAP.get(role_key)

#     if not role_skills:
#         role_skills = generate_role_skills_from_gemini(target_role)
#         if db and role_skills:
#             try:
#                 db.collection("role_skills").document(role_key).set({
#                     "original_role": target_role,
#                     "skills": role_skills,
#                     "source": "gemini",
#                     "timestamp": firestore.SERVER_TIMESTAMP
#                 })
#             except:
#                 pass

#     if not role_skills:
#         return []

#     resume_skills = set(normalize_skill(s) for s in (
#         current_skills.get("technical", []) +
#         current_skills.get("tools", [])
#     ) if isinstance(s, str))

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

# def calculate_match_score(skill_gaps):
#     score = max(30, 100 - len(skill_gaps) * 5)
#     return {
#         "match_score": score,
#         "readiness": "Moderate" if score < 70 else "High" if score > 80 else "Moderate",
#         "timeline_months": 2 if score > 80 else 3 if score > 60 else 6,
#         "difficulty": "Easy" if score > 80 else "Hard" if score < 50 else "Moderate"
#     }

# # ================== ROADMAP & TASKS ==================

# def generate_roadmap(skill_gaps, target_role):
#     gaps = [g["skill"] for g in skill_gaps[:5]]

#     if not gaps:
#         return [
#             {"week": "1-4", "phase": "Advanced Practice", "focus": f"Master advanced concepts for {target_role}", "tasks": ["Build advanced project", "Optimize performance"]},
#             {"week": "5-8", "phase": "Project Development", "focus": "Create portfolio projects", "tasks": ["Develop capstone project", "Document code"]},
#             {"week": "9-12", "phase": "Job Preparation", "focus": "Interview prep and applications", "tasks": ["Mock interviews", "Apply to positions"]}
#         ]

#     prompt = f"""Create a detailed 12-week learning roadmap for {target_role}.
# Missing skills: {", ".join(gaps)}

# Return ONLY JSON:
# {{ "roadmap": [{{ "week": "1-3", "phase": "Name", "focus": "Focus", "tasks": ["Task1", "Task2"] }}] }}"""
    
#     text = call_gemini_api(prompt)
#     if text:
#         result = parse_json_response(text)
#         if result and result.get("roadmap"):
#             return result["roadmap"]
    
#     return [{"week": "1-4", "phase": "Foundations", "focus": f"Learn {gaps[0] if gaps else 'skills'}", "tasks": ["Study", "Practice"]}]

# def generate_weekly_tasks(skill_gaps, target_role):
#     """Generate 12 detailed weekly tasks"""
#     gap_skills = [gap["skill"] for gap in skill_gaps[:8]]

#     if not gap_skills:
#         return [
#             {"week": i, "task": f"Week {i}: Build {target_role} project component", "outcome": f"Complete milestone {i}"}
#             for i in range(1, 13)
#         ]

#     prompt = f"""Create 12 specific weekly tasks for {target_role}.
# Skills: {", ".join(gap_skills)}

# Return ONLY JSON:
# {{ "weekly_tasks": [{{ "week": 1, "task": "Specific task", "outcome": "Result" }}, ...] }}"""

#     text = call_gemini_api(prompt)
#     if text:
#         result = parse_json_response(text)
#         tasks = result.get("weekly_tasks", []) if result else []
#         if len(tasks) >= 8:
#             return tasks
    
#     # Fallback
#     return [
#         {"week": i, "task": f"Week {i}: Learn and practice {gap_skills[i % len(gap_skills)]}", "outcome": f"Gain proficiency in {gap_skills[i % len(gap_skills)]}"}
#         for i in range(1, 13)
#     ]

# def identify_strengths():
#     return {
#         "strengths": [
#             "Diverse technical foundation",
#             "Hands-on project experience",
#             "Strong problem-solving ability",
#             "Proven learning capability"
#         ],
#         "advantages": [
#             "Multiple technology expertise",
#             "Real-world project experience",
#             "Continuous learning mindset"
#         ]
#     }

# def generate_role_skills_from_gemini(role):
#     prompt = f"""List 12-15 core skills for: {role}
# Return ONLY: {{ "skills": ["Skill1", "Skill2", ...] }}"""
#     text = call_gemini_api(prompt)
#     if text:
#         result = parse_json_response(text)
#         if result:
#             return result.get("skills", [])
#     return []

# # ================== ROUTES ==================

# @app.route("/health", methods=["GET"])
# def health():
#     return jsonify({"status": "SkillBridge API running"}), 200

# @app.route("/search-roles", methods=["GET"])
# def search_roles():
#     """Autocomplete endpoint for target role search"""
#     query = request.args.get("q", "").lower().strip()
    
#     if not query or len(query) < 1:
#         return jsonify({"roles": []})
    
#     matching_roles = [
#         role.title() 
#         for role in ROLE_SKILL_MAP.keys() 
#         if query in role.lower()
#     ]
    
#     return jsonify({"roles": sorted(matching_roles)[:10]})

# @app.route("/get-all-roles", methods=["GET"])
# def get_all_roles():
#     """Get all available roles"""
#     roles = [role.title() for role in ROLE_SKILL_MAP.keys()]
#     return jsonify({"roles": sorted(roles)})

# @app.route("/analyze-resume", methods=["POST"])
# def analyze_resume():
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400

#     data = request.get_json(silent=True)
#     if not data:
#         return jsonify({"error": "Invalid JSON body"}), 400

#     resume_text = data.get("resume_text")
#     target_role = data.get("target_role")
#     user_id = data.get("user_id", "anonymous")

#     if not resume_text:
#         return jsonify({"error": "resume_text is required"}), 400
#     if not target_role:
#         return jsonify({"error": "target_role is required"}), 400

#     target_role_normalized = target_role.strip()

#     print(f"\n📊 Analyzing resume for: {target_role_normalized}")
#     print(f"👤 User ID: {user_id}")
    
#     # Extract skills with improved function
#     current_skills = extract_skills_from_resume(resume_text)
#     total_skills = sum(len(v) for v in current_skills.values())
    
#     print(f"\n✅ Skills extraction complete: {total_skills} total skills")
    
#     skill_gaps = analyze_skill_gaps(current_skills, target_role_normalized)
#     match = calculate_match_score(skill_gaps)
#     roadmap = generate_roadmap(skill_gaps, target_role_normalized)
#     weekly_tasks = generate_weekly_tasks(skill_gaps, target_role_normalized)
#     strengths = identify_strengths()

#     if db and user_id != "anonymous":
#         try:
#             db.collection("user_analyses").add({
#                 "user_id": user_id,
#                 "target_role": target_role_normalized,
#                 "current_skills": current_skills,
#                 "match_score": match["match_score"],
#                 "timestamp": firestore.SERVER_TIMESTAMP
#             })
#         except Exception as e:
#             print(f"Firebase error: {e}")

#     return jsonify({
#         "targetRole": target_role_normalized,
#         "currentSkills": current_skills,
#         "skillGaps": skill_gaps,
#         "matchScore": match["match_score"],
#         "readiness": match["readiness"],
#         "timelineMonths": match["timeline_months"],
#         "difficulty": match["difficulty"],
#         "roadmap": roadmap,
#         "weeklyTasks": weekly_tasks,
#         "strengths": strengths["strengths"],
#         "competitiveAdvantages": strengths["advantages"]
#     }), 200

# @app.route("/delete-resume/<user_id>/<resume_id>", methods=["DELETE"])
# def delete_resume(user_id, resume_id):
#     if not db:
#         return jsonify({"error": "Database not available"}), 500
#     try:
#         db.collection("user_resumes").document(resume_id).delete()
#         return jsonify({"message": "Resume deleted successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/get-resumes/<user_id>", methods=["GET"])
# def get_resumes(user_id):
#     if not db:
#         return jsonify({"error": "Database not available"}), 500
#     try:
#         docs = db.collection("user_resumes").where("user_id", "==", user_id).stream()
#         resumes = []
#         for doc in docs:
#             data = doc.to_dict()
#             data["id"] = doc.id
#             resumes.append(data)
#         return jsonify({"resumes": resumes}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     print("\n" + "="*80)
#     print("🚀 SkillBridge Backend - FIXED SKILL EXTRACTION")
#     print("="*80 + "\n")
#     app.run(debug=True, host="0.0.0.0", port=5000)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# import json
# import time
# import requests
# from firebase_admin import credentials, firestore, initialize_app

# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# ROLE_SKILL_MAP = {
#     "machine learning engineer": [
#         "Python", "NumPy", "Pandas", "Scikit-learn",
#         "Machine Learning", "Deep Learning",
#         "TensorFlow", "PyTorch",
#         "Statistics", "Linear Algebra",
#         "Model Deployment", "MLOps"
#     ],
#     "data scientist": [
#         "Python", "Pandas", "NumPy",
#         "Data Analysis", "Statistics",
#         "Machine Learning", "SQL",
#         "Data Visualization", "Power BI"
#     ],
#     "backend engineer": [
#         "Python", "Java", "Node.js",
#         "APIs", "Databases",
#         "SQL", "System Design",
#         "Docker", "Cloud"
#     ],
#     "frontend engineer": [
#         "JavaScript", "React", "Vue.js", "Angular",
#         "HTML", "CSS", "TypeScript",
#         "Web Design", "UI/UX", "REST APIs"
#     ],
#     "full stack developer": [
#         "JavaScript", "Python", "React", "Node.js",
#         "Databases", "HTML", "CSS",
#         "APIs", "System Design", "DevOps"
#     ]
# }

# try:
#     cred = credentials.Certificate("serviceAccountKey.json")
#     initialize_app(cred)
#     db = firestore.client()
#     print("✅ Firebase initialized")
# except Exception as e:
#     print(f"⚠️ Firebase error: {e}")
#     db = None

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# def normalize_role(role):
#     return role.strip().lower()

# def normalize_skill(skill):
#     return skill.lower().replace("-", " ").strip()

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
#         "generationConfig": {
#             "temperature": 0.3,
#             "maxOutputTokens": 2048
#         }
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

# def extract_skills_from_resume(resume_text):
#     """
#     Improved skill extraction that gets ALL skills from resume
#     """
#     prompt = f"""You are a professional skill extractor. Analyze this resume and extract ALL skills mentioned.

# RESUME TEXT:
# {resume_text[:3000]}

# IMPORTANT: Extract EVERY skill mentioned, including:
# - All programming languages (Python, JavaScript, Java, C++, etc.)
# - All frameworks & libraries (React, Django, TensorFlow, etc.)
# - All tools & platforms (Git, Docker, AWS, etc.)
# - All soft skills (Communication, Leadership, Problem Solving, etc.)
# - All languages spoken

# Be thorough and don't miss any skills. Include even minor mentions.

# Return ONLY valid JSON in this exact format:
# {{
#   "technical": ["Python", "JavaScript", "React", "Django", "SQL", "AWS", "Docker", "Machine Learning", "System Design"],
#   "soft": ["Leadership", "Communication", "Problem Solving", "Team Collaboration", "Mentoring"],
#   "tools": ["Git", "GitHub", "Docker", "Kubernetes", "Jenkins", "VS Code", "Jira", "Linux"],
#   "languages": ["English", "Spanish", "Python", "JavaScript", "Java"]
# }}

# CRITICAL: Return ONLY the JSON object. No markdown, no explanations, no extra text."""

#     try:
#         text = call_gemini_api(prompt)
#         result = parse_json_response(text)
        
#         # Ensure all categories exist
#         if result and any([result.get(k) for k in ["technical", "soft", "tools", "languages"]]):
#             return {
#                 "technical": result.get("technical", []),
#                 "soft": result.get("soft", []),
#                 "tools": result.get("tools", []),
#                 "languages": result.get("languages", [])
#             }
        
#         # Fallback if extraction failed
#         return {
#             "technical": ["Python", "JavaScript"],
#             "soft": ["Communication"],
#             "tools": ["Git"],
#             "languages": ["English"]
#         }
#     except Exception as e:
#         print(f"Error extracting skills: {e}")
#         return {
#             "technical": ["Python"],
#             "soft": ["Communication"],
#             "tools": ["Git"],
#             "languages": ["English"]
#         }

# def analyze_skill_gaps(current_skills, target_role):
#     role_key = normalize_role(target_role)
#     role_skills = ROLE_SKILL_MAP.get(role_key)

#     if not role_skills:
#         role_skills = generate_role_skills_from_gemini(target_role)
#         if db and role_skills:
#             db.collection("role_skills").document(role_key).set({
#                 "original_role": target_role,
#                 "skills": role_skills,
#                 "source": "gemini",
#                 "timestamp": firestore.SERVER_TIMESTAMP
#             })

#     if not role_skills:
#         return []

#     resume_skills = set(normalize_skill(s) for s in (
#         current_skills.get("technical", []) +
#         current_skills.get("tools", [])
#     ) if isinstance(s, str))

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

# def calculate_match_score(skill_gaps):
#     score = max(30, 100 - len(skill_gaps) * 5)
#     return {
#         "match_score": score,
#         "readiness": "Moderate" if score < 70 else "High" if score > 80 else "Moderate",
#         "timeline_months": 2 if score > 80 else 3 if score > 60 else 6,
#         "difficulty": "Easy" if score > 80 else "Hard" if score < 50 else "Moderate"
#     }

# def generate_roadmap(skill_gaps, target_role):
#     gaps = [g["skill"] for g in skill_gaps[:5]]

#     if not gaps:
#         return [
#             {
#                 "week": "1-4",
#                 "phase": "Advanced Practice",
#                 "focus": f"Master advanced concepts for {target_role}",
#                 "tasks": ["Build advanced project", "Optimize performance"]
#             },
#             {
#                 "week": "5-8",
#                 "phase": "Project Development",
#                 "focus": "Create portfolio projects",
#                 "tasks": ["Develop capstone project", "Document code"]
#             },
#             {
#                 "week": "9-12",
#                 "phase": "Job Preparation",
#                 "focus": "Interview prep and applications",
#                 "tasks": ["Mock interviews", "Apply to positions"]
#             }
#         ]

#     prompt = f"""Create a detailed 12-week learning roadmap for {target_role}.
# Missing skills: {", ".join(gaps)}

# Divide into 3-4 phases, each with specific focus and actionable tasks.

# Return ONLY JSON:
# {{ "roadmap": [{{ "week": "1-3", "phase": "Foundations", "focus": "Learn X", "tasks": ["Task1", "Task2"] }}] }}"""
    
#     text = call_gemini_api(prompt)
#     result = parse_json_response(text)

#     if result.get("roadmap"):
#         return result["roadmap"]

#     return [
#         {
#             "week": "1-4",
#             "phase": "Foundations",
#             "focus": f"Learn {gaps[0] if gaps else 'core skills'}",
#             "tasks": ["Study fundamentals", "Build small projects"]
#         }
#     ]

# def generate_weekly_tasks(skill_gaps, target_role):
#     gap_skills = [gap["skill"] for gap in skill_gaps[:5]]

#     if not gap_skills:
#         return [
#             {"week": 1, "task": f"Build an advanced {target_role} project", "outcome": "Strengthen skills"},
#             {"week": 2, "task": "Optimize and refactor code", "outcome": "Better code quality"}
#         ]

#     prompt = f"""Create 6 weekly actionable tasks for {target_role}.
# Skills to improve: {", ".join(gap_skills)}

# Return ONLY JSON:
# {{ "weekly_tasks": [{{ "week": 1, "task": "...", "outcome": "..." }}] }}"""

#     text = call_gemini_api(prompt)
#     result = parse_json_response(text)

#     if result.get("weekly_tasks"):
#         return result["weekly_tasks"]

#     return [
#         {"week": 1, "task": f"Study {gap_skills[0]}", "outcome": f"Learn {gap_skills[0]}"}
#     ]

# def identify_strengths():
#     return {
#         "strengths": [
#             "Strong technical foundation",
#             "Fast learner",
#             "Good problem-solving skills",
#             "Hands-on experience with real projects"
#         ],
#         "advantages": ["Resume-driven analysis", "Personalized roadmap"]
#     }

# def generate_role_skills_from_gemini(role):
#     prompt = f"""List 10-12 core skills for: {role}
# Return ONLY: {{ "skills": ["Skill1", "Skill2"] }}"""
#     text = call_gemini_api(prompt)
#     result = parse_json_response(text)
#     return result.get("skills", [])

# @app.route("/health", methods=["GET"])
# def health():
#     return jsonify({"status": "SkillBridge API running"}), 200

# @app.route("/analyze-resume", methods=["POST"])
# def analyze_resume():
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400

#     data = request.get_json(silent=True)
#     if not data:
#         return jsonify({"error": "Invalid JSON body"}), 400

#     resume_text = data.get("resume_text")
#     target_role = data.get("target_role")
#     user_id = data.get("user_id", "anonymous")

#     if not resume_text:
#         return jsonify({"error": "resume_text is required"}), 400
#     if not target_role:
#         return jsonify({"error": "target_role is required"}), 400

#     target_role_normalized = target_role.strip()

#     current_skills = extract_skills_from_resume(resume_text)
#     skill_gaps = analyze_skill_gaps(current_skills, target_role_normalized)
#     match = calculate_match_score(skill_gaps)
#     roadmap = generate_roadmap(skill_gaps, target_role_normalized)
#     weekly_tasks = generate_weekly_tasks(skill_gaps, target_role_normalized)
#     strengths = identify_strengths()

#     if db and user_id != "anonymous":
#         try:
#             db.collection("user_analyses").add({
#                 "user_id": user_id,
#                 "target_role": target_role_normalized,
#                 "current_skills": current_skills,
#                 "match_score": match["match_score"],
#                 "timestamp": firestore.SERVER_TIMESTAMP
#             })
#         except Exception as e:
#             print(f"Firebase error: {e}")

#     return jsonify({
#         "targetRole": target_role_normalized,
#         "currentSkills": current_skills,
#         "skillGaps": skill_gaps,
#         "matchScore": match["match_score"],
#         "readiness": match["readiness"],
#         "timelineMonths": match["timeline_months"],
#         "difficulty": match["difficulty"],
#         "roadmap": roadmap,
#         "weeklyTasks": weekly_tasks,
#         "strengths": strengths["strengths"],
#         "competitiveAdvantages": strengths["advantages"]
#     }), 200

# @app.route("/delete-resume/<user_id>/<resume_id>", methods=["DELETE"])
# def delete_resume(user_id, resume_id):
#     """Delete a resume from Firestore"""
#     if not db:
#         return jsonify({"error": "Database not available"}), 500

#     try:
#         db.collection("user_resumes").document(resume_id).delete()
#         return jsonify({"message": "Resume deleted successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/get-resumes/<user_id>", methods=["GET"])
# def get_resumes(user_id):
#     """Get all resumes for a user"""
#     if not db:
#         return jsonify({"error": "Database not available"}), 500

#     try:
#         docs = db.collection("user_resumes").where("user_id", "==", user_id).stream()
#         resumes = []
#         for doc in docs:
#             data = doc.to_dict()
#             data["id"] = doc.id
#             resumes.append(data)
#         return jsonify({"resumes": resumes}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)





# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # from dotenv import load_dotenv
# # import os
# # import json
# # import time
# # import requests
# # from firebase_admin import credentials, firestore, initialize_app

# # load_dotenv()

# # app = Flask(__name__)
# # CORS(app)

# # # ================== ROLE SKILL MAP (CASE INSENSITIVE) ==================
# # ROLE_SKILL_MAP = {
# #     "machine learning engineer": [
# #         "Python", "NumPy", "Pandas", "Scikit-learn",
# #         "Machine Learning", "Deep Learning",
# #         "TensorFlow", "PyTorch",
# #         "Statistics", "Linear Algebra",
# #         "Model Deployment", "MLOps"
# #     ],
# #     "data scientist": [
# #         "Python", "Pandas", "NumPy",
# #         "Data Analysis", "Statistics",
# #         "Machine Learning", "SQL",
# #         "Data Visualization", "Power BI"
# #     ],
# #     "backend engineer": [
# #         "Python", "Java", "Node.js",
# #         "APIs", "Databases",
# #         "SQL", "System Design",
# #         "Docker", "Cloud"
# #     ],
# #     "frontend engineer": [
# #         "JavaScript", "React", "Vue.js", "Angular",
# #         "HTML", "CSS", "TypeScript",
# #         "Web Design", "UI/UX", "REST APIs"
# #     ],
# #     "full stack developer": [
# #         "JavaScript", "Python", "React", "Node.js",
# #         "Databases", "HTML", "CSS",
# #         "APIs", "System Design", "DevOps"
# #     ],
# #     "devops engineer": [
# #         "Docker", "Kubernetes", "AWS", "Azure",
# #         "CI/CD", "Jenkins", "Linux",
# #         "Terraform", "Cloud Architecture"
# #     ],
# #     "cloud architect": [
# #         "AWS", "Azure", "Google Cloud", "Cloud Design",
# #         "Architecture", "Security", "Scalability",
# #         "Infrastructure", "DevOps"
# #     ]
# # }

# # # ================== FIREBASE ==================
# # try:
# #     cred = credentials.Certificate("serviceAccountKey.json")
# #     initialize_app(cred)
# #     db = firestore.client()
# #     print("✅ Firebase initialized")
# # except Exception as e:
# #     print(f"⚠️ Firebase error: {e}")
# #     db = None

# # # ================== GEMINI ==================
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# # # ================== HELPERS ==================

# # def normalize_role(role):
# #     """Normalize role name for case-insensitive matching"""
# #     return role.strip().lower()

# # def normalize_skill(skill):
# #     return skill.lower().replace("-", " ").strip()

# # def normalize_skills(skills):
# #     return set(normalize_skill(s) for s in skills if isinstance(s, str))

# # def parse_json_response(text):
# #     try:
# #         if "```" in text:
# #             text = text.split("```")[1]
# #         start = text.find("{")
# #         end = text.rfind("}")
# #         if start != -1 and end != -1:
# #             text = text[start:end+1]
# #         return json.loads(text)
# #     except:
# #         return {}

# # def call_gemini_api(prompt, retries=3):
# #     payload = {
# #         "contents": [{"parts": [{"text": prompt}]}],
# #         "generationConfig": {
# #             "temperature": 0.3,
# #             "maxOutputTokens": 1024
# #         }
# #     }

# #     for _ in range(retries):
# #         try:
# #             r = requests.post(
# #                 f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
# #                 json=payload,
# #                 timeout=30
# #             )
# #             if r.status_code == 200:
# #                 return r.json()["candidates"][0]["content"]["parts"][0]["text"]
# #         except:
# #             time.sleep(1)
# #     return ""

# # # ================== CHECK UPLOAD LIMIT ==================

# # def check_upload_limit(user_id):
# #     """Check if user has reached resume upload limit (3)"""
# #     if not db:
# #         return True  # Allow if Firebase not available
    
# #     try:
# #         docs = db.collection("user_resumes").where("user_id", "==", user_id).stream()
# #         count = len(list(docs))
# #         return count < 3
# #     except:
# #         return True

# # # ================== CORE LOGIC ==================

# # def extract_skills_from_resume(resume_text):
# #     prompt = f"""
# # Return ONLY JSON.

# # Extract skills from this resume:
# # {resume_text[:2000]}

# # Format:
# # {{
# #   "technical": ["Python", "JavaScript"],
# #   "tools": ["Git"],
# #   "soft": ["Communication"],
# #   "languages": ["Python"]
# # }}
# # """
# #     text = call_gemini_api(prompt)
# #     result = parse_json_response(text)

# #     return result if result else {
# #         "technical": ["Python"],
# #         "tools": ["Git"],
# #         "soft": [],
# #         "languages": []
# #     }

# # def generate_role_skills_from_gemini(role):
# #     prompt = f"""
# # Return ONLY JSON.

# # List 8–12 core skills for role: {role}

# # Format:
# # {{ "skills": ["Skill1", "Skill2"] }}
# # """
# #     text = call_gemini_api(prompt)
# #     result = parse_json_response(text)
# #     return result.get("skills", [])

# # def analyze_skill_gaps(current_skills, target_role):
# #     # Normalize role for case-insensitive lookup
# #     role_key = normalize_role(target_role)
# #     role_skills = ROLE_SKILL_MAP.get(role_key)

# #     if not role_skills:
# #         role_skills = generate_role_skills_from_gemini(target_role)
# #         if db and role_skills:
# #             db.collection("role_skills").document(role_key).set({
# #                 "original_role": target_role,
# #                 "skills": role_skills,
# #                 "source": "gemini",
# #                 "timestamp": firestore.SERVER_TIMESTAMP
# #             })

# #     if not role_skills:
# #         return []

# #     resume_skills = normalize_skills(
# #         current_skills.get("technical", []) +
# #         current_skills.get("tools", [])
# #     )

# #     gaps = []
# #     for skill in role_skills:
# #         if normalize_skill(skill) not in resume_skills:
# #             gaps.append({
# #                 "skill": skill,
# #                 "importance": "High" if skill in role_skills[:6] else "Medium",
# #                 "proficiency": 0,
# #                 "learning_resource": f"Learn {skill} (Coursera / YouTube)"
# #             })

# #     return gaps

# # def calculate_match_score(skill_gaps):
# #     score = max(30, 100 - len(skill_gaps) * 5)
# #     return {
# #         "match_score": score,
# #         "readiness": "Moderate",
# #         "timeline_months": 3,
# #         "difficulty": "Moderate"
# #     }

# # def generate_roadmap(skill_gaps, target_role):
# #     gaps = [g["skill"] for g in skill_gaps[:5]]

# #     if not gaps:
# #         return [{
# #             "week": "1–12",
# #             "phase": "Job Readiness",
# #             "focus": f"Strengthen profile for {target_role}",
# #             "tasks": ["Advanced project", "Interview prep"]
# #         }]

# #     prompt = f"""
# # Return ONLY JSON.

# # Create a 12-week roadmap for {target_role}
# # Missing skills: {", ".join(gaps)}

# # Format:
# # {{ "roadmap": [{{ "week": "1-3", "phase": "Foundations", "focus": "...", "tasks": ["..."] }}] }}
# # """
# #     text = call_gemini_api(prompt)
# #     result = parse_json_response(text)

# #     if result.get("roadmap"):
# #         return result["roadmap"]

# #     return [{
# #         "week": "1–3",
# #         "phase": "Foundations",
# #         "focus": f"Learn {gaps[0]}",
# #         "tasks": [f"Study {gaps[0]}", "Build mini project"]
# #     }]

# # def generate_weekly_tasks(skill_gaps, target_role):
# #     gap_skills = [gap["skill"] for gap in skill_gaps[:5]]

# #     if not gap_skills:
# #         return [
# #             {
# #                 "week": 1,
# #                 "task": f"Build an advanced project related to {target_role}",
# #                 "outcome": "Strengthen existing skills"
# #             },
# #             {
# #                 "week": 2,
# #                 "task": "Refactor and optimize an old project",
# #                 "outcome": "Improve code quality"
# #             }
# #         ]

# #     prompt = f"""
# # Return ONLY valid JSON.

# # Target role: {target_role}
# # Skills to improve: {", ".join(gap_skills)}

# # Create 6 weekly tasks.
# # Each task must include:
# # - week (number)
# # - task (actionable)
# # - outcome (what user gains)

# # Format:
# # {{
# #   "weekly_tasks": [
# #     {{
# #       "week": 1,
# #       "task": "Learn NumPy basics and solve 20 problems",
# #       "outcome": "Comfort with numerical computing"
# #     }}
# #   ]
# # }}
# # """

# #     try:
# #         text = call_gemini_api(prompt)
# #         result = parse_json_response(text)

# #         tasks = result.get("weekly_tasks")
# #         if isinstance(tasks, list) and len(tasks) > 0:
# #             return tasks

# #     except Exception as e:
# #         print("Weekly task generation failed:", e)

# #     # FALLBACK
# #     tasks = []
# #     for i, skill in enumerate(gap_skills[:3], start=1):
# #         tasks.append({
# #             "week": i,
# #             "task": f"Study and practice {skill}",
# #             "outcome": f"Basic proficiency in {skill}"
# #         })

# #     return tasks

# # def identify_strengths():
# #     return {
# #         "strengths": ["Strong programming foundation", "Fast learner"],
# #         "advantages": ["Resume-driven AI analysis"]
# #     }

# # # ================== ROUTES ==================

# # @app.route("/health", methods=["GET"])
# # def health():
# #     return jsonify({"status": "SkillBridge API running"}), 200

# # @app.route("/check-upload-limit/<user_id>", methods=["GET"])
# # def check_limit(user_id):
# #     """Check if user can upload more resumes"""
# #     can_upload = check_upload_limit(user_id)
# #     return jsonify({
# #         "user_id": user_id,
# #         "can_upload": can_upload,
# #         "remaining_uploads": 3 if can_upload else 0
# #     }), 200

# # @app.route("/analyze-resume", methods=["POST"])
# # def analyze_resume():
# #     if not request.is_json:
# #         return jsonify({"error": "Request must be JSON"}), 400

# #     data = request.get_json(silent=True)
# #     if not data:
# #         return jsonify({"error": "Invalid JSON body"}), 400

# #     resume_text = data.get("resume_text")
# #     target_role = data.get("target_role")
# #     user_id = data.get("user_id", "anonymous")

# #     if not resume_text:
# #         return jsonify({"error": "resume_text is required"}), 400

# #     if not target_role:
# #         return jsonify({"error": "target_role is required"}), 400

# #     # Check upload limit
# #     if user_id != "anonymous" and not check_upload_limit(user_id):
# #         return jsonify({
# #             "error": "You have reached the maximum of 3 resume uploads. Please delete an old resume or build manually."
# #         }), 403

# #     # Normalize target role (case-insensitive)
# #     target_role_normalized = target_role.strip()

# #     current_skills = extract_skills_from_resume(resume_text)
# #     skill_gaps = analyze_skill_gaps(current_skills, target_role_normalized)
# #     match = calculate_match_score(skill_gaps)
# #     roadmap = generate_roadmap(skill_gaps, target_role_normalized) 
# #     weekly_tasks = generate_weekly_tasks(skill_gaps, target_role_normalized)

# #     # Save analysis to Firebase
# #     if db and user_id != "anonymous":
# #         try:
# #             db.collection("user_analyses").add({
# #                 "user_id": user_id,
# #                 "target_role": target_role_normalized,
# #                 "current_skills": current_skills,
# #                 "skill_gaps": skill_gaps,
# #                 "match_score": match["match_score"],
# #                 "timestamp": firestore.SERVER_TIMESTAMP
# #             })
# #         except Exception as e:
# #             print(f"Firebase save error: {e}")

# #     strengths = identify_strengths()

# #     return jsonify({
# #         "targetRole": target_role_normalized,
# #         "currentSkills": current_skills,
# #         "skillGaps": skill_gaps,
# #         "matchScore": match["match_score"],
# #         "readiness": match["readiness"],
# #         "timelineMonths": match["timeline_months"],
# #         "difficulty": match["difficulty"],
# #         "roadmap": roadmap,
# #         "weeklyTasks": weekly_tasks,
# #         "strengths": strengths["strengths"],
# #         "competitiveAdvantages": strengths["advantages"]
# #     }), 200

# # @app.errorhandler(400)
# # def bad_request(e):
# #     return jsonify({"error": "Bad request"}), 400

# # @app.errorhandler(500)
# # def server_error(e):
# #     return jsonify({"error": "Internal server error"}), 500

# # if __name__ == "__main__":
# #     app.run(debug=True, host="0.0.0.0", port=5000)

















# # from flask import Flask, request, jsonify
# # from firebase_admin import credentials, firestore, initialize_app
# # from flask_cors import CORS
# # from dotenv import load_dotenv
# # import cloudinary
# # import cloudinary.uploader
# # import os
# # import uuid
# # import pdfplumber
# # import json
# # import time
# # import requests

# # # ================== LOAD ENV ==================
# # load_dotenv()

# # app = Flask(__name__)
# # CORS(app)

# # # ================== ROLE SKILL MAP ==================
# # ROLE_SKILL_MAP = {
# #     "Machine Learning Engineer": [
# #         "Python", "NumPy", "Pandas", "Scikit-learn",
# #         "Machine Learning", "Deep Learning",
# #         "TensorFlow", "PyTorch",
# #         "Statistics", "Linear Algebra",
# #         "Model Deployment", "MLOps"
# #     ],
# #     "Data Scientist": [
# #         "Python", "Pandas", "NumPy",
# #         "Data Analysis", "Statistics",
# #         "Machine Learning", "SQL",
# #         "Data Visualization", "Power BI"
# #     ],
# #     "Backend Engineer": [
# #         "Python", "Java", "Node.js",
# #         "APIs", "Databases",
# #         "SQL", "System Design",
# #         "Docker", "Cloud"
# #     ]
# # }

# # # ================== FIREBASE ==================
# # try:
# #     cred = credentials.Certificate("serviceAccountKey.json")
# #     initialize_app(cred)
# #     db = firestore.client()
# #     print("✅ Firebase initialized")
# # except Exception as e:
# #     print(f"⚠️ Firebase error: {e}")
# #     db = None

# # # ================== CLOUDINARY ==================
# # cloudinary.config(
# #     cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
# #     api_key=os.getenv("CLOUDINARY_API_KEY"),
# #     api_secret=os.getenv("CLOUDINARY_API_SECRET")
# # )
# # print("✅ Cloudinary configured")

# # # ================== GEMINI ==================
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # if not GEMINI_API_KEY:
# #     raise ValueError("GEMINI_API_KEY missing")

# # GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
# # print("✅ Gemini API configured")

# # # ================== HELPERS ==================

# # def normalize_skill(skill):
# #     return skill.lower().replace("-", " ").strip()

# # def normalize_skills(skills):
# #     return set(normalize_skill(s) for s in skills if isinstance(s, str))

# # def parse_json_response(text):
# #     try:
# #         if "```" in text:
# #             text = text.split("```")[1]
# #         start = text.find("{")
# #         end = text.rfind("}")
# #         if start != -1 and end != -1:
# #             text = text[start:end+1]
# #         return json.loads(text)
# #     except:
# #         return {}

# # def call_gemini_api(prompt, retries=3):
# #     payload = {
# #         "contents": [{"parts": [{"text": prompt}]}],
# #         "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}
# #     }
# #     for _ in range(retries):
# #         try:
# #             r = requests.post(
# #                 f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
# #                 json=payload,
# #                 timeout=30
# #             )
# #             if r.status_code == 200:
# #                 return r.json()["candidates"][0]["content"]["parts"][0]["text"]
# #         except:
# #             time.sleep(1)
# #     return ""

# # # ================== CORE AI LOGIC ==================

# # def extract_skills_from_resume(resume_text):
# #     prompt = f"""
# # Return ONLY JSON.

# # Extract technical skills, tools, soft skills from this resume:

# # {resume_text[:2000]}

# # Format:
# # {{
# #   "technical": ["Python"],
# #   "tools": ["Git"],
# #   "soft": ["Communication"],
# #   "languages": ["Python"]
# # }}
# # """
# #     try:
# #         text = call_gemini_api(prompt)
# #         result = parse_json_response(text)
# #         return result if result else {
# #             "technical": ["Python"],
# #             "tools": ["Git"],
# #             "soft": [],
# #             "languages": []
# #         }
# #     except:
# #         return {"technical": ["Python"], "tools": ["Git"], "soft": [], "languages": []}

# # def generate_role_skills_from_gemini(role):
# #     prompt = f"""
# # Return ONLY JSON.

# # List 8–12 core skills required for role: {role}

# # Format:
# # {{ "skills": ["Skill1", "Skill2"] }}
# # """
# #     try:
# #         text = call_gemini_api(prompt)
# #         result = parse_json_response(text)
# #         return result.get("skills", [])
# #     except:
# #         return []

# # def analyze_skill_gaps(current_skills, target_role):
# #     target_role = target_role.strip()

# #     role_skills = ROLE_SKILL_MAP.get(target_role)

# #     if not role_skills:
# #         role_skills = generate_role_skills_from_gemini(target_role)
# #         if db and role_skills:
# #             db.collection("role_skills").document(target_role).set({
# #                 "skills": role_skills,
# #                 "source": "gemini",
# #                 "timestamp": firestore.SERVER_TIMESTAMP
# #             })

# #     if not role_skills:
# #         return []

# #     resume_skills = normalize_skills(
# #         current_skills.get("technical", []) +
# #         current_skills.get("tools", [])
# #     )

# #     gaps = []
# #     for skill in role_skills:
# #         if normalize_skill(skill) not in resume_skills:
# #             gaps.append({
# #                 "skill": skill,
# #                 "importance": "High" if skill in role_skills[:6] else "Medium",
# #                 "proficiency": 0,
# #                 "learning_resource": f"Learn {skill} (Coursera / YouTube)"
# #             })

# #     return gaps

# # def calculate_match_score(current_skills, skill_gaps, target_role):
# #     return {
# #         "match_score": max(30, 100 - len(skill_gaps) * 5),
# #         "readiness": "Moderate",
# #         "timeline_months": 3,
# #         "difficulty": "Moderate"
# #     }

# # def generate_roadmap(current_skills, skill_gaps, target_role):
# #     gaps = [g["skill"] for g in skill_gaps[:5]]

# #     if not gaps:
# #         return [{
# #             "week": "1-12",
# #             "phase": "Job Readiness",
# #             "focus": f"Strengthen profile for {target_role}",
# #             "tasks": ["Build advanced project", "Prepare interviews"]
# #         }]

# #     prompt = f"""
# # Return ONLY JSON.

# # Create a 12-week roadmap for {target_role}
# # Missing skills: {", ".join(gaps)}

# # Format:
# # {{ "roadmap": [{{ "week": "1-3", "phase": "Foundations", "focus": "...", "tasks": ["..."] }}] }}
# # """
# #     try:
# #         text = call_gemini_api(prompt)
# #         result = parse_json_response(text)
# #         if result.get("roadmap"):
# #             return result["roadmap"]
# #     except:
# #         pass

# #     return [{
# #         "week": "1-3",
# #         "phase": "Foundations",
# #         "focus": f"Learn {gaps[0]}",
# #         "tasks": [f"Study {gaps[0]}", f"Build mini project"]
# #     }]

# # def identify_strengths(resume_text, current_skills, target_role):
# #     return {
# #         "strengths": ["Strong programming foundation", "Good learning ability"],
# #         "advantages": ["Resume-driven AI analysis"]
# #     }

# # # ================== ROUTES ==================

# # @app.route("/health")
# # def health():
# #     return jsonify({"status": "ok"})

# # @app.route("/analyze-resume", methods=["POST"])
# # def analyze_resume():
# #     data = request.get_json()
# #     resume_text = data.get("resume_text", "")
# #     target_role = data.get("target_role", "")

# #     current_skills = extract_skills_from_resume(resume_text)
# #     skill_gaps = analyze_skill_gaps(current_skills, target_role)
# #     match = calculate_match_score(current_skills, skill_gaps, target_role)
# #     roadmap = generate_roadmap(current_skills, skill_gaps, target_role)
# #     strengths = identify_strengths(resume_text, current_skills, target_role)

# #     return jsonify({
# #         "targetRole": target_role,
# #         "currentSkills": current_skills,
# #         "skillGaps": skill_gaps,
# #         "matchScore": match["match_score"],
# #         "readiness": match["readiness"],
# #         "timelineMonths": match["timeline_months"],
# #         "difficulty": match["difficulty"],
# #         "roadmap": roadmap,
# #         "strengths": strengths["strengths"],
# #         "competitiveAdvantages": strengths["advantages"]
# #     })

# # # ================== RUN ==================
# # if __name__ == "__main__":
# #     app.run(debug=True, port=5000)





















































# # ROLE_SKILL_MAP = {
# #     "Machine Learning Engineer": [
# #         "Python", "NumPy", "Pandas", "Scikit-learn",
# #         "Machine Learning", "Deep Learning",
# #         "TensorFlow", "PyTorch",
# #         "Statistics", "Linear Algebra",
# #         "Model Deployment", "MLOps"
# #     ],
# #     "Data Scientist": [
# #         "Python", "Pandas", "NumPy",
# #         "Data Analysis", "Statistics",
# #         "Machine Learning", "SQL",
# #         "Data Visualization", "Power BI"
# #     ],
# #     "Backend Engineer": [
# #         "Python", "Java", "Node.js",
# #         "APIs", "Databases",
# #         "SQL", "System Design",
# #         "Docker", "Cloud"
# #     ]
# # }

# # from flask import Flask, request, jsonify
# # from firebase_admin import credentials, firestore, initialize_app
# # from flask_cors import CORS
# # from dotenv import load_dotenv
# # import cloudinary
# # import cloudinary.uploader
# # import os
# # import uuid
# # import pdfplumber
# # import json
# # import time
# # import requests

# # load_dotenv()

# # app = Flask(__name__)
# # CORS(app)

# # # ================== FIREBASE ==================
# # try:
# #     cred = credentials.Certificate("serviceAccountKey.json")
# #     initialize_app(cred)
# #     db = firestore.client()
# #     print("✅ Firebase initialized")
# # except Exception as e:
# #     print(f"⚠️ Firebase error: {e}")
# #     db = None

# # # ================== CLOUDINARY ==================
# # cloudinary.config(
# #     cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
# #     api_key=os.getenv("CLOUDINARY_API_KEY"),
# #     api_secret=os.getenv("CLOUDINARY_API_SECRET")
# # )
# # print("✅ Cloudinary configured")

# # # ================== GEMINI API (REST) ==================
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # if not GEMINI_API_KEY:
# #     raise ValueError("GEMINI_API_KEY not found in environment")

# # GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
# # print("✅ Gemini API configured (REST)")

# # UPLOAD_LIMIT = 3


# # # ================== UTILITY FUNCTIONS ==================

# # def parse_json_response(response_text):
# #     """Safely parse JSON from API response"""
# #     try:
# #         # Remove markdown code blocks
# #         if '```json' in response_text:
# #             response_text = response_text.split('```json')[1].split('```')[0]
# #         elif '```' in response_text:
# #             response_text = response_text.split('```')[1].split('```')[0]
        
# #         response_text = response_text.strip()
        
# #         # Try to find JSON object if wrapped in text
# #         if not response_text.startswith('{'):
# #             # Find first { and last }
# #             start = response_text.find('{')
# #             end = response_text.rfind('}')
# #             if start != -1 and end != -1:
# #                 response_text = response_text[start:end+1]
        
# #         result = json.loads(response_text)
# #         print(f"✅ Parsed JSON: {str(result)[:100]}")
# #         return result
# #     except json.JSONDecodeError as e:
# #         print(f"❌ JSON Parse Error: {str(e)}")
# #         print(f"Response was: {response_text[:300]}")
# #         return {}


# # def call_gemini_api(prompt, retry_count=3):
# #     """Call Gemini API via REST with retry logic"""
# #     headers = {
# #         "Content-Type": "application/json",
# #     }
    
# #     payload = {
# #         "contents": [
# #             {
# #                 "parts": [
# #                     {
# #                         "text": prompt
# #                     }
# #                 ]
# #             }
# #         ],
# #         "generationConfig": {
# #             "temperature": 0.3,
# #             "maxOutputTokens": 1024,
# #         }
# #     }
    
# #     for attempt in range(retry_count):
# #         try:
# #             response = requests.post(
# #                 f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
# #                 headers=headers,
# #                 json=payload,
# #                 timeout=30
# #             )
            
# #             if response.status_code == 200:
# #                 result = response.json()
# #                 if "candidates" in result and len(result["candidates"]) > 0:
# #                     return result["candidates"][0]["content"]["parts"][0]["text"]
# #                 else:
# #                     raise Exception("No candidates in response")
# #             elif response.status_code == 429:  # Rate limited
# #                 if attempt < retry_count - 1:
# #                     wait_time = (attempt + 1) * 2
# #                     print(f"⏱️ Rate limited. Waiting {wait_time}s...")
# #                     time.sleep(wait_time)
# #                     continue
# #                 else:
# #                     raise Exception(f"Rate limited after {retry_count} attempts")
# #             else:
# #                 error_msg = response.text
# #                 print(f"API Error ({response.status_code}): {error_msg[:200]}")
# #                 raise Exception(f"API Error: {response.status_code}")
# #         except requests.exceptions.Timeout:
# #             if attempt < retry_count - 1:
# #                 print(f"Timeout, retrying... ({attempt + 1}/{retry_count})")
# #                 time.sleep(2)
# #                 continue
# #             raise
# #         except Exception as e:
# #             if attempt < retry_count - 1:
# #                 print(f"Attempt {attempt + 1} failed: {str(e)[:50]}")
# #                 time.sleep(1)
# #                 continue
# #             raise
    
# #     return None


# # def extract_skills_from_resume(resume_text):
# #     """Extract current skills using Gemini"""
# #     prompt = f"""IMPORTANT: You MUST return ONLY valid JSON. No other text.

# # Extract ALL skills from this resume:

# # RESUME:
# # {resume_text[:2000]}

# # Find:
# # 1. All programming languages and technical frameworks
# # 2. All soft skills
# # 3. All tools and platforms
# # 4. All programming languages

# # Return ONLY this JSON:
# # {{"technical": ["Python", "JavaScript", "React", "Django", "SQL", "AWS", "Docker"], "soft": ["Leadership", "Communication", "Problem Solving", "Team Work"], "tools": ["Git", "Docker", "VS Code", "Jira"], "languages": ["Python", "JavaScript", "SQL"]}}

# # CRITICAL: Start with {{ and end with }}. No text before or after JSON."""
    
# #     try:
# #         response_text = call_gemini_api(prompt)
# #         result = parse_json_response(response_text)
# #         if not result or not result.get('technical'):
# #             print("⚠️ Empty skills, using defaults")
# #             return {
# #                 "technical": ["Python", "JavaScript", "React"],
# #                 "soft": ["Communication", "Problem Solving"],
# #                 "tools": ["Git", "Docker"],
# #                 "languages": ["Python", "JavaScript"]
# #             }
# #         return result
# #     except Exception as e:
# #         print(f"Error extracting skills: {e}")
# #         return {"technical": ["Python", "JavaScript"], "soft": ["Communication"], "tools": ["Git"], "languages": ["Python"]}

# # def normalize_skills(skills):
# #     return set(skill.lower().strip() for skill in skills)

# # def normalize_skills(skills):
# #     if not skills:
# #         return set()
# #     return set(skill.lower().strip() for skill in skills if isinstance(skill, str))

# # def analyze_skill_gaps(current_skills, target_role):
# #     target_role = target_role.strip()
# #     role_skills = ROLE_SKILL_MAP.get(target_role)

# #     if not role_skills:
# #         role_skills = generate_role_skills_from_gemini(target_role)

        
# #         if db and role_skills:
# #             db.collection("role_skills").document(target_role).set({
# #                 "skills": role_skills,
# #                 "source": "gemini",
# #                 "timestamp": firestore.SERVER_TIMESTAMP
# #             })

# #     if not current_skills or not role_skills:
# #         return []

# #     resume_skills = normalize_skills(
# #         current_skills.get("technical", []) +
# #         current_skills.get("tools", [])
# #     )

# #     gaps = []
# #     for skill in role_skills:
# #         if skill.lower() not in resume_skills:
# #             gaps.append({
# #                 "skill": skill,
# #                 "importance": "High" if skill in role_skills[:6] else "Medium",
# #                 "proficiency": 0,
# #                 "learning_resource": f"Learn {skill} (Coursera / YouTube)"
# #             })

# #     return gaps




# # def calculate_match_score(current_skills, skill_gaps, target_role):
# #     """Calculate match score"""
# #     current_count = len(current_skills.get('technical', []))
# #     gaps_count = len(skill_gaps)
# #     high_gaps = sum(1 for gap in skill_gaps if gap.get('importance') == 'High')
    
# #     prompt = f"""Candidate Profile:
# # - Technical skills: {current_count}
# # - Target role: {target_role}
# # - Skills to learn: {gaps_count} ({high_gaps} high priority)

# # Calculate a realistic match score (0-100) for this {target_role} position.

# # Return ONLY JSON:
# # {{
# #     "match_score": 65,
# #     "readiness": "Moderate",
# #     "timeline_months": 3,
# #     "difficulty": "Moderate"
# # }}

# # readiness: "High", "Moderate", or "Low"
# # difficulty: "Easy", "Moderate", or "Hard"
# # Return ONLY JSON."""
    
# #     try:
# #         response_text = call_gemini_api(prompt)
# #         result = parse_json_response(response_text)
# #         return result
# #     except Exception as e:
# #         print(f"Error calculating score: {e}")
# #         return {"match_score": 50, "readiness": "Moderate", "timeline_months": 3, "difficulty": "Moderate"}


# # def generate_roadmap(current_skills, skill_gaps, target_role):
# #     """
# #     Generate a 12-week roadmap. Always returns a roadmap.
# #     """

# #     # Extract missing skills safely
# #     gaps_list = [gap["skill"] for gap in skill_gaps[:5]]
# #     gaps_str = ", ".join(gaps_list)

# #     # If no gaps, create an improvement roadmap
# #     if not gaps_list:
# #         return [
# #             {
# #                 "week": "1-4",
# #                 "phase": "Skill Enhancement",
# #                 "focus": f"Strengthen existing skills for {target_role}",
# #                 "tasks": [
# #                     "Revise core concepts",
# #                     "Build one advanced project",
# #                     "Optimize existing projects"
# #                 ]
# #             },
# #             {
# #                 "week": "5-8",
# #                 "phase": "Advanced Practice",
# #                 "focus": "Real-world problem solving",
# #                 "tasks": [
# #                     "Solve real datasets",
# #                     "Improve performance & scalability",
# #                     "Write technical documentation"
# #                 ]
# #             },
# #             {
# #                 "week": "9-12",
# #                 "phase": "Job Readiness",
# #                 "focus": "Portfolio & interviews",
# #                 "tasks": [
# #                     "Polish resume",
# #                     "Mock interviews",
# #                     "Apply to jobs"
# #                 ]
# #             }
# #         ]

# #     prompt = f"""IMPORTANT: Return ONLY valid JSON.

# # Target role: {target_role}
# # Missing skills: {gaps_str}

# # Create a detailed 12-week roadmap.
# # Split into 4 phases.
# # Each phase must include:
# # - week
# # - phase
# # - focus
# # - tasks (list)

# # Return ONLY JSON:
# # {{
# #   "roadmap": [
# #     {{
# #       "week": "1-2",
# #       "phase": "Foundations",
# #       "focus": "Core fundamentals",
# #       "tasks": ["Task 1", "Task 2"]
# #     }}
# #   ]
# # }}
# # """

# #     try:
# #         response_text = call_gemini_api(prompt)
# #         result = parse_json_response(response_text)

# #         roadmap = result.get("roadmap")

# #         # HARD GUARANTEE
# #         if isinstance(roadmap, list) and len(roadmap) > 0:
# #             return roadmap

# #     except Exception as e:
# #         print("Roadmap generation failed:", e)

# #     # 🔒 FINAL FALLBACK (NEVER EMPTY)
# #     return [
# #         {
# #             "week": "1-3",
# #             "phase": "Foundations",
# #             "focus": f"Learn {gaps_list[0]}",
# #             "tasks": [
# #                 f"Study basics of {gaps_list[0]}",
# #                 f"Build a small project using {gaps_list[0]}"
# #             ]
# #         },
# #         {
# #             "week": "4-6",
# #             "phase": "Core Skills",
# #             "focus": f"Apply {gaps_list[1] if len(gaps_list) > 1 else gaps_list[0]}",
# #             "tasks": [
# #                 "Practice with datasets",
# #                 "Implement algorithms"
# #             ]
# #         },
# #         {
# #             "week": "7-12",
# #             "phase": "Job Readiness",
# #             "focus": "Portfolio + Interview Prep",
# #             "tasks": [
# #                 "Build capstone project",
# #                 "Prepare interview questions"
# #             ]
# #         }
# #     ]


# # def identify_strengths(resume_text, current_skills, target_role):
# #     """Identify candidate's key strengths"""
# #     current_tech = ", ".join(current_skills.get('technical', [])[:5])
    
# #     prompt = f"""IMPORTANT: You MUST return ONLY valid JSON. No other text.

# # Analyze candidate strengths for {target_role}.

# # Resume: {resume_text[:1000]}
# # Skills: {current_tech}

# # Identify 4-5 key strengths and 2-3 competitive advantages.

# # Return ONLY this JSON:
# # {{"strengths": ["Strong foundation in multiple languages", "Experience with cloud platforms", "Proven ability to learn new technologies", "Good problem-solving skills", "Leadership experience"], "advantages": ["Already familiar with ML basics", "Strong software engineering foundation", "DevOps experience helps with deployment"]}}

# # CRITICAL: Start with {{ and end with }}. No text before or after JSON."""
    
# #     try:
# #         response_text = call_gemini_api(prompt)
# #         result = parse_json_response(response_text)
# #         if not result.get('strengths'):
# #             return {
# #                 "strengths": [
# #                     f"Strong foundation in {current_tech}",
# #                     "Proven learning ability",
# #                     "Relevant experience",
# #                     "Problem-solving skills"
# #                 ],
# #                 "advantages": ["Good foundation", "Quick learner", "Relevant skills"]
# #             }
# #         return result
# #     except Exception as e:
# #         print(f"Error identifying strengths: {e}")
# #         return {"strengths": ["Technical skills", "Learning ability", "Relevant experience"], "advantages": ["Learning ability", "Technical background"]}


# # # ================== API ROUTES ==================

# # @app.route("/health", methods=["GET"])
# # def health_check():
# #     return jsonify({"status": "SkillBridge API is running"}), 200


# # @app.route("/upload-resume", methods=["POST"])
# # def upload_resume():
# #     """Upload resume to Cloudinary and extract text"""
# #     try:
# #         user_id = request.form.get("user_id", "anonymous")
# #         file = request.files.get("resume")
# #         target_role = request.form.get("target_role", "")

# #         if not file:
# #             return jsonify({"error": "Missing resume file"}), 400

# #         # Upload to Cloudinary
# #         upload_result = cloudinary.uploader.upload(
# #             file,
# #             resource_type="raw",
# #             folder=f"resumes/{user_id}",
# #             public_id=str(uuid.uuid4())
# #         )
# #         file_url = upload_result["secure_url"]

# #         # Extract text from PDF
# #         extracted_text = ""
# #         file.seek(0)
# #         try:
# #             with pdfplumber.open(file) as pdf:
# #                 for page in pdf.pages:
# #                     extracted_text += page.extract_text() or ""
# #         except Exception as pdf_error:
# #             print(f"PDF extraction error: {pdf_error}")

# #         # Save to Firebase if available
# #         if db:
# #             db.collection("resumes").add({
# #                 "user_id": user_id,
# #                 "file_url": file_url,
# #                 "text": extracted_text,
# #                 "target_role": target_role
# #             })

# #         return jsonify({
# #             "message": "Resume uploaded successfully",
# #             "file_url": file_url,
# #             "extracted_text": extracted_text[:500],
# #             "text_length": len(extracted_text)
# #         }), 200

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # def generate_role_skills_from_gemini(target_role):
# #     prompt = f"""Return ONLY JSON.

# # List 8–12 core skills required for the role: {target_role}

# # Format:
# # {{ "skills": ["Skill1", "Skill2", "Skill3"] }}
# # """

# #     try:
# #         response = call_gemini_api(prompt)
# #         result = parse_json_response(response)
# #         return result.get("skills", [])
# #     except:
# #         return []


# # @app.route("/analyze-resume", methods=["POST"])
# # def analyze_resume():
# #     """Complete skill analysis pipeline"""
# #     try:
# #         data = request.get_json()
# #         if not data:
# #             return jsonify({"error": "Invalid JSON"}), 400

# #         resume_text = data.get("resume_text", "")
# #         target_role = data.get("target_role", "")

# #         if not resume_text or not target_role:
# #             return jsonify({"error": "Missing resume_text or target_role"}), 400

# #         print(f"\n🔄 Analyzing resume for: {target_role}")

# #         # STEP 1: Extract skills ONCE
# #         print("📍 Step 1: Extracting current skills...")
# #         current_skills = extract_skills_from_resume(resume_text) or {
# #             "technical": [],
# #             "tools": [],
# #             "languages": [],
# #             "soft": []
# #         }
# #         print(f"   ✅ Found {len(current_skills.get('technical', []))} technical skills")

# #         # STEP 2: Analyze skill gaps (deterministic)
# #         print("📍 Step 2: Analyzing skill gaps...")
# #         skill_gaps = analyze_skill_gaps(current_skills, target_role) or []
# #         print("FINAL SKILL GAPS:", skill_gaps)

# #         # STEP 3: Calculate match score
# #         print("📍 Step 3: Calculating match score...")
# #         match_info = calculate_match_score(current_skills, skill_gaps, target_role)
# #         print(f"   ✅ Match score: {match_info.get('match_score', 'N/A')}%")

# #         # STEP 4: Generate roadmap (AI, grounded)
# #         print("📍 Step 4: Generating learning roadmap...")
# #         roadmap = generate_roadmap(current_skills, skill_gaps, target_role)
# #         print(f"   ✅ Created {len(roadmap)} learning phases")

# #         # STEP 5: Identify strengths
# #         print("📍 Step 5: Identifying strengths...")
# #         strengths = identify_strengths(resume_text, current_skills, target_role)
# #         print(f"   ✅ Found {len(strengths.get('strengths', []))} key strengths")

# #         # FINAL RESPONSE
# #         analysis = {
# #             "targetRole": target_role,
# #             "currentSkills": current_skills,
# #             "skillGaps": skill_gaps,
# #             "matchScore": match_info.get("match_score", 50),
# #             "readiness": match_info.get("readiness", "Moderate"),
# #             "timelineMonths": match_info.get("timeline_months", 3),
# #             "difficulty": match_info.get("difficulty", "Moderate"),
# #             "roadmap": roadmap,
# #             "strengths": strengths.get("strengths", []),
# #             "competitiveAdvantages": strengths.get("advantages", [])
# #         }

# #         print("✅ Analysis complete!\n")
# #         return jsonify(analysis), 200

# #     except Exception as e:
# #         print(f"❌ Error: {e}")
# #         return jsonify({"error": str(e)}), 500



# # @app.route("/full-analysis", methods=["POST"])
# # def full_analysis():
# #     """Combined upload + analyze in one request"""
# #     try:
# #         user_id = request.form.get("user_id", "anonymous")
# #         file = request.files.get("resume")
# #         target_role = request.form.get("target_role", "")

# #         if not file or not target_role:
# #             return jsonify({"error": "Missing resume file or target_role"}), 400

# #         # Upload to Cloudinary
# #         upload_result = cloudinary.uploader.upload(
# #             file,
# #             resource_type="raw",
# #             folder=f"resumes/{user_id}",
# #             public_id=str(uuid.uuid4())
# #         )
# #         file_url = upload_result["secure_url"]

# #         # Extract text
# #         extracted_text = ""
# #         file.seek(0)
# #         try:
# #             with pdfplumber.open(file) as pdf:
# #                 for page in pdf.pages:
# #                     extracted_text += page.extract_text() or ""
# #         except:
# #             pass

# #         # Run full analysis
# #         current_skills = extract_skills_from_resume(extracted_text)
# #         skill_gaps = analyze_skill_gaps(current_skills, target_role)
# #         match_info = calculate_match_score(current_skills, skill_gaps, target_role)
# #         roadmap = generate_roadmap(current_skills, skill_gaps, target_role)
# #         strengths = identify_strengths(extracted_text, current_skills, target_role)

# #         # Save to Firebase if available
# #         if db:
# #             db.collection("analyses").add({
# #                 "user_id": user_id,
# #                 "target_role": target_role,
# #                 "file_url": file_url,
# #                 "timestamp": firestore.SERVER_TIMESTAMP
# #             })

# #         return jsonify({
# #             "resumeUrl": file_url,
# #             "targetRole": target_role,
# #             "currentSkills": current_skills,
# #             "skillGaps": skill_gaps,
# #             "matchScore": match_info.get('match_score', 50),
# #             "readiness": match_info.get('readiness', 'Moderate'),
# #             "timelineMonths": match_info.get('timeline_months', 3),
# #             "difficulty": match_info.get('difficulty', 'Moderate'),
# #             "roadmap": roadmap,
# #             "strengths": strengths.get('strengths', []),
# #             "competitiveAdvantages": strengths.get('advantages', [])
# #         }), 200

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500


# # @app.errorhandler(404)
# # def not_found(error):
# #     return jsonify({"error": "Endpoint not found"}), 404


# # @app.errorhandler(500)
# # def server_error(error):
# #     return jsonify({"error": "Internal server error"}), 500


# # if __name__ == "__main__":
# #     print("\n" + "="*80)
# #     print("🚀 SkillBridge Backend - Production Mode (Gemini REST API)")
# #     print("="*80 + "\n")
# #     app.run(debug=True, host="0.0.0.0", port=5000)