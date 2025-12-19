// Disclaimer
const modal = document.getElementById("disclaimer-modal");
const closeBtn = document.getElementById("close-modal");
const acceptBtn = document.getElementById("accept-btn");

closeBtn.onclick = () => modal.style.display = "none";
acceptBtn.onclick = () => modal.style.display = "none";

// Upload PDFs
async function uploadPDFs() {
    const input = document.getElementById("pdfInput");
    const status = document.getElementById("upload-status");

    if (!input.files.length) {
        alert("Please select PDF files");
        return;
    }

    const formData = new FormData();
    for (let file of input.files) {
        formData.append("files", file);
    }

    status.innerText = "Uploading...";

    const res = await fetch("/upload_pdfs/", {
        method: "POST",
        body: formData
    });

    if (res.ok) {
        status.innerText = "Upload successful";
    } else {
        status.innerText = "Upload failed";
    }
}

// Ask Question
async function askQuestion() {
    const input = document.getElementById("questionInput");
    const chatBox = document.getElementById("chat-box");

    if (!input.value.trim()) return;

    chatBox.innerHTML += `
        <div class="message user">You: ${input.value}</div>
    `;

    const formData = new FormData();
    formData.append("question", input.value);

    input.value = "";

    const res = await fetch("/ask/", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    chatBox.innerHTML += `
        <div class="message bot">Bot: ${data.response || "No response"}</div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
}
