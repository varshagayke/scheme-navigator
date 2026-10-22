"""Look and feel: colours, banners, cards. Every page uses these helpers."""
import base64
import html as htmllib
from pathlib import Path

import streamlit as st

from i18n import LANGS

ASSETS = Path(__file__).parent / "assets"

CATEGORY_ICONS = {
    "Education": "🎓", "Agriculture & Allied": "🌾", "Business & Startup": "💼",
    "Health & Nutrition": "🏥", "Skills & Employment": "🛠️", "Women & Child": "👩‍👧",
    "Pension, Savings & Insurance": "💰", "Housing & Infrastructure": "🏠",
    "Social Welfare": "🤝", "Other": "📌",
}

EN_LABELS = {
    "who": "Who can get it", "benefit": "Benefit", "check": "Conditions to check",
    "window": "Application status", "website": "Official website",
    "more": "More details", "why": "Why it matched",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stMarkdown, button, input, textarea {
    font-family: 'Poppins', 'Noto Sans Devanagari', sans-serif !important;
}
.block-container { padding: 2.6rem 4rem 3rem 4rem; max-width: 100% !important; }
#MainMenu, footer { visibility: hidden; }

/* tricolour strip at the very top */
.stApp::before {
    content: ""; position: fixed; top: 0; left: 0; right: 0; height: 5px; z-index: 999999;
    background: linear-gradient(90deg, #FF9933 0 33.3%, #FFFFFF 33.3% 66.6%, #138808 66.6% 100%);
}

/* ---------- Hero ---------- */
.hero {
    background: linear-gradient(120deg, #0A2A5E 0%, #12468F 55%, #1B6FB5 100%);
    border-radius: 26px; padding: 2.2rem 2.6rem; color: #fff;
    display: flex; align-items: center; justify-content: space-between; gap: 1.5rem;
    box-shadow: 0 14px 34px rgba(10, 42, 94, .28); overflow: hidden; margin-bottom: 1rem;
}
.hero h1 { color: #fff !important; font-size: 2.5rem !important; line-height: 1.25 !important;
           margin: 0 0 .7rem 0 !important; padding: 0 !important; font-weight: 700 !important; }
.hero p { color: #DCE9FF; font-size: 1.12rem; margin: 0 0 1rem 0; line-height: 1.6; }
.hero img { height: 290px; flex-shrink: 0; }
.tag { display: inline-block; background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.35);
       padding: .28rem .85rem; border-radius: 999px; margin: 0 .4rem .4rem 0; font-size: .85rem; }

/* ---------- Small page banner ---------- */
.banner {
    background: linear-gradient(120deg, #0A2A5E 0%, #12468F 70%, #1B6FB5 100%);
    border-radius: 20px; padding: 1.3rem 1.8rem; color: #fff; margin-bottom: 1.2rem;
    box-shadow: 0 8px 22px rgba(10, 42, 94, .22); border-left: 8px solid #FF9933;
}
.banner h1 { color: #fff !important; font-size: 1.8rem !important; margin: 0 !important; padding: 0 !important; font-weight: 700 !important; }
.banner p { color: #DCE9FF; margin: .35rem 0 0 0; font-size: 1rem; }

/* ---------- Section titles ---------- */
.section-title { font-size: 1.45rem; font-weight: 700; color: #0A2A5E; margin: 2rem 0 .8rem 0; }
.section-title::after { content: ""; display: block; width: 56px; height: 4px; border-radius: 2px;
                        background: linear-gradient(90deg, #FF9933, #138808); margin-top: .35rem; }

/* ---------- Stats ---------- */
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.4rem 0 .4rem 0; }
.stat { background: #fff; border-radius: 18px; padding: 1rem; text-align: center;
        box-shadow: 0 6px 18px rgba(20, 40, 80, .08); border-bottom: 4px solid #FF9933; }
.stat b { display: block; font-size: 1.8rem; color: #E8590C; }
.stat span { color: #4A5A73; font-size: .9rem; }

/* ---------- Feature cards ---------- */
.feature-icon { font-size: 2.6rem; line-height: 1; }
.feature-title { font-size: 1.2rem; font-weight: 700; color: #0A2A5E; margin: .5rem 0 .3rem 0; }
.feature-text { color: #4A5A73; font-size: .95rem; min-height: 3.2rem; }

/* ---------- Personas and steps ---------- */
.personas { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: .9rem; }
.persona { background: #fff; border-radius: 16px; padding: 1rem .5rem; text-align: center;
           box-shadow: 0 4px 14px rgba(20, 40, 80, .07); font-weight: 600; color: #1B2A41; }
.persona span { display: block; font-size: 2rem; margin-bottom: .2rem; }
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.step { background: #fff; border-radius: 16px; padding: 1.1rem; box-shadow: 0 4px 14px rgba(20, 40, 80, .07);
        text-align: center; color: #1B2A41; font-weight: 500; }
.step-num { width: 40px; height: 40px; border-radius: 50%; margin: 0 auto .6rem auto; color: #fff; font-weight: 700;
            background: linear-gradient(135deg, #FF9933, #E8590C); display: flex; align-items: center; justify-content: center; }
.note { background: #FFF4E6; border-left: 6px solid #FF9933; border-radius: 12px; padding: .9rem 1.1rem;
        color: #5B3A00; margin-top: 1.6rem; }

/* ---------- Scheme cards ---------- */
.card-title { font-size: 1.1rem; font-weight: 700; color: #0A2A5E; margin-bottom: .35rem; }
.chip { display: inline-block; padding: .15rem .7rem; border-radius: 999px; font-size: .78rem; font-weight: 600; margin-right: .4rem; }
.chip-cat { background: #E7F1FF; color: #12468F; }
.chip-lvl { background: #E6F6E6; color: #0B6B0B; }
.chip-why { background: #FFF1DD; color: #9A4A00; }
.card-line { margin: .35rem 0; color: #243247; }

[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 18px; background: #fff;
    box-shadow: 0 6px 18px rgba(20, 40, 80, .07); }

/* ---------- Buttons ---------- */
.stButton > button, .stLinkButton > a, [data-testid="stPageLink-NavLink"] {
    border-radius: 12px !important; font-weight: 600 !important;
}
[data-testid="stPageLink-NavLink"] { background: #FF9933; color: #fff !important; justify-content: center;
    padding: .55rem 1rem; box-shadow: 0 4px 12px rgba(232, 89, 12, .3); }
[data-testid="stPageLink-NavLink"] p { color: #fff !important; font-weight: 600; }
[data-testid="stPageLink-NavLink"]:hover { background: #E8590C; }

/* ---------- Chat look ---------- */
[data-testid="stChatMessage"] { border-radius: 20px; padding: 1rem 1.2rem; margin-bottom: .9rem;
    box-shadow: 0 3px 12px rgba(20, 40, 80, .07); }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background: #E4EEFF; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) { background: #FFF6E9; border: 1px solid #FFDDB0; }
[data-testid="stChatInput"] { border-radius: 18px; border: 2px solid #FF9933; }

/* ---------- Mobile ---------- */
@media (max-width: 800px) {
    .block-container { padding: 2.4rem 1rem 2rem 1rem; }
    .hero { flex-direction: column-reverse; text-align: center; padding: 1.5rem; }
    .hero h1 { font-size: 1.7rem !important; }
    .hero img { height: 170px; }
    .stats, .personas, .steps { grid-template-columns: repeat(2, 1fr); }
}
"""


def inject_css():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def render_html(text):
    """Show HTML. Lines are joined so Markdown does not treat indentation as code."""
    st.markdown(" ".join(line.strip() for line in text.strip().splitlines()), unsafe_allow_html=True)


def esc(value):
    return htmllib.escape(str(value))


def image_uri(name):
    data = (ASSETS / name).read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(data).decode()


def banner(title, subtitle=""):
    render_html(f'<div class="banner"><h1>{esc(title)}</h1><p>{esc(subtitle)}</p></div>')


def section_title(text):
    render_html(f'<div class="section-title">{esc(text)}</div>')


def language_picker():
    """One shared language choice, remembered while the user moves between pages."""
    labels = list(LANGS)
    if "lang_choice" not in st.session_state:
        st.session_state["lang_choice"] = st.session_state.get("lang_saved", labels[0])
    choice = st.radio("🌐 भाषा / Language", labels, horizontal=True, key="lang_choice")
    st.session_state["lang_saved"] = choice
    return LANGS[choice]


def scheme_card(row, key, reasons=None, labels=None):
    """One scheme as a clean card, with details inside a small expander."""
    L = labels or EN_LABELS
    icon = CATEGORY_ICONS.get(row["category_group"], "📌")
    with st.container(border=True):
        chips = (f'<span class="chip chip-cat">{esc(row["category_group"])}</span>'
                 f'<span class="chip chip-lvl">{esc(row["government_level"])}</span>')
        render_html(f'<div class="card-title">{icon} {esc(row["scheme_name"])}</div>{chips}')
        render_html(f'<div class="card-line"><b>{esc(L["benefit"])}:</b> {esc(row["benefit"])}</div>')
        render_html(f'<div class="card-line"><b>{esc(L["who"])}:</b> {esc(row["target_beneficiary"])}</div>')
        if reasons:
            render_html(f'<span class="chip chip-why">✅ {esc(L["why"])}: {esc("; ".join(reasons))}</span>')
        with st.expander(L["more"]):
            st.write(row["scheme_description"])
            st.markdown(f"**{L['check']}:** {row['income_or_eligibility_condition']}")
            st.markdown(f"**{L['window']}:** {row['application_window_status']}")
            st.link_button(f"🔗 {L['website']}", row["application_url"], key=f"lnk_{key}")
