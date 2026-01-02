/************************************
 * SkillBridge - Frontend Script
 * Step 2: Backend-ready structure
 ************************************/

/* ================================
   CONFIG
================================ */
const API_BASE_URL = "http://localhost:5000"; 
// Later: replace with production backend URL


/* ================================
   GENERIC API HELPER
================================ */
async function postData(endpoint, formData) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    throw new Error("Server error");
  }

  return response.json();
}


/* ================================
   RESUME UPLOAD + PREVIEW
================================ */
function uploadResume() {
  const fileInput = document.getElementById("resume");
  const status = document.getElementById("status");
  const resumeTextArea = document.getElementById("resumeText");

  if (!fileInput || !fileInput.files.length) {
    status.innerText = "Please select a PDF resume first.";
    status.className = "text-red-400";
    return;
  }

  const file = fileInput.files[0];

  if (file.type !== "application/pdf") {
    status.innerText = "Only PDF files are allowed.";
    status.className = "text-red-400";
    return;
  }

  // ================================
  // TODO (BACKEND):
  // Send resume to /upload-resume API
  // ================================

  // TEMP DEMO: Simulated extracted resume text
  resumeTextArea.value =
    "Student with experience in Python, SQL, and Machine Learning.\n" +
    "Worked on data analysis and ML projects.\n" +
    "Familiar with Git, teamwork, and basic deployment.";

  status.innerText =
    "Resume uploaded successfully. You can edit the extracted text.";
  status.className = "text-green-400";
}


/* ================================
   SAVE EDITED RESUME TEXT
================================ */
function saveResumeText() {
  const resumeTextArea = document.getElementById("resumeText");

  if (!resumeTextArea || !resumeTextArea.value.trim()) {
    alert("Resume text cannot be empty.");
    return;
  }

  // ================================
  // TODO (BACKEND):
  // Send cleaned resume text to backend
  // ================================

  alert(
    "Resume text saved successfully.\n" +
    "This version will be used for skill analysis."
  );
}


/* ================================
   SKILL ANALYSIS
================================ */
function analyze() {
  const careerSelect = document.getElementById("career");

  if (!careerSelect) {
    alert("Career selection not found.");
    return;
  }

  const selectedCareer = careerSelect.value;

  // ================================
  // TODO (BACKEND):
  // POST to /analyze endpoint with:
  // - resume text
  // - selected career
  // ================================

  // TEMP DEMO DATA
  document.getElementById("skills").innerText =
    "Python, SQL, Machine Learning, Git";

  document.getElementById("gaps").innerText =
    "Statistics, Data Visualization, System Design";

  document.getElementById("roadmap").innerText =
    "Week 1: Learn statistics basics\n" +
    "Week 2: Practice data visualization\n" +
    "Week 3: Build a real-world project\n" +
    "Week 4: Revise ML concepts and deploy";

  document.getElementById("distance").innerText =
    `You are 65% aligned with the ${selectedCareer} role`;
}


/* ================================
   DASHBOARD PLACEHOLDERS
================================ */
// Later backend will update these dynamically
function updateDashboard() {
  const resumeCount = document.getElementById("resumeCount");

  if (resumeCount) {
    resumeCount.innerText = "2"; // TEMP
  }
}
