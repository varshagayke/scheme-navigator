import streamlit as st

from data_loader import get_schemes
from style import banner, render_html, scheme_card

df = get_schemes()

banner("📚 Browse all schemes", "Search and filter every scheme. Open a card to see details and the official website.")

# ---------- Filters ----------
with st.container(border=True):
    query = st.text_input("🔍 Search (scheme name, benefit, who it is for)")
    f1, f2, f3, f4 = st.columns(4)
    groups = f1.multiselect("Category", sorted(df["category_group"].unique()))
    level = f2.selectbox("Government level", ["All", "Central", "Maharashtra State"])
    area = f3.selectbox("Area", ["Any", "Rural", "Urban"])
    age = f4.number_input("Your age (0 = skip)", min_value=0, max_value=100, value=0)

# ---------- Apply filters one by one ----------
result = df.copy()
if query:
    result = result[result["search_text"].str.contains(query.lower(), regex=False)]
if groups:
    result = result[result["category_group"].isin(groups)]
if level != "All":
    result = result[result["level_group"] == level]
if area == "Rural":
    result = result[result["residence"] != "Urban"]
elif area == "Urban":
    result = result[result["residence"] != "Rural"]
if age > 0:
    result = result[(result["min_age"] <= age) & (result["max_age"] >= age)]

# ---------- Numbers and charts ----------
render_html(f'''
<div class="stats" style="grid-template-columns: repeat(3, 1fr);">
  <div class="stat"><b>{len(df)}</b><span>Total schemes</span></div>
  <div class="stat"><b>{len(result)}</b><span>Matching your filters</span></div>
  <div class="stat"><b>{result["category_group"].nunique()}</b><span>Categories found</span></div>
</div>
''')

left, right = st.columns(2)
with left:
    st.subheader("Schemes by category")
    st.bar_chart(result["category_group"].value_counts(), color="#FF9933", horizontal=True)
with right:
    st.subheader("Central vs Maharashtra State")
    st.bar_chart(result["level_group"].value_counts(), color="#138808")

# ---------- Cards ----------
st.subheader("Schemes")
st.warning("This list is a reference. Not every scheme is accepting applications today. "
           "Always confirm on the official website before applying.")
if result.empty:
    st.info("No scheme matches these filters. Try removing one filter.")

for i, (_, row) in enumerate(result.head(30).iterrows()):
    scheme_card(row, key=f"browse_{i}")

if len(result) > 30:
    st.caption(f"Showing first 30 of {len(result)}. Use the filters to narrow down.")
