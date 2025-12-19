import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are a helpful AI assistant.
Answer strictly using the context below.

Context:
{context}

Question:
{question}

If the answer is not present, say you don't know.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
