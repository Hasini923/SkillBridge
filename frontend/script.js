function uploadResume() {
  const fileInput = document.getElementById("resume");
  const status = document.getElementById("status");

  if (!fileInput.files.length) {
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

  status.innerText = "Resume selected successfully. Ready to upload.";
  status.className = "text-green-400";
}

function analyze() {
  document.getElementById("skills").innerText =
    "Python, SQL, Machine Learning, Git";

  document.getElementById("gaps").innerText =
    "Statistics, Data Visualization, Real-world Projects";

  document.getElementById("roadmap").innerText =
    "Week 1: Learn statistics fundamentals\n" +
    "Week 2: Practice data visualization\n" +
    "Week 3: Build a data science project\n" +
    "Week 4: Revise ML concepts and deploy";

  document.getElementById("distance").innerText =
    "You are 65% aligned with the selected career";
}

