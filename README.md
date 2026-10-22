# AI Government Scheme Navigator

Dashboard + eligibility finder + multilingual voice chatbot (English / Hindi / Marathi)
over 295 Central and Maharashtra government schemes.

## Run it (you already have the venv)
```
venv\Scripts\activate
python -m pip install -r requirements.txt      # new libraries were added
python -m streamlit run app.py
```

## Gemini key (needed for smart answers + voice input)
The key is already inside the `.env` file, so the chatbot loads it automatically.
Never upload `.env` to GitHub (the `.gitignore` file already blocks it). To change the key, edit `.env`.

Without a key the chatbot still works in basic mode (finds schemes, no translation of answers, no voice input).
Spoken answers use gTTS and need internet only.

## Pages
| Page | What it does |
|---|---|
| Home (views/home.py) | What the site is about, 3-language text, buttons to every section |
| Chatbot (views/chatbot.py) | RAG chatbot, type or speak, answers in the chosen language, reads answers aloud |
| Find My Schemes (views/find.py) | Form (age, gender, area, occupation) -> rule-based eligibility, with "why it matched" |
| Browse All Schemes (views/browse.py) | Dashboard: filters, charts, scheme cards |

## How the chatbot works (RAG)
1. **Input**: typed text, or voice (`st.audio_input`) -> Gemini converts speech to text.
2. **Understand**: Hindi/Marathi question -> English search keywords (Gemini, with a built-in word dictionary as backup).
3. **Retrieve** (`rag.py`): TF-IDF finds the 5 most related schemes in the CSV.
4. **Generate** (`llm.py`): Gemini writes a simple answer in the user's language, using ONLY those 5 schemes.
5. **Speak** (`voice.py`): gTTS reads the answer aloud in Hindi / Marathi / English.

## Files
- `app.py` theme + top navigation, `style.py` colours/cards/banners, `assets/hero.svg` home image, `.streamlit/config.toml` theme colours
- `data_loader.py` cleans the CSV (category groups, age limits)
- `eligibility.py` hard rules + soft rules (no AI decides eligibility)
- `rag.py` retrieval, `llm.py` Gemini calls, `voice.py` text-to-speech, `i18n.py` 3-language screen text

## Deploy (Streamlit Community Cloud)
1. Upload the project folder to a GitHub repo (do NOT upload `.env` or `venv`; `.gitignore` handles this).
2. On share.streamlit.io choose the repo and `app.py`.
3. In Advanced settings -> Secrets add: `GEMINI_API_KEY = "your_key"`.

## Known limits (say these in your viva)
- The dataset says many schemes are "not confirmed open", so the app always asks users to verify on the official site.
- Income and category conditions are text, so the app shows them to the user instead of deciding them.
- The chatbot answers one question at a time (no memory of earlier questions).
- Microphone works on localhost and on https sites only.
