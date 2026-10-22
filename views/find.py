import streamlit as st

from data_loader import get_schemes
from eligibility import OCCUPATION_WORDS, find_schemes
from style import banner, scheme_card

df = get_schemes()

banner("🔎 Find schemes for me", "Answer a few questions. We show schemes you may be eligible for.")

with st.container(border=True):
    with st.form("person_form", border=False):
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Your age", min_value=1, max_value=100, value=25)
        gender = c2.selectbox("Gender", ["Female", "Male", "Other"])
        area = c3.selectbox("Where do you live?", ["Rural (village)", "Urban (city)"])

        c4, c5 = st.columns(2)
        occupation = c4.selectbox("What describes you best?", list(OCCUPATION_WORDS.keys()))
        maharashtra = c5.radio("Do you live in Maharashtra?", ["Yes", "No"], horizontal=True)

        submitted = st.form_submit_button("🔎 Find my schemes", type="primary")

if submitted:
    person = {
        "age": age,
        "gender": gender,
        "area": "Rural" if area.startswith("Rural") else "Urban",
        "occupation": occupation,
        "maharashtra": maharashtra == "Yes",
    }
    best, general = find_schemes(df, person)

    st.success(f"Found {len(best)} schemes made for you and {len(general)} open to everyone.")
    st.warning("Final eligibility (income, documents, category) is decided by the government. "
               "Check conditions and the official website before applying.")

    tab1, tab2 = st.tabs([f"⭐ Best matches ({len(best)})", f"🌍 Open to everyone ({len(general)})"])
    with tab1:
        for i, (row, reasons) in enumerate(best[:40]):
            scheme_card(row, key=f"best_{i}", reasons=reasons)
        if len(best) > 40:
            st.caption(f"Showing first 40 of {len(best)}.")
    with tab2:
        for i, (row, reasons) in enumerate(general[:40]):
            scheme_card(row, key=f"gen_{i}", reasons=reasons)
        if len(general) > 40:
            st.caption(f"Showing first 40 of {len(general)}.")
