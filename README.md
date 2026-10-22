# AI Government Scheme Navigator

An AI-powered government scheme discovery platform featuring a dashboard, rule-based eligibility finder, and multilingual voice chatbot for **295 Central Government and Maharashtra Government schemes**.

The application helps users discover relevant schemes through Retrieval-Augmented Generation (RAG), search and filtering, eligibility matching, and conversational assistance in **English, Hindi, and Marathi**.

## Features

- **Multilingual AI Chatbot:** Ask questions about government schemes in English, Hindi, or Marathi.
- **Voice Input:** Ask questions using your microphone, with speech converted to text through Gemini.
- **Text-to-Speech:** Listen to chatbot responses in your preferred language using gTTS.
- **RAG-Based Retrieval:** Retrieve relevant schemes from the dataset using TF-IDF similarity.
- **Eligibility Finder:** Match schemes using user details such as age, gender, location, and occupation.
- **Scheme Dashboard:** Browse schemes using filters, visualizations, and scheme cards.
- **Eligibility Explanations:** Understand why a scheme matched the entered profile.
- **Secure API Configuration:** Load the Gemini API key from environment variables.

## Tech Stack

| Component | Technologies |
|---|---|
| Frontend and dashboard | Streamlit |
| Programming language | Python |
| AI and language processing | Google Gemini API |
| Retrieval system | Retrieval-Augmented Generation (RAG), TF-IDF |
| Data processing | Pandas |
| Voice output | gTTS |
| Configuration | python-dotenv |
| Dataset | CSV |

## Project Structure

```text
AI-Government-Scheme-Navigator/
│
├── app.py                  # Main application and navigation
├── style.py                # Styling, cards, and banners
├── data_loader.py          # Dataset loading and preprocessing
├── eligibility.py          # Rule-based eligibility matching
├── rag.py                  # Relevant scheme retrieval
├── llm.py                  # Gemini API integration
├── voice.py                # Text-to-speech functionality
├── i18n.py                 # Multilingual interface text
│
├── views/
│   ├── home.py              # Home page
│   ├── chatbot.py           # Multilingual chatbot
│   ├── find.py               # Eligibility finder
│   └── browse.py             # Scheme dashboard
│
├── data/
│   └── [scheme dataset CSV]
│
├── assets/
│   └── hero.svg              # Home page illustration
│
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration
│
├── requirements.txt          # Python dependencies
├── .gitignore                # Excluded files and secrets
├── .env                      # Local environment variables
└── README.md
```

*Note: The dataset filename and any additional files should match your actual repository structure.*

## Getting Started

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd AI-Government-Scheme-Navigator
```

### 2. Create and activate a virtual environment

If you already have a virtual environment, activate it directly.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own valid API key. Keep this file private and never commit it to GitHub.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL to open the application in your browser.

## Application Pages

| Page | Description |
|---|---|
| **Home** | Introduces the application and provides navigation to its main features. |
| **AI Chatbot** | Answers scheme-related questions using RAG and Gemini, supports voice input, and reads answers aloud. |
| **Find My Schemes** | Matches government schemes to user profiles using predefined eligibility rules. |
| **Browse All Schemes** | Displays the scheme collection through searchable filters, charts, and scheme cards. |

## How the RAG Chatbot Works

The chatbot combines information retrieval with a generative AI model to provide contextual answers about government schemes.

1. **User Input:** The user enters a question by typing or speaking through the microphone.
2. **Speech Recognition:** For voice queries, Gemini converts the spoken question into text.
3. **Language Processing:** Hindi and Marathi queries are converted into English search keywords using Gemini, with a built-in dictionary as a fallback.
4. **Information Retrieval:** `rag.py` uses TF-IDF similarity to retrieve the five most relevant schemes from the dataset.
5. **Answer Generation:** `llm.py` sends the retrieved scheme information and user question to Gemini to generate an answer in the selected language.
6. **Voice Response:** `voice.py` uses gTTS to convert the generated answer into speech.

The retrieved schemes provide the context for answering questions. This helps ground the chatbot's responses in the available dataset rather than relying solely on the language model's general knowledge.

## Eligibility Matching

The eligibility finder uses a **rule-based approach** rather than allowing an AI model to make eligibility decisions.

- Collects user details such as age, gender, location, and occupation.
- Applies predefined hard and soft matching rules.
- Displays potentially relevant schemes with explanations for the matches.
- Presents income requirements and category-specific conditions for users to review.

A match indicates potential eligibility, not guaranteed approval. Users should verify the complete eligibility criteria through the relevant official government portal.

## Environment Variables and API Key Security

The application uses a Gemini API key for AI-powered functionality.

For local development, configure the key in `.env`. For Streamlit Community Cloud, configure it through the application's **Secrets** settings.

Example Streamlit secrets configuration:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
```

Ensure `.env` and `venv/` are included in `.gitignore`. Never publish API keys, credentials, or other secrets in your repository.

**Without a Gemini API key:** Basic scheme retrieval may still work, but AI-generated answers, language conversion, and voice-input features may be unavailable. Exact fallback behavior depends on the implementation.

## Deployment

The application can be deployed using Streamlit Community Cloud.

1. Push the project source code to a GitHub repository.
2. Ensure that `.env`, `venv/`, and other sensitive or unnecessary files are excluded.
3. Open [Streamlit Community Cloud](https://share.streamlit.io/).
4. Create a new app and select your repository and `app.py` as the entry point.
5. Add `GEMINI_API_KEY` under the app's Secrets settings.
6. Deploy the application and test its pages, chatbot, and voice features.

## Limitations

- **Scheme status:** Some schemes in the dataset may not have a confirmed current application status. Users should verify availability through official government websites.
- **Eligibility accuracy:** The finder uses predefined rules and cannot guarantee eligibility or scheme approval.
- **Text-based conditions:** Some income, category, and other eligibility requirements are displayed for manual verification instead of being fully evaluated.
- **AI-generated responses:** Gemini may produce inaccurate or incomplete information. Users should cross-check important details against official sources.
- **Conversation context:** The chatbot handles questions independently and does not retain previous questions as conversational memory.
- **Microphone access:** Voice input generally requires localhost or a secure HTTPS connection and browser microphone permission.
- **Internet dependency:** Gemini requests and gTTS speech generation require internet access.

## Future Enhancements

- Integrate official government sources to improve scheme-status verification.
- Expand automated eligibility evaluation for income and category requirements.
- Add conversational memory for follow-up questions.
- Improve retrieval with semantic embeddings and more advanced ranking.
- Add user feedback and response-quality evaluation.
- Expand support for additional Indian languages.

## Disclaimer

This project is intended to help users discover and understand potentially relevant government schemes. It is an informational tool, not an official government service. Scheme details, application status, and eligibility requirements should always be verified through the appropriate official government portal.

---

**Built with Python, Streamlit, RAG, and Google Gemini.**
