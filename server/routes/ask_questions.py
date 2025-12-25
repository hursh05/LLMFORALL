# server/routes/ask_questions.py

from fastapi import APIRouter, Form, Request
from pinecone import Pinecone
from cohere import Client as CohereClient
from server.modules.llm import generate_answer
import os

router = APIRouter()

co = CohereClient(os.environ["COHERE_API_KEY"])
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(os.environ["PINECONE_INDEX_NAME"])


@router.post("/set_current_doc/")
async def set_current_doc(request: Request, doc_id: str = Form(...)):
    request.session["doc_id"] = doc_id
    return {"active_doc": doc_id}


@router.post("/ask/")
async def ask_question(request: Request, question: str = Form(...)):

    doc_id = request.session.get("doc_id")

    if not doc_id:
        return {"response": "Please upload a document first."}

    query_emb = co.embed(
        texts=[question],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings[0]

    res = index.query(
        vector=query_emb,
        top_k=5,
        include_metadata=True,
        filter={"doc_id": doc_id}
    )

    if not res["matches"]:
        return {"response": "No relevant information found in the document."}

    context = "\n\n".join(m["metadata"]["text"] for m in res["matches"])
    answer = generate_answer(context, question)

    return {"response": answer}
