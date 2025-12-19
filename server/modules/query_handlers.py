import os
from pinecone import Pinecone
from cohere import Client as CohereClient

co = CohereClient(os.environ["COHERE_API_KEY"])
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(os.environ["PINECONE_INDEX_NAME"])


def search_similar_docs(query: str, top_k: int = 5):
    query_embedding = co.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings[0]

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    docs = []
    for match in results["matches"]:
        docs.append({
            "text": match["metadata"]["text"],
            "score": match["score"]
        })

    return docs
