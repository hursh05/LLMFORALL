import os
from dotenv import load_dotenv
import cohere

load_dotenv()

co = cohere.Client(os.environ["COHERE_API_KEY"])

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are a helpful AI assistant.
Answer strictly using the context below.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say "I don't know based on the provided document."
"""

    response = co.chat(
        model="command-a-03-2025", 
        message=prompt,
        temperature=0.2,
    )

    return response.text
