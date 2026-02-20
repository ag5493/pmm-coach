import streamlit as st

st.set_page_config(
    page_title="PMM Coach | MOR",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── MOR Brand Styles ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --mor-black:   #0D0D0D;
    --mor-white:   #F5F4F0;
    --mor-gold:    #C9A84C;
    --mor-gold-lt: #E8C97A;
    --mor-gray:    #2A2A2A;
    --mor-mid:     #6B6B6B;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--mor-black);
    color: var(--mor-white);
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111111 !important;
    border-right: 1px solid #222 !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--mor-white);
}

/* Main container */
.block-container {
    padding-top: 2rem !important;
    max-width: 960px !important;
}

/* Buttons */
.stButton > button {
    background-color: var(--mor-gold) !important;
    color: var(--mor-black) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.04em !important;
    transition: background 0.2s ease !important;
}
.stButton > button:hover {
    background-color: var(--mor-gold-lt) !important;
}

/* Text inputs / textareas */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background-color: #1A1A1A !important;
    border: 1px solid #333 !important;
    color: var(--mor-white) !important;
    border-radius: 4px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--mor-gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #1A1A1A !important;
    border-radius: 8px !important;
    border: 1px solid #2A2A2A !important;
    margin-bottom: 0.5rem !important;
}

/* Dividers */
hr { border-color: #2A2A2A !important; }

/* Selectbox */
[data-baseweb="select"] > div {
    background-color: #1A1A1A !important;
    border-color: #333 !important;
}

/* Info / warning boxes */
.stAlert {
    background-color: #1A1A1A !important;
    border-left: 3px solid var(--mor-gold) !important;
    color: var(--mor-white) !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 0.5rem 0;'>
        <span style='font-family: Syne, sans-serif; font-size: 1.6rem; font-weight: 800; color: #C9A84C;'>MOR</span>
        <span style='font-family: DM Sans, sans-serif; font-size: 0.75rem; color: #6B6B6B; display:block; margin-top:-4px; letter-spacing:0.12em; text-transform:uppercase;'>PMM Coach</span>
    </div>
    <hr style='border-color:#222; margin: 0.75rem 0;'/>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='font-size:0.78rem; color:#6B6B6B; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;'>Modules</p>
    """, unsafe_allow_html=True)

    st.page_link("app.py",                    label="🏠  Home",               )
    st.page_link("pages/1_roleplay.py",        label="🎭  Stakeholder Roleplay")
    st.page_link("pages/2_work_reviewer.py",   label="📋  Work Reviewer")
    st.page_link("pages/3_plan_builder.py",    label="🗓️  30-60-90 Plan Builder")
    st.page_link("pages/4_pressure_test.py",   label="🔥  Pressure Test")

    st.markdown("<hr style='border-color:#222; margin:1.5rem 0 0.75rem;'/>", unsafe_allow_html=True)

    existing_key = st.session_state.get("ANTHROPIC_API_KEY", "")
    if existing_key:
        st.markdown("""
        <div style='font-size:0.78rem;color:#6B6B6B;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem;'>API Key</div>
        <div style='font-size:0.85rem;color:#C9A84C;margin-bottom:0.5rem;'>✓ Key active</div>
        """, unsafe_allow_html=True)
        if st.button("Change Key", key="change_key_btn"):
            del st.session_state["ANTHROPIC_API_KEY"]
            st.rerun()
    else:
        new_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...", label_visibility="visible")
        if new_key and new_key.strip().startswith("sk-ant-"):
            st.session_state["ANTHROPIC_API_KEY"] = new_key.strip()
            st.success("Key saved!")
            st.rerun()
        elif new_key:
            st.error("Key should start with `sk-ant-`")

# ── Home Page ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom: 0.25rem;'>
    <span style='font-family: Syne, sans-serif; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.14em; color:#C9A84C;'>Welcome to</span>
</div>
<h1 style='font-size: 3rem; line-height:1.1; margin-bottom: 0.5rem;'>PMM Onboarding<br>Coach</h1>
<p style='color: #6B6B6B; font-size: 1.05rem; max-width: 560px; margin-bottom: 2.5rem;'>
A structured practice environment for first-time Product Marketing Managers — built for Series B B2B SaaS reality, not textbook theory.
</p>
""", unsafe_allow_html=True)

# Module cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background:#1A1A1A; border:1px solid #2A2A2A; border-radius:8px; padding:1.5rem; margin-bottom:1rem;'>
        <div style='font-size:1.6rem; margin-bottom:0.5rem;'>🎭</div>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.1rem; margin-bottom:0.4rem;'>Stakeholder Roleplay</div>
        <div style='color:#6B6B6B; font-size:0.9rem;'>Practice high-stakes conversations with a skeptical founder, territorial PM, or disbelieving sales lead — before they happen for real.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#1A1A1A; border:1px solid #2A2A2A; border-radius:8px; padding:1.5rem; margin-bottom:1rem;'>
        <div style='font-size:1.6rem; margin-bottom:0.5rem;'>🗓️</div>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.1rem; margin-bottom:0.4rem;'>30-60-90 Plan Builder</div>
        <div style='color:#6B6B6B; font-size:0.9rem;'>Build a tailored onboarding plan for your specific company stage, team size, and priorities. Export it as a clean document.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background:#1A1A1A; border:1px solid #2A2A2A; border-radius:8px; padding:1.5rem; margin-bottom:1rem;'>
        <div style='font-size:1.6rem; margin-bottom:0.5rem;'>📋</div>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.1rem; margin-bottom:0.4rem;'>Work Reviewer</div>
        <div style='color:#6B6B6B; font-size:0.9rem;'>Paste your positioning doc, competitive brief, or launch plan and get structured, senior-PMM-level feedback before sharing with stakeholders.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#1A1A1A; border:1px solid #2A2A2A; border-radius:8px; padding:1.5rem; margin-bottom:1rem;'>
        <div style='font-size:1.6rem; margin-bottom:0.5rem;'>🔥</div>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.1rem; margin-bottom:0.4rem;'>Pressure Test</div>
        <div style='color:#6B6B6B; font-size:0.9rem;'>Explain your strategy out loud. A senior PMM will poke holes, challenge assumptions, and help you think sharper before the real meeting.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color:#2A2A2A; margin: 2rem 0;'/>", unsafe_allow_html=True)

st.markdown("""
<div style='display:flex; align-items:center; gap:1rem;'>
    <div>
        <span style='font-family:Syne,sans-serif; font-size:0.8rem; color:#6B6B6B;'>Powered by</span>
        <span style='font-family:Syne,sans-serif; font-size:0.9rem; font-weight:700; color:#C9A84C; margin-left:0.4rem;'>MOR</span>
        <span style='font-family:DM Sans,sans-serif; font-size:0.8rem; color:#6B6B6B;'> — Make Every Dollar of Effort Work Harder.</span>
    </div>
</div>
""", unsafe_allow_html=True)
