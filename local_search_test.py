from sentence_transformers import SentenceTransformer, util
from chunk_test import chunk_text

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("test_audio/yt_transcript.txt") as f:
    transcript = f.read()

chunks = chunk_text(transcript)
chunk_vectors = model.encode(chunks)

question = "why did uber rides drop?"
question_vector = model.encode(question)

# cosine similarity between the question and every chunk
scores = util.cos_sim(question_vector, chunk_vectors)[0]

# rank chunks by score, highest first
ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

print(f"QUESTION: {question}\n")
print("TOP 4 MATCHING CHUNKS:\n")
for rank, (idx, score) in enumerate(ranked[:4], start=1):
    print(f"#{rank}  chunk {idx}  (score {score:.3f})")
    print(f"    {chunks[idx][:180]}...")
    print()
