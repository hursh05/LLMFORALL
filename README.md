# LLMFORALL 🚀  
### A Full-Stack Document-Aware Retrieval-Augmented Generation (RAG) System

LLMFORALL is a **production-ready, document-scoped RAG application** that allows users to upload PDF documents and ask natural language questions.

Each query is answered **strictly from the currently uploaded document only**, ensuring **zero context leakage** across documents or user sessions.

---

## 🔥 Key Features

- 📄 Upload one or multiple PDF documents  
- 🧠 **Document-scoped Question Answering** (No cross-document answers)  
- 🔍 Semantic search using vector embeddings  
- 🎯 Accurate, context-aware responses via RAG  
- ⚡ FastAPI backend  
- ☁️ Pinecone vector database  
- 🧩 Modular, scalable backend architecture  
- 🌐 Clean frontend with real-time interaction  

---

## 🧠 Core RAG Logic (Important)

LLMFORALL **strictly answers questions ONLY from the selected document**.

### How It Works

1. Each uploaded document is assigned a unique `doc_id`
2. All text chunks are stored in Pinecone with metadata:

```json
{
  "text": "...",
  "doc_id": "blood_cancer"
}
Runtime Flow
When a document is uploaded:

That document becomes the active context

When a question is asked:

Pinecone is queried only with the active doc_id

No vectors from other documents are retrieved

The LLM:

Receives only retrieved document chunks

Is explicitly instructed not to hallucinate or use external knowledge

✅ Result
If the question is not related to the uploaded document, the system correctly responds:

"No relevant information found in the document."

🏗️ Tech Stack
Backend
Python 3.11

FastAPI

Cohere API – Embeddings

Pinecone – Vector Database

Groq API – LLM Inference

PyPDF2 – PDF Parsing

Frontend
HTML

CSS

JavaScript (Fetch API)

📂 Project Structure
text
Copy code
LLMFORALL/
│
├── server/
│   ├── main.py                  # FastAPI app entry point
│   ├── routes/
│   │   ├── upload_pdfs.py        # PDF upload endpoint
│   │   └── ask_questions.py      # Question answering endpoint
│   │
│   ├── modules/
│   │   ├── load_vectorstore.py   # PDF → chunks → embeddings → Pinecone
│   │   ├── llm.py                # LLM prompt + response logic
│   │   └── query_handlers.py     # Vector search helpers
│   │
│   ├── templates/
│   │   └── index.html            # Frontend UI
│   │
│   └── static/
│       ├── style.css
│       └── script.js
│
├── .env
├── requirements.txt
├── .gitignore
└── README.md
🚀 How to Run Locally
1️⃣ Clone the Repository
bash
Copy code
git clone https://github.com/your-username/LLMFORALL.git
cd LLMFORALL
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Configure Environment Variables
Create a .env file:

env
Copy code
COHERE_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_INDEX_NAME=llmforall
PINECONE_DIMENSION=1024
PINECONE_ENV=aws-region
UPLOAD_DIR=uploaded_docs
5️⃣ Run the Server
bash
Copy code
uvicorn server.main:app --reload
Open your browser →
👉 http://127.0.0.1:8000

🧪 Example Behavior
Scenario	Result
Ask diabetes question on blood cancer PDF	❌ Correctly says Not Found
Upload second PDF in another session	✅ No cross-document leakage
Multiple users	✅ Session-safe
Hallucination	❌ Prevented

🛡️ Design Principles
❌ No global memory

❌ No cross-document leakage

❌ No external knowledge injection

✅ Deterministic, document-grounded answers

✅ Production-safe RAG architecture

📌 Use Cases
Medical document Q&A

Legal document analysis

Financial reports

Enterprise knowledge assistants

Internal documentation bots

👨‍💻 Author
Hursh Karnik
AI / Backend Engineer
