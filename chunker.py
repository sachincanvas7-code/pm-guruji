def chunk_text(text, chunk_size=1000):
    """Split text into ~chunk_size pieces, never cutting a word in half."""
    words = text.split()
    chunks = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > chunk_size:
            chunks.append(current.strip())
            current = word
        else:
            current += " " + word
    if current.strip():
        chunks.append(current.strip())
    return chunks
