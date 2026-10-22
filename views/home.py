import streamlit as st

from data_loader import get_schemes
from i18n import HOME
from style import image_uri, language_picker, render_html, section_title, esc

df = get_schemes()
code = language_picker()
h = HOME[code]

# ---------- Hero ----------
tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in h["tags"])
render_html(f'''
<div class="hero">
  <div>
    <h1>{esc(h["hero_title"])}</h1>
    <p>{esc(h["hero_sub"])}</p>
    {tags}
  </div>
  <img src="{image_uri("hero.svg")}" alt="Chatbot on a phone">
</div>
''')

c1, c2, _ = st.columns([1, 1, 2])
with c1:
    st.page_link("views/chatbot.py", label=h["cta_chat"], icon="🤖", use_container_width=True)
with c2:
    st.page_link("views/find.py", label=h["cta_find"], icon="🔎", use_container_width=True)

# ---------- Numbers ----------
render_html(f'''
<div class="stats">
  <div class="stat"><b>{len(df)}</b><span>{esc(h["stat_schemes"])}</span></div>
  <div class="stat"><b>🏛️</b><span>{esc(h["stat_levels"])}</span></div>
  <div class="stat"><b>3</b><span>{esc(h["stat_lang"])}</span></div>
  <div class="stat"><b>🎤🔊</b><span>{esc(h["stat_voice"])}</span></div>
</div>
''')

# ---------- What is this site ----------
section_title(h["about_title"])
st.markdown(f"<div style='font-size:1.08rem; line-height:1.75; color:#243247'>{esc(h['about'].format(n=len(df)))}</div>",
            unsafe_allow_html=True)

# ---------- What can you do (navigation cards) ----------
section_title(h["do_title"])
cards = [
    ("🤖", h["f1_title"], h["f1_text"], "views/chatbot.py"),
    ("🔎", h["f2_title"], h["f2_text"], "views/find.py"),
    ("📚", h["f3_title"], h["f3_text"], "views/browse.py"),
]
for col, (icon, title, text, page) in zip(st.columns(3), cards):
    with col:
        with st.container(border=True):
            render_html(f'<div class="feature-icon">{icon}</div><div class="feature-title">{esc(title)}</div>'
                        f'<div class="feature-text">{esc(text)}</div>')
            st.page_link(page, label=f'{h["go"]}  {title}', icon="➡️", use_container_width=True)

# ---------- Who is it for ----------
section_title(h["who_title"])
people = "".join(f'<div class="persona"><span>{e}</span>{esc(n)}</div>' for e, n in h["personas"])
render_html(f'<div class="personas">{people}</div>')

# ---------- How it works ----------
section_title(h["how_title"])
steps = "".join(f'<div class="step"><div class="step-num">{i}</div>{esc(s)}</div>'
                for i, s in enumerate(h["steps"], 1))
render_html(f'<div class="steps">{steps}</div>')

render_html(f'<div class="note">⚠️ {esc(h["note"])}</div>')
