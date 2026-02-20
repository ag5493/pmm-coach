import anthropic
import streamlit as st


def _resolve_api_key() -> str:
    """
    Resolve the Anthropic API key from (in priority order):
      1. st.session_state  — set by the user via the sidebar or the key-gate screen
      2. st.secrets         — set in Streamlit Cloud dashboard or secrets.toml
    Returns an empty string if none found.
    """
    # 1. Already saved in this session
    key = st.session_state.get("ANTHROPIC_API_KEY", "")
    if key:
        return key

    # 2. Streamlit secrets (Cloud deployment or local secrets.toml)
    try:
        key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if key:
            st.session_state["ANTHROPIC_API_KEY"] = key  # cache for the session
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
        return  # key is present — nothing to do

    # ── Styled key-gate screen (white, minimal) ─────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
    .key-gate {
        max-width: 520px;
        margin: 6rem auto 0;
        background: #FFFFFF;
        border: 1px solid #E6E6E6;
        border-radius: 12px;
        padding: 2.5rem 2rem;
        text-align: center;
    }
    .key-gate .logo {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        color: #C9A84C;
    }
    .key-gate .subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #6B6B6B;
        margin-top: -4px;
        margin-bottom: 1.25rem;
    }
    .key-gate h2 {
        font-family: 'Syne', sans-serif !important;
        font-size: 1.25rem !important;
        color: #0D0D0D;
        margin-bottom: 0.4rem;
    }
    .key-gate p {
        font-size: 0.95rem;
        color: #6B6B6B;
        margin-bottom: 1.25rem;
        line-height: 1.6;
    }
    .key-gate a { color: #C9A84C; text-decoration: none; }
    </style>

    <div class="key-gate">
        <div class="logo">PMM Coach</div>
        <div class="subtitle">Unlock modules</div>
        <h2>API Key Required</h2>
        <p>
            This app uses Claude (Anthropic).<br>
            Enter your API key to unlock the coaching modules.<br>
            <a href="https://console.anthropic.com/account/keys" target="_blank">
                Get your key at console.anthropic.com →
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
        save_btn = st.button("Unlock PMM Coach →", use_container_width=True)

    if save_btn:
        if entered_key.strip().startswith("sk-ant-"):
            st.session_state["ANTHROPIC_API_KEY"] = entered_key.strip()
            st.success("Key saved! Loading...")
            st.rerun()
        elif entered_key.strip():
            st.error("That doesn't look like a valid Anthropic key. It should start with `sk-ant-`.")
        else:
            st.warning("Please enter your API key above.")

    st.stop()


def get_client() -> anthropic.Anthropic:
    """Return an Anthropic client, gating on API key presence."""
    require_api_key()
    return anthropic.Anthropic(api_key=st.session_state["ANTHROPIC_API_KEY"])


def stream_response(system: str, messages: list[dict]) -> str:
    """Stream a Claude response and return the full text."""
    client = get_client()
    full_response = ""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=system,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
    return full_response


def get_response(system: str, messages: list[dict], max_tokens: int = 2048) -> str:
    """Get a single Claude response (non-streaming)."""
    client = get_client()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    return response.content[0].text
