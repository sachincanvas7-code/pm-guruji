def chunk_text(text, chunk_size=1000):
    words = text.split()          # split the blob into individual words
    chunks = []
    current = ""
    for word in words:
        # if adding this word would push us over the limit, close the chunk
        if len(current) + len(word) + 1 > chunk_size:
            chunks.append(current.strip())
            current = word        # start a fresh chunk with this word
        else:
            current += " " + word # otherwise keep adding to the current chunk
    if current.strip():           # don't forget the last, partial chunk
        chunks.append(current.strip())
    return chunks


with open("test_audio/yt_transcript.txt") as f:
    transcript = f.read()

chunks = chunk_text(transcript)

print(f"Total characters: {len(transcript)}")
print(f"Number of chunks: {len(chunks)}")
print(f"Chunk sizes: {[len(c) for c in chunks]}")
print("\n--- CHUNK 0 ---")
print(chunks[0])
print("\n--- CHUNK 1 ---")
print(chunks[1])
