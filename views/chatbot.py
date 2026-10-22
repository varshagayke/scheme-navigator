import hashlib

import streamlit as st

import llm
import voice
from data_loader import get_schemes
from i18n import T
from rag import SchemeRetriever, add_english_keywords, build_context
from style import banner, language_picker, scheme_card


@st.cache_resource
def get_retriever():
    return SchemeRetriever(get_schemes())


retriever = get_retriever()

# ---------- Language first, so anyone can choose ----------
code = language_picker()
t = T[code]
banner(t["title"], t["subtitle"])

# ---------- API key: read from .env / secrets, or ask only if missing ----------
api_key = llm.default_api_key()
if not api_key:
    with st.expander("🔑 Gemini API key"):
        api_key = st.text_input("Gemini API key", type="password", help="Free key from aistudio.google.com")
client = llm.get_client(api_key) if api_key else None
if client is None:
    st.info(t["need_key"])

# ---------- Session memory ----------
st.session_state.setdefault("messages", [])
st.session_state.setdefault("tts", {})
st.session_state.setdefault("last_audio", None)
st.session_state.setdefault("autoplay_idx", None)


# ---------- The RAG pipeline ----------
def offline_answer(rows):
    """Used when there is no API key: simple list of what we found."""
    if not rows:
        return t["not_found"]
    lines = [t["found"], ""]
    for row, _ in rows[:3]:
        lines.append(f"- **{row['scheme_name']}** — {t['benefit']}: {row['benefit']}")
    lines += ["", t["disclaimer"]]
    return "\n".join(lines)


def handle_question(question, speak_auto):
    st.session_state.messages.append({"role": "user", "content": question})

    # 1) Make an English search query from the user's words
    english_query = add_english_keywords(question)
    if client:
        try:
            english_query = llm.to_english_query(client, question) + " " + english_query
        except Exception:
            pass

    # 2) RETRIEVE the best matching schemes
    rows = retriever.search(english_query, k=5)

    # 3) GENERATE the answer in the user's language
    if not rows:
        reply = t["not_found"]
    elif client:
        try:
            reply = llm.answer(client, question, build_context(rows), code)
        except Exception:
            st.warning(t["error"])
            reply = offline_answer(rows)
    else:
        reply = offline_answer(rows)

    sources = [int(row.name) for row, _ in rows[:3]]
    st.session_state.messages.append({"role": "assistant", "content": reply, "sources": sources})

    # 4) SPEAK the answer
    if speak_auto and rows:
        idx = len(st.session_state.messages) - 1
        try:
            st.session_state.tts[idx] = voice.speak(reply, code)
            st.session_state.autoplay_idx = idx
        except Exception:
            pass


# ---------- Input area: microphone card + typed chat box ----------
question = st.chat_input(t["placeholder"])

left, right = st.columns([1, 1])
with left:
    with st.container(border=True):
        st.markdown(f"### {t['mic_title']}")
        st.caption(t["mic_hint"])
        audio = st.audio_input(t["mic_title"], label_visibility="collapsed")
        if audio is not None:
            audio_bytes = audio.getvalue()
            audio_id = hashlib.md5(audio_bytes).hexdigest()
            if audio_id != st.session_state.last_audio:      # process each recording once
                st.session_state.last_audio = audio_id
                if client is None:
                    st.warning(t["need_key"])
                else:
                    try:
                        with st.spinner(t["thinking"]):
                            question = llm.transcribe(client, audio_bytes, code)
                    except Exception as e:
                        st.error(f"{t['error']} ({e})")

with right:
    with st.container(border=True):
        st.markdown(f"### 💡 {t['examples_title']}")
        for n, example in enumerate(t["examples"]):
            if st.button(example, use_container_width=True, key=f"ex_{n}"):
                question = example

o1, o2 = st.columns([3, 1])
speak_auto = o1.toggle("🔊 " + t["speak_auto"], value=True)
if o2.button("🗑️ " + t["clear"], use_container_width=True):
    st.session_state.messages = []
    st.session_state.tts = {}
    st.rerun()

if question:
    with st.spinner(t["thinking"]):
        handle_question(question, speak_auto)

# ---------- Conversation ----------
for i, msg in enumerate(st.session_state.messages):
    avatar = "🤖" if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] != "assistant":
            continue

        if st.button(t["listen"], key=f"listen_{i}"):
            try:
                st.session_state.tts[i] = voice.speak(msg["content"], code)
                st.session_state.autoplay_idx = i
            except Exception as e:
                st.error(f"Text-to-speech failed: {e}")
        if i in st.session_state.tts:
            st.audio(st.session_state.tts[i], format="audio/mp3",
                     autoplay=(st.session_state.autoplay_idx == i))

        if msg.get("sources"):
            with st.expander("📋 " + t["sources"]):
                labels = {"who": t["who"], "benefit": t["benefit"], "check": t["check"],
                          "window": t["window"], "website": t["website"],
                          "more": t["sources"], "why": ""}
                for pos in msg["sources"]:
                    row = retriever.df.iloc[pos]
                    scheme_card(row, key=f"chat_{i}_{pos}", labels=labels)

st.session_state.autoplay_idx = None   # play the sound only once
