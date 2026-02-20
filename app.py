import streamlit as st

st.set_page_config(
    page_title="PMM Coach",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --tm-bg: #FFFFFF;
    --tm-text: #0D0D0D;
    --tm-muted: #6B6B6B;
    --tm-accent: #C9A84C;
    --tm-accent-2: #E8C97A;
    --tm-border: #E6E6E6;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--tm-bg);
    color: var(--tm-text);
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

.block-container {
    padding-top: 2rem !important;
    max-width: 960px !important;
}

.stButton > button {
    background-color: var(--tm-accent) !important;
    color: var(--tm-text) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.2rem !important;
    transition: background 0.15s ease !important;
}
.stButton > button:hover {
    background-color: var(--tm-accent-2) !important;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background-color: #FFFFFF !important;
    border: 1px solid var(--tm-border) !important;
    color: var(--tm-text) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--tm-accent) !important;
    box-shadow: 0 0 0 4px rgba(201,168,76,0.06) !important;
}

[data-testid="stChatMessage"] {
    background-color: #FAFAFA !important;
    border-radius: 8px !important;
    border: 1px solid var(--tm-border) !important;
    margin-bottom: 0.5rem !important;
}

hr { border-color: var(--tm-border) !important; }

[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: var(--tm-border) !important;
}

.stAlert {
    background-color: #FFFDF5 !important;
    border-left: 3px solid var(--tm-accent) !important;
    color: var(--tm-text) !important;
}

[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid var(--tm-border);
    border-radius: 8px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Sidebar removed — module links are available on the home page
# Keep API key entry in the main UI
existing_key = st.session_state.get("ANTHROPIC_API_KEY", "")
if existing_key:
    st.markdown("""
    <div style='font-size:0.9rem;color:var(--tm-muted);margin-bottom:0.5rem;'>API Key: active</div>
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
    <span style='font-family: Syne, sans-serif; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.14em; color:var(--tm-accent);'>Welcome to</span>
</div>
<h1 style='font-size: 2.6rem; line-height:1.1; margin-bottom: 0.5rem;'>PMM Onboarding Coach</h1>
<p style='color: var(--tm-muted); font-size: 1.05rem; max-width: 560px; margin-bottom: 2.5rem;'>
A modern practice environment for new Product Marketing Managers — focused on practical, revenue-aligned skills.
</p>
""", unsafe_allow_html=True)

# Module cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background:#FFFFFF; border:1px solid var(--tm-border); border-radius:8px; padding:1.25rem; margin-bottom:1rem;'>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.05rem; margin-bottom:0.4rem;'>Stakeholder Roleplay</div>
        <div style='color:var(--tm-muted); font-size:0.9rem;'>Practice high-stakes conversations with founders, PMs, or sales stakeholders before they happen.</div>
        <div style='margin-top:0.75rem;'>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_roleplay.py", label="Open Roleplay")
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#FFFFFF; border:1px solid var(--tm-border); border-radius:8px; padding:1.25rem; margin-bottom:1rem;'>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.05rem; margin-bottom:0.4rem;'>30-60-90 Plan Builder</div>
        <div style='color:var(--tm-muted); font-size:0.9rem;'>Generate a focused onboarding plan tailored to your role and company.</div>
        <div style='margin-top:0.75rem;'>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_plan_builder.py", label="Open Plan Builder")
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background:#FFFFFF; border:1px solid var(--tm-border); border-radius:8px; padding:1.25rem; margin-bottom:1rem;'>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.05rem; margin-bottom:0.4rem;'>Work Reviewer</div>
        <div style='color:var(--tm-muted); font-size:0.9rem;'>Get structured, senior-level feedback on positioning docs, briefs, and launch plans.</div>
        <div style='margin-top:0.75rem;'>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_work_reviewer.py", label="Open Work Reviewer")
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#FFFFFF; border:1px solid var(--tm-border); border-radius:8px; padding:1.25rem; margin-bottom:1rem;'>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.05rem; margin-bottom:0.4rem;'>Pressure Test</div>
        <div style='color:var(--tm-muted); font-size:0.9rem;'>Practice explaining your strategy and get direct, critical feedback to sharpen your thinking.</div>
        <div style='margin-top:0.75rem;'>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_pressure_test.py", label="Open Pressure Test")
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color:var(--tm-border); margin: 2rem 0;'/>", unsafe_allow_html=True)

st.markdown("""
<div style='display:flex; align-items:center; gap:1rem;'>
    <div>
        <span style='font-family:Syne,sans-serif; font-size:0.85rem; color:var(--tm-muted);'>PMM Coach</span>
    </div>
</div>
""", unsafe_allow_html=True)
