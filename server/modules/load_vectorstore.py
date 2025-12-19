import os
import time
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from cohere import Client as CohereClient
from PyPDF2 import PdfReader

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

co = CohereClient(os.environ["COHERE_API_KEY"])
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

index_name = os.environ["PINECONE_INDEX_NAME"]
dimension = int(os.environ["PINECONE_DIMENSION"])

if index_name not in [i["name"] for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=os.environ["PINECONE_ENV"])
    )
    time.sleep(5)

index = pc.Index(index_name)

def load_vectorstore(files):
    for file in files:
        path = Path(UPLOAD_DIR) / file.filename
        with open(path, "wb") as f:
            f.write(file.file.read())

        reader = PdfReader(path)
        text = "\n".join(page.extract_text() for page in reader.pages)

        chunks = [text[i:i+800] for i in range(0, len(text), 800)]

        embeddings = co.embed(
            texts=chunks,
            model="embed-english-v3.0",
            input_type="search_document"
        ).embeddings

        vectors = [
            (f"{file.filename}-{i}", embeddings[i], {"text": chunks[i]})
            for i in range(len(chunks))
        ]

        index.upsert(vectors=vectors)
        print(f"Uploaded {len(chunks)} chunks for {file.filename}")
