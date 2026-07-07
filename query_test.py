import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("pm-guruji")

question = "why did uber rides drop?"
question_vector = model.encode(question).tolist()

# ask Pinecone for the top 4 closest chunks, and include their metadata
results = index.query(
    vector=question_vector,
    top_k=4,
    include_metadata=True,
)

print(f"QUESTION: {question}\n")
for rank, match in enumerate(results["matches"], start=1):
    md = match["metadata"]
    print(f"#{rank}  {match['id']}  (score {match['score']:.3f})  [{md['title']}]")
    print(f"    {md['text'][:160]}...")
    print()
