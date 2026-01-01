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
