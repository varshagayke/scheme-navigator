"""RETRIEVAL part of RAG: find the schemes most related to the user's question.
We use TF-IDF (a classic NLP method): words that are rare but present in a scheme
get a high score. Hindi/Marathi questions are first converted to English keywords."""

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Words that appear in every scheme or every question, so they do not help to find the right one
EXTRA_STOP_WORDS = ["scheme", "schemes", "yojana", "programme", "program", "government",
                    "get", "want", "need", "help", "please", "tell", "know", "kind"]
STOP_WORDS = list(ENGLISH_STOP_WORDS) + EXTRA_STOP_WORDS

# English word -> Hindi / Marathi words people commonly use.
# This is the offline fallback. With a Gemini key, the LLM translates instead.
KEYWORDS = {
    "farmer": ["किसान", "शेतकरी", "शेतकर्‍"],
    "agriculture farming": ["खेती", "शेती", "कृषी"],
    "loan credit": ["कर्ज", "लोन", "ऋण", "कर्ज़"],
    "student": ["विद्यार्थी", "विद्यार्थिनी", "छात्र", "छात्रा"],
    "scholarship": ["छात्रवृत्ति", "छात्रवृत्ती", "शिष्यवृत्ती", "शिष्यवृत्ति", "स्कॉलरशिप"],
    "education": ["शिक्षण", "शिक्षा"],
    "women": ["महिला", "स्त्री", "महिलां", "औरत"],
    "girl": ["मुलगी", "मुलींसाठी", "लड़की", "लड़कियों", "बेटी", "कन्या"],
    "pension": ["पेन्शन", "पेंशन", "निवृत्तीवेतन"],
    "senior citizen old age": ["वृद्ध", "ज्येष्ठ", "बुजुर्ग", "बुज़ुर्ग", "वरिष्ठ", "वयोवृद्ध"],
    "disability disabled": ["दिव्यांग", "अपंग", "विकलांग"],
    "housing house": ["घरकुल", "आवास", "मकान", "घर"],
    "health medical treatment": ["आरोग्य", "स्वास्थ्य", "इलाज", "उपचार", "हॉस्पिटल", "अस्पताल"],
    "insurance": ["विमा", "बीमा"],
    "business entrepreneur": ["व्यवसाय", "व्यापार", "उद्योग", "धंदा", "धंधा"],
    "startup": ["स्टार्टअप"],
    "employment job": ["नोकरी", "रोजगार", "नौकरी"],
    "skill training": ["कौशल्य", "कौशल", "प्रशिक्षण"],
    "youth": ["युवा", "तरुण", "युवक"],
    "unemployed": ["बेरोजगार", "बेकार"],
    "worker labour": ["मजूर", "मजदूर", "कामगार", "श्रमिक"],
    "widow": ["विधवा"],
    "pregnant maternity": ["गर्भवती", "प्रसूती", "मातृत्व"],
    "child children": ["बालक", "बच्चा", "बच्चे", "मुलांसाठी", "मुले"],
    "electricity solar": ["वीज", "बिजली", "सौर", "सोलर"],
    "water irrigation": ["पाणी", "पानी", "सिंचन", "सिंचाई"],
    "toilet sanitation": ["शौचालय", "स्वच्छता"],
    "gas cooking LPG": ["गॅस", "गैस", "सिलेंडर", "सिलिंडर"],
    "fisheries fisher": ["मच्छीमार", "मछुआरा", "मत्स्य", "मछली"],
    "dairy animal livestock": ["पशुपालन", "डेअरी", "दूध", "पशु", "जनावर"],
    "tribal": ["आदिवासी"],
    "minority": ["अल्पसंख्याक", "अल्पसंख्यक"],
    "free": ["मोफत", "मुफ्त", "निःशुल्क"],
    "savings": ["बचत"],
    "subsidy grant": ["अनुदान", "सब्सिडी"],
    "tractor machinery": ["ट्रॅक्टर", "ट्रैक्टर", "यंत्र"],
    "crop insurance": ["पीक", "फसल"],
    "bank account": ["बँक", "बैंक", "खाते", "खाता"],
    "marriage wedding": ["विवाह", "लग्न", "शादी"],
    "food ration": ["अन्न", "राशन", "धान्य", "अनाज"],
}


# Same idea for English: add related words so "loan" also finds "credit" schemes
ENGLISH_RELATED = {
    "loan": "credit", "farmer": "agriculture kisan", "old": "senior citizen elderly",
    "girl": "women", "widow": "women pension", "jobless": "unemployed employment",
    "house": "housing awas", "business": "entrepreneur msme", "disabled": "disability divyang",
}


def add_english_keywords(text):
    """Offline translation: if a Hindi/Marathi word is in the text, add its English meaning."""
    extra = []
    for english, native_words in KEYWORDS.items():
        if any(w in text for w in native_words):
            extra.append(english)
    lower = text.lower()
    extra += [related for word, related in ENGLISH_RELATED.items() if word in lower]
    return (text + " " + " ".join(extra)).strip()


class SchemeRetriever:
    def __init__(self, df):
        self.df = df.reset_index(drop=True)
        docs = (
            (self.df["scheme_name"] + " ") * 2          # name counts double
            + self.df["category"] + " "
            + self.df["occupation_or_profile"] + " "
            + self.df["target_beneficiary"] + " "
            + self.df["benefit"] + " "
            + self.df["scheme_description"]
        )
        self.vectorizer = TfidfVectorizer(
            stop_words=STOP_WORDS, ngram_range=(1, 2), sublinear_tf=True
        )
        self.matrix = self.vectorizer.fit_transform(docs.str.lower())

    def search(self, query, k=5):
        """Return the k best matching rows as a list of (row, score)."""
        vec = self.vectorizer.transform([query.lower()])
        scores = cosine_similarity(vec, self.matrix).ravel()
        best = scores.argsort()[::-1][:k]
        return [(self.df.iloc[i], float(scores[i])) for i in best if scores[i] > 0]


def build_context(rows):
    """Turn retrieved rows into text that we give to the LLM (the 'augmented' part)."""
    parts = []
    for n, (row, _) in enumerate(rows, 1):
        parts.append(
            f"[{n}] {row['scheme_name']} ({row['government_level']})\n"
            f"  What: {row['scheme_description']}\n"
            f"  Who: {row['target_beneficiary']}\n"
            f"  Benefit: {row['benefit']}\n"
            f"  Conditions: {row['income_or_eligibility_condition']}\n"
            f"  Application status: {row['application_window_status']}\n"
            f"  Website: {row['application_url']}"
        )
    return "\n\n".join(parts)
