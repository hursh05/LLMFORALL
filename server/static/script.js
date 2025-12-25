let ACTIVE_DOC_ID = null;

/* --- DOM ELEMENTS --- */
const els = {
    pdfInput: document.getElementById('pdfInput'),
    fileStatus: document.getElementById('file-status'),
    uploadBtn: document.getElementById('upload-btn'),
    uploadLoader: document.getElementById('upload-loader'),
    questionInput: document.getElementById('questionInput'),
    chatBox: document.getElementById('chat-box'),
    themeToggle: document.getElementById('theme-toggle'),
    themeIcon: document.getElementById('theme-icon'),

    mobileMenuBtn: document.getElementById('mobile-menu-btn'),
    closeSidebarBtn: document.getElementById('close-sidebar-btn'),
    sidebar: document.getElementById('sidebar'),
    overlay: document.getElementById('mobile-overlay'),

    modal: document.getElementById('disclaimer-modal'),
    acceptBtn: document.getElementById('accept-btn')
};

/* --- INITIALIZATION --- */
document.addEventListener('DOMContentLoaded', () => {

    // THEME INIT
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    // EVENTS
    els.themeToggle?.addEventListener('click', toggleTheme);

    els.pdfInput?.addEventListener('change', handleFileSelect);

    els.questionInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') askQuestion();
    });

    els.acceptBtn?.addEventListener('click', () => {
        els.modal.style.display = 'none';
    });

    els.mobileMenuBtn?.addEventListener('click', () => {
        els.sidebar.classList.add('active');
        els.overlay.classList.add('active');
    });

    const closeMenu = () => {
        els.sidebar.classList.remove('active');
        els.overlay.classList.remove('active');
    };

    els.closeSidebarBtn?.addEventListener('click', closeMenu);
    els.overlay?.addEventListener('click', closeMenu);
});

/* --- FUNCTIONS --- */

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    if (!els.themeIcon) return;
    els.themeIcon.className =
        theme === 'dark' ? 'ri-moon-clear-line' : 'ri-sun-line';
}

function handleFileSelect() {
    const files = els.pdfInput.files;

    if (files.length > 0) {
        els.fileStatus.innerText = `${files.length} file(s) selected`;
        els.fileStatus.style.color = "var(--accent-primary)";
        els.uploadBtn.disabled = false;
    } else {
        els.fileStatus.innerText = "No active documents";
        els.uploadBtn.disabled = true;
    }
}

function clearChat() {
    ACTIVE_DOC_ID = null; // ✅ REQUIRED

    els.chatBox.innerHTML = `
        <div class="msg-row bot-row">
            <div class="msg-bubble welcome-bubble">
                <h3>Chat Cleared</h3>
                <p>Please upload a document to begin.</p>
            </div>
        </div>
    `;
}


async function uploadPDFs() {
    if (!els.pdfInput.files.length) return;

    els.uploadBtn.disabled = true;
    els.uploadBtn.innerHTML = `<i class="ri-loader-4-line ri-spin"></i> Processing...`;
    els.uploadLoader.style.width = "100%";

    const formData = new FormData();
    for (let file of els.pdfInput.files) {
        formData.append("files", file);
    }

    try {
        const res = await fetch("/upload_pdfs/", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (!data.doc_id) {
            throw new Error("No document ID returned");
        }

        ACTIVE_DOC_ID = data.doc_id;

        const setForm = new FormData();
        setForm.append("doc_id", ACTIVE_DOC_ID);
        await fetch("/set_current_doc/", {
            method: "POST",
            body: setForm
        });

        els.uploadBtn.innerHTML = `<i class="ri-check-line"></i> Context Ready`;
        els.uploadBtn.style.background = "#22c55e";
        els.uploadLoader.style.width = "0%";

        addSystemMsg(`Document "${ACTIVE_DOC_ID}" loaded. You may now ask questions.`);

        if (window.innerWidth <= 768) {
            els.sidebar.classList.remove('active');
            els.overlay.classList.remove('active');
        }

    } catch (err) {
        console.error(err);
        els.uploadBtn.innerHTML = "Upload Failed";
        els.uploadBtn.style.background = "#ef4444";
    }
}

async function askQuestion() {
    const text = els.questionInput.value.trim();
    if (!text) return;

    if (!ACTIVE_DOC_ID) {
        appendMsg("Please upload a document first.", 'bot');
        return;
    }

    appendMsg(text, 'user');
    els.questionInput.value = '';

    const loaderId = appendLoader();

    const formData = new FormData();
    formData.append("question", text);

    try {
        const res = await fetch("/ask/", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        document.getElementById(loaderId)?.remove();
        appendMsg(data.response || "No response", 'bot');

    } catch {
        document.getElementById(loaderId)?.remove();
        appendMsg("Connection error.", 'bot');
    }
}

function appendMsg(text, type) {
    const div = document.createElement('div');
    div.className = `msg-row ${type === 'user' ? 'user-row' : 'bot-row'}`;
    div.innerHTML = `<div class="msg-bubble">${text}</div>`;
    els.chatBox.appendChild(div);
    els.chatBox.scrollTop = els.chatBox.scrollHeight;
}

function appendLoader() {
    const id = 'loader-' + Date.now();
    const div = document.createElement('div');
    div.className = 'msg-row bot-row';
    div.id = id;
    div.innerHTML = `<div class="msg-bubble"><span class="typing">•••</span></div>`;
    els.chatBox.appendChild(div);
    return id;
}

function addSystemMsg(text) {
    const div = document.createElement('div');
    div.className = 'msg-row bot-row';
    div.innerHTML = `<div class="msg-bubble system">${text}</div>`;
    els.chatBox.appendChild(div);
}
// 👇 expose functions used directly in HTML
window.clearChat = clearChat;
window.askQuestion = askQuestion;
window.uploadPDFs = uploadPDFs;
