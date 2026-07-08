# PM Guruji — Vision & Roadmap

> The north star for this project. Build v1 simple; everything below is the end goal.
> Specs may evolve, but the identity does not: **a search engine that lets you ask
> PM podcasts a question instead of listening to hundreds of hours hoping to find the answer.**

---

## 🎯 Vision (north star)
**PM Guruji** — ask any question and get an answer grounded in what real PM podcast hosts,
guests, and interviewers actually said — across podcasts AND free YouTube interviews/
tutorials/guides — with citations back to the exact source, speaker, and timestamp. When
more than one source has something relevant to say, a judge compares candidate answers and
returns the best-grounded one, not a blind mashup. Built free-first (local transcription,
free-tier everything), and built to double as proof I can ship a real production-RAG
pattern, not just a toy demo.

**Principles:**
- **Free to build, free to run** — local Whisper transcription (not paid Deepgram), free-tier
  Pinecone, free LLM (Groq/Llama, same as RoastMyPM). No recurring cost until a phase genuinely needs it.
- **Depth over breadth for v1** — one podcast, indexed well, beats five podcasts indexed badly.
  Breadth (more podcasts, YouTube) comes in later phases, once the core pipeline is proven.
- **Grounded, not generic** — every answer must cite its source episode/speaker. If the
  retrieved chunks don't support an answer, say so — never let the LLM fill gaps from its
  own training data.
- **Multi-source, judged** — once more than one source exists, don't just merge everything
  blindly. Generate a candidate answer per source, then use an LLM-as-judge step to pick
  (or explain) the best-grounded one. Same technique used to grade AI outputs in evals,
  applied live.
- **My own build** — architecture and concepts come from the CuriousPM Podcast Search
  tutorial (Ankit's session); the code is written from scratch, not reused from his repo.
  Same reason RoastMyPM wasn't a fork of the course's chatbot starter.
- **Public demo vs. private use** — the public live link (the portfolio proof) stays scoped
  to copyright-clean sources (podcasts, YouTube). Books Sachin supplies as PDFs are for his
  own private study use and are kept in a separate, non-public data partition — same
  pipeline/code, different data visibility. Decided 2026-07-04: full book text is in scope,
  copyright risk accepted for the private-use path specifically.

---

## 🪜 Capability roadmap (each phase ships; none pivots)

| Phase | Capability | Tools / APIs | Data | New concept |
|------|-----------|--------------|------|-------------|
| **v1** Core Search | ask a question → grounded answer with citations, across one podcast (single-turn Q&A) | local Whisper (transcription) + free embedding model + Pinecone (free tier) + Groq/Llama (synthesis) | Lenny's Podcast, ~100-150 episodes | RAG pipeline: chunk → embed → retrieve → synthesize |
| **v2** Conversational Memory | multi-turn chat — handle follow-ups ("tell me more about that") and questions about the conversation itself, instead of answering each question in isolation | LLM-based **query rewriting** (rewrite a follow-up into a standalone search query using history) + pass conversation history to the answer step | conversation history in session state | query rewriting / conversation-aware RAG; keeps content answers grounded while using history for context |
| **v3** Multi-Source Corpus | expand beyond one podcast — add free YouTube interviews/tutorials/guides AND PDF books (Sachin-supplied) as sources | YouTube caption API (free, when available) + Whisper fallback for uncaptioned videos; PDF text extraction (no transcription needed — books are already text) | chunks tagged with `source_type` (podcast/youtube/book) + source metadata; **books live in a private Pinecone namespace, podcast+YouTube in the public one** | multi-source ingestion, unified schema across source types, public/private data separation |
| **v4** Best-of-N Judge | when multiple sources have relevant content, don't blindly merge — generate a candidate answer per source, judge picks/explains the best | separate LLM-as-judge call scoring candidates on groundedness/completeness | — | LLM-as-judge, applied at query time (ties to Season 2 tutorial #09) |
| **v5** Speaker Attribution | filter/attribute answers by who said it (host vs. guest) | LLM reads episode intro to map "Speaker 1" → real name | speaker-tagged chunks | name resolution from raw diarization |
| **v6** Hybrid Retrieval | more precise results — catches exact terms semantic search misses | keyword re-ranking on top of vector search | — | hybrid search (semantic + keyword) |
| **v7** Episode Summarizer | ask for a full-episode/video summary, not just a targeted answer | same retrieval, different prompt mode | — | prompt-mode branching |
| **v8** MCP Distribution | query PM Guruji directly from Claude Desktop/Cursor, no web UI needed | MCP server exposing a `search_podcast` tool | — | writing an MCP server (ties to Season 2 tutorial #11) |
| **v9** Content Catalog | browse/list episodes/videos properly (not just search) — fixes the Pinecone-can't-list-everything gap | lightweight SQLite catalog alongside Pinecone | content metadata table | vector DB vs. relational DB, used together |
| **v10** Eval Harness | prove retrieval quality doesn't silently degrade when I change chunking/prompts — different from v4's runtime judge, this is regression testing over time | golden set of ~20 Q&A pairs, scored automatically | eval dataset | evals as a regression gate (ties to Season 2 tutorial #09) |

---

## 🔧 Cost reality check (why free-first is possible here)
| Item | Ankit's version (4,700 episodes, 3-day deadline) | PM Guruji v1 (100-150 episodes, no deadline) |
|---|---|---|
| Transcription | Deepgram, ~$1,200 | **Local Whisper, $0** (slower, no time pressure) |
| Always-on server | Fly.io, $10/month | **None needed** — ingestion runs once, locally |
| Vector DB hosting | Pinecone paid, $50/month | **Pinecone free tier** (well within limits at this scale) |
| Per-query synthesis | GPT-4o, ~$0.002/query | **Groq/Llama, free** (same as RoastMyPM) |

---

## 🟢 v1 scope (the first build — simple, a true slice)
- **Source:** Lenny's Podcast only (~100-150 episodes) — via its public RSS feed
- **Transcription:** local Whisper, run once, offline
- **Chunking:** 1,000-character chunks, no overlap (same tradeoff call the tutorial made — general PM advice content, low stakes on a cut sentence)
- **Embedding:** a free local/open embedding model (decide exact one when we get there — options to compare: sentence-transformers vs. a free-tier hosted embedding API)
- **Storage:** Pinecone free tier
- **Retrieval:** top 8-10 chunks by cosine similarity
- **Synthesis:** Groq/Llama, strict system prompt — "only use provided chunks, cite the episode, never invent quotes"
- **UI:** Streamlit (same as RoastMyPM — you already know this stack)
- **Ship:** Streamlit Community Cloud, push-to-deploy

---

## Notes / open items
- Repo: new, `pm-guruji`, own GitHub repo (not a fork of Ankit's course repo).
- Build order & per-project workflow: see `../../portfolio-plan/BUILD_PLAN.md` and `PROGRESS.md`.
- Stay in the build-it-myself model: Claude coaches; Sachin writes & commits each step.
- v1 podcast scope (Lenny's Podcast only) can expand to more PM shows in a later phase once the pipeline works end-to-end.
- **Conversational memory (v2), multi-source + judge (v3/v4) are intentionally NOT in v1** — added to the vision so they're not forgotten, but v1 stays a simple single-source, single-turn slice on purpose. Build the core pipeline first, understand it cold, then add complexity.
- **v2 (Conversational Memory) was added 2026-07-08** after building v1: the single-turn chat couldn't handle follow-ups or "what did I ask earlier?" (it answered each question in isolation, grounded only to transcript chunks). Inserted as the new v2 because it's a distinct capability (query rewriting / conversation-aware RAG) and it's the most immediately-felt gap in a chat UI. Everything after it bumped down one (multi-source is now v3, etc.).
- **v1 status: DONE & verified (2026-07-07/08)** — full RAG pipeline built and tested end-to-end on one YouTube transcript (PM root-cause-analysis video); grounded answers with citations + verified refusal on off-topic questions. Streamlit UI built. See `../../portfolio-plan/PROGRESS.md` Session 4.
