import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from groq import Groq

model = SentenceTransformer("all-MiniLM-L6-v2")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("pm-guruji")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# THE grounding constraint — this is what prevents hallucination
SYSTEM_PROMPT = """You answer questions using ONLY the context provided below.
Rules:
- Use only information from the context chunks. Do not use outside knowledge.
- If the context does not contain the answer, say "I couldn't find that in the source."
- Cite the source title in your answer.
- Never invent quotes or facts."""


def answer(question, top_k=5):
    # 1. retrieve
    qvec = model.encode(question).tolist()
    results = index.query(vector=qvec, top_k=top_k, include_metadata=True)

    # 2. build the context block from retrieved chunks, and collect sources
    context = ""
    sources = []
    for m in results["matches"]:
        md = m["metadata"]
        context += f"[Source: {md['title']}]\n{md['text']}\n\n"
        sources.append({"title": md["title"], "score": m["score"], "text": md["text"]})

    # 3. ask Groq to answer using ONLY that context
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return {"text": response.choices[0].message.content, "sources": sources}


if __name__ == "__main__":
    q = "why did uber rides drop, and how was that concluded?"
    print(f"Q: {q}\n")
    print("A:", answer(q)["text"])
