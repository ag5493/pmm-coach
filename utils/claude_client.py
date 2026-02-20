import anthropic
import streamlit as st


def _resolve_api_key() -> str:
    """
    Resolve the Anthropic API key from (in priority order):
      1. st.session_state  — set by the user via sidebar or key-gate screen
      2. st.secrets         — set in Streamlit Cloud dashboard or secrets.toml
    Returns an empty string if none found.
    """
    key = st.session_state.get("ANTHROPIC_API_KEY", "")
    if key:
        return key
    try:
        key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if key:
            st.session_state["ANTHROPIC_API_KEY"] = key
            return key
    except Exception:
        pass
    return ""


def require_api_key() -> None:
    """
    Call this at the top of any page that needs the API.
    If no key is available, renders a full-page key-entry screen and stops execution.
    """
    if _resolve_api_key():
        return

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Sans:wght@400;500&display=swap');
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #FFFFFF !important;
        color: #111827;
    }
    .stApp { background-color: #FFFFFF !important; }
    .key-gate {
        max-width: 460px;
        margin: 6rem auto 0;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    .key-gate .logo {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #2053C5;
    }
    .key-gate .subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #9CA3AF;
        margin-top: 2px;
        margin-bottom: 1.5rem;
    }
    .key-gate h2 {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    .key-gate p {
        font-size: 0.9rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
        line-height: 1.65;
    }
    .key-gate a { color: #2053C5; text-decoration: none; }
    .stTextInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        color: #111827 !important;
        border-radius: 8px !important;
        text-align: center;
    }
    .stTextInput input:focus {
        border-color: #2053C5 !important;
        box-shadow: 0 0 0 3px rgba(32,83,197,0.12) !important;
    }
    .stButton > button {
        background-color: #2053C5 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        width: 100%;
    }
    .stButton > button:hover { background-color: #1A44A8 !important; }
    </style>

    <div class="key-gate">
        <div class="logo">PMM Coach</div>
        <div class="subtitle">Onboarding Practice Tool</div>
        <h2>Enter your API Key</h2>
        <p>
            This app is powered by Claude (Anthropic).<br>
            Enter your API key below to get started.<br>
            <a href="https://console.anthropic.com/account/keys" target="_blank">
                Get your key at console.anthropic.com
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        entered_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            label_visibility="collapsed",
        )
        save_btn = st.button("Unlock PMM Coach", use_container_width=True)

    if save_btn:
        if entered_key.strip().startswith("sk-ant-"):
            st.session_state["ANTHROPIC_API_KEY"] = entered_key.strip()
            st.success("Key saved — loading...")
            st.rerun()
        elif entered_key.strip():
            st.error("That key doesn't look valid. It should start with sk-ant-")
        else:
            st.warning("Please enter your API key above.")

    st.stop()


def get_client() -> anthropic.Anthropic:
    """Return an Anthropic client, gating on API key presence."""
    require_api_key()
    return anthropic.Anthropic(api_key=st.session_state["ANTHROPIC_API_KEY"])