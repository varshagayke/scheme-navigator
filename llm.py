"""GENERATION part of RAG + speech-to-text, using Google Gemini (free API key)."""
import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from i18n import LANG_NAMES

load_dotenv()

# First model is tried first. If it fails (limit / name changed), the next one is tried.
MODELS = [m for m in [os.getenv("GEMINI_MODEL"), "gemini-flash-latest", "gemini-2.5-flash",
                      "gemini-flash-lite-latest", "gemini-2.5-flash-lite"] if m]


def default_api_key():
    """Look for the key in Streamlit secrets (deployment) or in the .env file / environment."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "")


@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


def _generate(client, contents, system=None, temperature=0.2):
    last_error = None
    for model in MODELS:
        for attempt in range(2):                 # try each model twice
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(system_instruction=system, temperature=temperature),
                )
                if response.text:
                    return response.text.strip()
                break                            # empty answer: go to the next model
            except Exception as e:
                last_error = e
                busy = any(code in str(e) for code in ("503", "429", "UNAVAILABLE"))
                if busy and attempt == 0:
                    time.sleep(2)                # server is busy: wait 2 seconds, retry same model
                    continue
                break                            # other error (for example a retired model): next model
    raise RuntimeError(f"Gemini failed: {last_error}")


def to_english_query(client, text):
    """Translate a Hindi / Marathi / English question into short English search keywords."""
    prompt = (
        "Convert this question about Indian government schemes into 5-10 English search keywords "
        "(who the person is, what they need). Output only the keywords.\n\nQuestion: " + text
    )
    return _generate(client, prompt, temperature=0)


def answer(client, question, context, lang_code):
    language = LANG_NAMES[lang_code]
    system = (
        "You are a helpful assistant that explains Indian government schemes to citizens, "
        "many of whom have little education.\n"
        "Rules:\n"
        "- Use ONLY the schemes in CONTEXT. Never invent schemes, amounts, dates or rules.\n"
        "- If CONTEXT has no suitable scheme, say so politely and suggest asking in other words.\n"
        f"- Reply fully in {language}. Use very simple, short sentences and everyday words.\n"
        "- Recommend at most 3 schemes. For each one: the name, the benefit, who can get it, "
        "and the official website link.\n"
        "- Tell the user to confirm on the official website because application dates change.\n"
        "- No tables. Short bullet points are fine."
    )
    contents = f"CONTEXT:\n{context}\n\nUSER QUESTION: {question}"
    return _generate(client, contents, system=system)


def transcribe(client, audio_bytes, lang_code):
    """Speech to text. Gemini listens to the audio and writes what was said."""
    hint = LANG_NAMES[lang_code]
    prompt = (
        f"Transcribe this audio exactly. The speaker most likely speaks {hint}, "
        "but it may be Hindi, Marathi or English. Write Hindi and Marathi in Devanagari script. "
        "Output only the transcript, nothing else."
    )
    part = types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
    return _generate(client, [prompt, part], temperature=0)
