import os
import time
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from chunker import chunk_text

load_dotenv()                       # reads PINECONE_API_KEY from .env

INDEX_NAME = "pm-guruji"
EMBED_DIM = 384                     # must match the embedding model's output

# --- 1. embed the chunks ---
model = SentenceTransformer("all-MiniLM-L6-v2")
with open("test_audio/yt_transcript.txt") as f:
    transcript = f.read()
chunks = chunk_text(transcript)
vectors = model.encode(chunks)
print(f"Embedded {len(chunks)} chunks.")

# --- 2. connect to Pinecone, create the index if it doesn't exist ---
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

if not pc.has_index(INDEX_NAME):
    print(f"Creating index '{INDEX_NAME}'...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=EMBED_DIM,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(INDEX_NAME).status["ready"]:
        time.sleep(1)
    print("Index ready.")
else:
    print(f"Index '{INDEX_NAME}' already exists.")

index = pc.Index(INDEX_NAME)

# --- 3. upsert vectors with metadata (metadata is what makes citations possible) ---
to_upsert = []
for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
    to_upsert.append({
        "id": f"chunk-{i}",
        "values": vec.tolist(),
        "metadata": {
            "text": chunk,
            "source": "youtube:PA-Z__0G8Cs",
            "title": "PM interview: root cause analysis (Uber rides -50%)",
            "chunk_index": i,
        },
    })

index.upsert(vectors=to_upsert)
print(f"Upserted {len(to_upsert)} vectors.")
print("Index stats:", index.describe_index_stats())
