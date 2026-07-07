from sentence_transformers import SentenceTransformer
from chunk_test import chunk_text

# load the free local embedding model (downloads ~80MB the first time)
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("test_audio/yt_transcript.txt") as f:
    transcript = f.read()

chunks = chunk_text(transcript)

# turn all 18 chunks into vectors
vectors = model.encode(chunks)

print(f"Number of chunks: {len(chunks)}")
print(f"Shape of the vectors: {vectors.shape}")   # (num_chunks, dimensions)
print(f"Each vector has {len(vectors[0])} numbers")
print(f"\nFirst 8 numbers of chunk 0's vector:")
print(vectors[0][:8])
