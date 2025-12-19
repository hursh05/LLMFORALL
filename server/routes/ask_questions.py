from fastapi import APIRouter, Form
from server.modules.llm import generate_answer
from server.modules.query_handlers import search_similar_docs
from server.logger import logger
from fastapi import APIRouter, Form
from pinecone import Pinecone
from cohere import Client as CohereClient
import os
router = APIRouter()

co = CohereClient(os.environ["COHERE_API_KEY"])
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(os.environ["PINECONE_INDEX_NAME"])

@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    query_emb = co.embed(
        texts=[question],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings[0]

    res = index.query(vector=query_emb, top_k=5, include_metadata=True)

    docs = [m["metadata"]["text"] for m in res["matches"]]
    context = "\n\n".join(docs)

    answer = generate_answer(context, question)

    return {"response": answer}