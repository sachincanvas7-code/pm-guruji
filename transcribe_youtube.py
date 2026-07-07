from faster_whisper import WhisperModel

# medium model, already cached; int8 is the fast CPU compute mode
model = WhisperModel("medium", device="cpu", compute_type="int8")

# task="translate" -> outputs English text even though the audio is Hindi
segments, info = model.transcribe("test_audio/yt_video.mp3", task="translate")

print(f"Detected language: {info.language} (prob {info.language_probability:.2f})")

full_text = ""
for seg in segments:
    full_text += seg.text.strip() + " "
    print(f"[{seg.start:.0f}s] {seg.text.strip()}")

with open("test_audio/yt_transcript.txt", "w") as f:
    f.write(full_text.strip())

print(f"\n--- DONE. {len(full_text)} chars saved to test_audio/yt_transcript.txt ---")
