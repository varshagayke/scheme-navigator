"""Entry point: sets the theme once and builds the top navigation bar."""
import streamlit as st

from style import inject_css

st.set_page_config(page_title="Government Scheme Navigator", page_icon="🇮🇳", layout="wide")
inject_css()

pages = [
    st.Page("views/home.py", title="Home", icon="🏠", default=True),
    st.Page("views/chatbot.py", title="Chatbot", icon="🤖"),
    st.Page("views/find.py", title="Find My Schemes", icon="🔎"),
    st.Page("views/browse.py", title="Browse All Schemes", icon="📚"),
]

st.navigation(pages, position="top").run()
