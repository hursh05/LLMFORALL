# LLMFORALL 🚀  
A Full-Stack Retrieval-Augmented Generation (RAG) Application

LLMFORALL is a production-ready RAG system that allows users to upload documents (PDFs) and ask natural language questions.  
The system retrieves relevant content using vector search and generates accurate answers using a Large Language Model.

---

## 🔥 Features

- 📄 Upload and process multiple PDF documents
- 🔍 Semantic search using vector embeddings
- 🧠 Context-aware question answering (RAG)
- ⚡ FastAPI backend
- ☁️ Pinecone vector database
- 🤖 Cohere embeddings + reranking
- 🧠 Groq LLM for fast inference
- 🧩 Modular & scalable architecture

---

## 🏗️ Tech Stack

### Backend
- **Python 3.11**
- **FastAPI**
- **Cohere API** (Embeddings + Rerank)
- **Pinecone** (Vector Database)
- **Groq API** (LLM inference)
- **Langchain**

### Frontend
- **HTML**
- **CSS**
- **JavaScript (Fetch API)**

---

## 📂 Project Structure

```text
LLMFORALL/
│
├── server/
│   ├── main.py
│   ├── routes/
│   ├── modules/
│   ├── templates/
│   └── static/
│
│
├── .env
├── requirements.txt
├── .gitignore
└── README.md
