import streamlit as st
from answer import answer

st.set_page_config(page_title="PM Guruji", page_icon="🎙️")
st.title("🎙️ PM Guruji")
st.caption("Ask a PM question — answered only from indexed content, with sources. No made-up answers.")

# conversation memory (same idea as RoastMyPM: a list in session_state)
if "messages" not in st.session_state:
    st.session_state.messages = []

# replay the conversation so far
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# handle a new question
if prompt := st.chat_input("Ask about PM topics from the indexed content..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching the sources..."):
            result = answer(prompt)
        st.markdown(result["text"])

        # show the retrieved chunks — this is what proves the answer is grounded
        with st.expander(f"📚 Sources used ({len(result['sources'])})"):
            for s in result["sources"]:
                st.markdown(f"**{s['title']}** · similarity {s['score']:.2f}")
                st.caption(s["text"][:300] + "...")

    st.session_state.messages.append({"role": "assistant", "content": result["text"]})
