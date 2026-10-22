"""Text to speech: the app reads the answer aloud (English, Hindi or Marathi)."""
import io
import re

from gtts import gTTS


def clean_for_speech(text):
    text = re.sub(r"https?://\S+", "", text)          # do not read web links aloud
    text = re.sub(r"[*#_`>|]", "", text)               # remove markdown symbols
    text = re.sub(r"\s*\n\s*", ". ", text)             # new lines become pauses
    return re.sub(r"\s+", " ", text).strip()


def speak(text, lang_code, max_chars=900):
    """Return mp3 bytes. Needs internet (uses Google's free text-to-speech)."""
    text = clean_for_speech(text)[:max_chars]
    buffer = io.BytesIO()
    tld = "co.in" if lang_code == "en" else "com"      # Indian English accent
    gTTS(text=text, lang=lang_code, tld=tld).write_to_fp(buffer)
    return buffer.getvalue()
