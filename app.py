import streamlit as st
import sys, os
sys.path.append(os.path.dirname(__file__))
from utils.claude_client import get_client

st.set_page_config(
    page_title="PMM Coach",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:         #FFFFFF;
    --bg-subtle:  #F7F8FA;
    --border:     #E5E7EB;
    --border-mid: #D1D5DB;
    --text:       #111827;
    --text-mid:   #4B5563;
    --text-muted: #9CA3AF;
    --blue:       #2053C5;
    --blue-hover: #1A44A8;
    --blue-light: #EEF2FF;
    --blue-mid:   #C7D2FE;
    --radius:     8px;
}

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background-color: var(--bg) !important; }

h1,h2,h3,h4,h5,h6 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text) !important;
}

/* Hide default sidebar toggle & sidebar */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
#MainMenu { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }

/* Remove default top padding so navbar sits flush */
.block-container {
    padding-top: 0 !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1100px !important;
}

/* ── Top navbar ── */
.pmm-navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    background: #FFFFFF;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    height: 56px;
    margin-left: -2rem;
    margin-right: -2rem;
    margin-bottom: 2rem;
    width: calc(100% + 4rem);
}
.pmm-navbar .brand {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--blue);
    white-space: nowrap;
    text-decoration: none;
}
.pmm-navbar .nav-links {
    display: flex;
    align-items: center;
    gap: 0.15rem;
    flex: 1;
    margin-left: 2rem;
}
.pmm-navbar .nav-links a {
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-mid);
    text-decoration: none;
    padding: 0.35rem 0.85rem;
    border-radius: 6px;
    transition: all 0.15s ease;
    white-space: nowrap;
}
.pmm-navbar .nav-links a:hover {
    background: var(--bg-subtle);
    color: var(--text);
}
.pmm-navbar .nav-links a.active {
    background: var(--blue-light);
    color: var(--blue);
    font-weight: 600;
}
.pmm-navbar .nav-right {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
}
.key-badge {
    background: var(--blue-light);
    color: var(--blue);
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid var(--blue-mid);
    white-space: nowrap;
}
.key-badge-missing {
    background: #FEF3C7;
    color: #92400E;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid #FDE68A;
    white-space: nowrap;
}

/* ── API key banner (shown when no key) ── */
.key-banner {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}
.key-banner p {
    margin: 0;
    font-size: 0.9rem;
    color: #78350F;
    font-family: 'DM Sans', sans-serif;
}
.key-banner a { color: var(--blue); }

/* ── Buttons ── */
.stButton > button {
    background-color: var(--blue) !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.5rem 1.25rem !important;
    font-size: 0.875rem !important;
    transition: background 0.15s ease !important;
}
.stButton > button:hover { background-color: var(--blue-hover) !important; }

/* Secondary ghost button */
.stButton.secondary > button {
    background-color: transparent !important;
    color: var(--text-mid) !important;
    border: 1px solid var(--border-mid) !important;
}
.stButton.secondary > button:hover {
    background-color: var(--bg-subtle) !important;
    color: var(--text) !important;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-mid) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(32,83,197,0.1) !important;
}
label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--text-mid) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: var(--border-mid) !important;
    border-radius: var(--radius) !important;
}
[data-baseweb="select"] span { color: var(--text) !important; }

/* ── Chat ── */
[data-testid="stChatMessage"] {
    background-color: var(--bg-subtle) !important;
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stChatMessage"] p { color: var(--text) !important; }
[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-mid) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
}

/* ── Alerts ── */
.stAlert {
    background-color: var(--blue-light) !important;
    border-left: 3px solid var(--blue) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background-color: var(--bg-subtle) !important;
    color: var(--blue) !important;
    border: 1px solid var(--blue-mid) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    border-radius: var(--radius) !important;
}

/* ── Form submit ── */
[data-testid="stFormSubmitButton"] > button {
    background-color: var(--blue) !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: var(--radius) !important;
}

/* ── Module cards ── */
.mod-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    cursor: pointer;
    transition: box-shadow 0.15s ease, border-color 0.15s ease, transform 0.1s ease;
    text-decoration: none;
    display: block;
}
.mod-card:hover {
    box-shadow: 0 4px 12px rgba(32,83,197,0.12);
    border-color: var(--blue-mid);
    transform: translateY(-1px);
}
.mod-card .tag {
    display: inline-block;
    background: var(--blue-light);
    color: var(--blue);
    font-size: 0.7rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 0.65rem;
}
.mod-card .title {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    color: var(--text);
    margin-bottom: 0.4rem;
}
.mod-card .desc {
    font-size: 0.875rem;
    color: var(--text-mid);
    line-height: 1.6;
}
.mod-card .cta {
    margin-top: 1rem;
    font-size: 0.82rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    color: var(--blue);
}

hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ── Resolve active tab from query params ──────────────────────────────────────
params = st.query_params
active_tab = params.get("tab", "home")

# ── Resolve API key ───────────────────────────────────────────────────────────
def resolve_api_key():
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

api_key = resolve_api_key()

# ── Top Navbar ────────────────────────────────────────────────────────────────
def nav_link(label, tab_id):
    css_class = "active" if active_tab == tab_id else ""
    return f'<a href="?tab={tab_id}" class="{css_class}" target="_self">{label}</a>'

key_html = (
    '<span class="key-badge">API Key Active</span>'
    if api_key else
    '<span class="key-badge-missing">No API Key</span>'
)

st.markdown(f"""
<div class="pmm-navbar">
    <a class="brand" href="?tab=home" target="_self">PMM Coach</a>
    <div class="nav-links">
        {nav_link("Home", "home")}
        {nav_link("Roleplay", "roleplay")}
        {nav_link("Work Reviewer", "reviewer")}
        {nav_link("Plan Builder", "planner")}
        {nav_link("Pressure Test", "pressure")}
    </div>
    <div class="nav-right">
        {key_html}
    </div>
</div>
""", unsafe_allow_html=True)

# ── API Key banner (shown on all tabs if key is missing) ──────────────────────
if not api_key:
    st.markdown("""
    <div class="key-banner">
        <p><strong>API key required.</strong> Enter your Anthropic API key below to use all modules.
        <a href="https://console.anthropic.com/account/keys" target="_blank">Get a key at console.anthropic.com</a></p>
    </div>
    """, unsafe_allow_html=True)
    col_k1, col_k2, col_k3 = st.columns([2, 2, 2])
    with col_k1:
        entered = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...", label_visibility="collapsed")
        if entered and entered.strip().startswith("sk-ant-"):
            st.session_state["ANTHROPIC_API_KEY"] = entered.strip()
            api_key = entered.strip()
            st.rerun()
        elif entered:
            st.error("Key should start with sk-ant-")
elif active_tab == "home":
    # Show change key option subtly on home
    col_k1, col_k2 = st.columns([6,1])
    with col_k2:
        if st.button("Change Key", key="change_key"):
            del st.session_state["ANTHROPIC_API_KEY"]
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB: HOME
# ═══════════════════════════════════════════════════════════════════════════════
if active_tab == "home":
    st.markdown("""
    <div style='margin: 2rem 0 0.25rem 0;'>
        <span style='font-family:Inter,sans-serif;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.12em;color:#2053C5;font-weight:600;'>Product Marketing</span>
    </div>
    <h1 style='font-size:2.5rem;line-height:1.15;margin-bottom:0.6rem;'>PMM Onboarding Coach</h1>
    <p style='color:#4B5563;font-size:1.05rem;max-width:580px;margin-bottom:2.5rem;line-height:1.75;'>
    A structured practice environment for first-time Product Marketing Managers — built for Series B B2B SaaS reality, not textbook theory.
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("""
        <a class="mod-card" href="?tab=roleplay" target="_self">
            <div class="tag">Module 1</div>
            <div class="title">Stakeholder Roleplay</div>
            <div class="desc">Practice difficult conversations with a skeptical founder, territorial PM, or dismissive sales lead before they happen. Get structured feedback after each session.</div>
            <div class="cta">Open Roleplay &rarr;</div>
        </a>
        <a class="mod-card" href="?tab=planner" target="_self">
            <div class="tag">Module 3</div>
            <div class="title">30-60-90 Plan Builder</div>
            <div class="desc">Build a tailored onboarding plan for your specific company stage, team size, and priorities. Export it as a clean Markdown document.</div>
            <div class="cta">Open Plan Builder &rarr;</div>
        </a>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <a class="mod-card" href="?tab=reviewer" target="_self">
            <div class="tag">Module 2</div>
            <div class="title">Work Reviewer</div>
            <div class="desc">Paste your positioning doc, competitive brief, or launch plan and get structured, senior-PMM-level feedback before sharing with stakeholders.</div>
            <div class="cta">Open Work Reviewer &rarr;</div>
        </a>
        <a class="mod-card" href="?tab=pressure" target="_self">
            <div class="tag">Module 4</div>
            <div class="title">Pressure Test</div>
            <div class="desc">Explain your strategy out loud. A senior PMM will challenge your assumptions and poke holes — so you think sharper before the real meeting.</div>
            <div class="cta">Open Pressure Test &rarr;</div>
        </a>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:2.5rem 0 1rem;'/>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem;color:#9CA3AF;'>Powered by Claude (Anthropic) · Built for first-time PMMs at fast-growing B2B SaaS companies.</p>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB: ROLEPLAY
# ═══════════════════════════════════════════════════════════════════════════════
elif active_tab == "roleplay":
    st.markdown("""
    <span style='font-family:Inter,sans-serif;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.12em;color:#2053C5;font-weight:600;'>Module 1</span>
    <h1 style='font-size:2rem;margin-bottom:0.3rem;'>Stakeholder Roleplay</h1>
    <p style='color:#4B5563;font-size:0.95rem;margin-bottom:1.75rem;max-width:600px;line-height:1.7;'>
    Practice difficult conversations before they happen. Choose a stakeholder scenario, have a live back-and-forth, then get feedback on how you handled it.
    </p>
    """, unsafe_allow_html=True)

    SCENARIOS = {
        "Skeptical Founder": {
            "system": """You are a demanding Series B startup founder with high standards and limited patience for marketing fluff. You're skeptical of PMM value and constantly push for revenue impact. You ask hard questions like 'How does this move the needle?', 'What's the ROI?', 'Why should I prioritize this over product work?'. You are not hostile but you are direct, data-driven, and will not accept vague answers. Stay in character throughout. After the user says 'END ROLEPLAY', break character and give structured, honest feedback.""",
            "opener": "I've got 15 minutes. Walk me through what you're planning to work on in your first 30 days and why I should care."
        },
        "Territorial Product Manager": {
            "system": """You are a Product Manager at a fast-growing B2B SaaS startup who is protective of the roadmap and skeptical of marketing involvement. You feel PMM often creates noise without insight. You push back on requests for roadmap access, question whether PMM really understands the customer, and challenge positioning. You are professional but guarded. After the user says 'END ROLEPLAY', break character and give structured feedback.""",
            "opener": "So you want to get up to speed on the roadmap. What specifically do you need, and why can't you just read the product docs?"
        },
        "Dismissive Sales Lead": {
            "system": """You are a VP of Sales at a Series B startup who has been burned by marketing before. You think most PMM work is theoretical. You want battle cards, not brand positioning. You're direct, transactional, and challenge the PMM to prove their value in terms of pipeline and quota. After the user says 'END ROLEPLAY', break character and give structured feedback.""",
            "opener": "Look, I'll be straight with you. The last PMM we had gave us a 40-page brand doc that nobody read. What are you actually going to do to help my team hit quota?"
        },
        "Ambiguous Executive": {
            "system": """You are a CRO at a Series B startup who says things like 'I want marketing to be more strategic' but can't clearly articulate what that means. You give vague direction, change priorities frequently, and expect PMM to read your mind. You're not difficult intentionally — you're just moving fast. After the user says 'END ROLEPLAY', break character and give structured feedback on how well the PMM navigated ambiguity.""",
            "opener": "I'm glad you're here. We really need PMM to step up and be more strategic. I'd love to hear your thoughts on how you're going to approach that."
        },
    }

    if not api_key:
        st.warning("Please enter your API key above to use this module.")
    else:
        scenario_key = st.selectbox("Choose your stakeholder scenario", list(SCENARIOS.keys()), key="scenario_select")
        scenario = SCENARIOS[scenario_key]

        col1, col2 = st.columns([3, 1])
        with col1:
            context = st.text_area("Add context about your company or role (optional)", placeholder="e.g. Series B B2B SaaS, 50 employees, first dedicated PMM, workflow automation product...", height=75, key="rp_context")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            start_btn = st.button("Start Roleplay", key="start_btn")
            if st.session_state.get("roleplay_active"):
                if st.button("Reset", key="reset_btn"):
                    for k in ["roleplay_messages","roleplay_active","feedback_given","current_scenario","current_context"]:
                        st.session_state.pop(k, None)
                    st.rerun()

        st.markdown("<hr/>", unsafe_allow_html=True)

        if "roleplay_messages" not in st.session_state: st.session_state["roleplay_messages"] = []
        if "roleplay_active" not in st.session_state:   st.session_state["roleplay_active"] = False
        if "feedback_given" not in st.session_state:    st.session_state["feedback_given"] = False

        if start_btn:
            st.session_state.update({"roleplay_messages": [], "roleplay_active": True, "feedback_given": False,
                                     "current_scenario": scenario_key, "current_context": context})
            st.session_state["roleplay_messages"].append({"role": "assistant", "content": scenario["opener"]})

        if st.session_state["roleplay_active"]:
            cur = SCENARIOS.get(st.session_state.get("current_scenario", scenario_key), scenario)
            st.markdown(f"""<div style='background:#EEF2FF;border:1px solid #C7D2FE;border-radius:8px;padding:0.8rem 1.2rem;margin-bottom:1.25rem;font-size:0.875rem;'>
                <strong style='color:#2053C5;'>Active:</strong> <span style='color:#111827;'>{st.session_state.get('current_scenario','')}</span>
                &nbsp;&nbsp;<span style='color:#9CA3AF;'>Type <code style='background:#fff;border:1px solid #E5E7EB;padding:1px 5px;border-radius:3px;'>END ROLEPLAY</code> when done</span></div>""", unsafe_allow_html=True)

            for msg in st.session_state["roleplay_messages"]:
                with st.chat_message(msg["role"]):
                    st.markdown(f"**{'Stakeholder' if msg['role']=='assistant' else 'You'}:** {msg['content']}")

            if not st.session_state["feedback_given"]:
                user_input = st.chat_input("Your response...")
                if user_input:
                    st.session_state["roleplay_messages"].append({"role": "user", "content": user_input})
                    sys_prompt = cur["system"]
                    if st.session_state.get("current_context"):
                        sys_prompt += f"\n\nContext: {st.session_state['current_context']}"
                    client = get_client()
                    if "END ROLEPLAY" in user_input.upper():
                        st.session_state["feedback_given"] = True
                        with st.chat_message("assistant"):
                            with st.spinner("Generating feedback..."):
                                r = client.messages.create(model="claude-sonnet-4-6", max_tokens=1500, system=sys_prompt, messages=st.session_state["roleplay_messages"])
                                fb = r.content[0].text
                                st.markdown(f"**Feedback:** {fb}")
                        st.session_state["roleplay_messages"].append({"role": "assistant", "content": f"[FEEDBACK] {fb}"})
                        st.rerun()
                    else:
                        full = ""
                        with st.chat_message("assistant"):
                            ph = st.empty()
                            with client.messages.stream(model="claude-sonnet-4-6", max_tokens=512, system=sys_prompt, messages=st.session_state["roleplay_messages"]) as stream:
                                for t in stream.text_stream:
                                    full += t
                                    ph.markdown(f"**Stakeholder:** {full}▌")
                            ph.markdown(f"**Stakeholder:** {full}")
                        st.session_state["roleplay_messages"].append({"role": "assistant", "content": full})
                        st.rerun()
            else:
                st.info("Roleplay complete. Press **Reset** to start a new scenario.")
        else:
            st.markdown("<div style='color:#9CA3AF;text-align:center;padding:2.5rem;border:1px dashed #E5E7EB;border-radius:8px;'>Select a scenario above and click <strong style='color:#2053C5;'>Start Roleplay</strong>.</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB: WORK REVIEWER
# ═══════════════════════════════════════════════════════════════════════════════
elif active_tab == "reviewer":
    st.markdown("""
    <span style='font-family:Inter,sans-serif;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.12em;color:#2053C5;font-weight:600;'>Module 2</span>
    <h1 style='font-size:2rem;margin-bottom:0.3rem;'>Work Reviewer</h1>
    <p style='color:#4B5563;font-size:0.95rem;margin-bottom:1.75rem;max-width:600px;line-height:1.7;'>
    Paste any PMM artifact and get structured, senior-level feedback before it goes to stakeholders.
    </p>
    """, unsafe_allow_html=True)

    if not api_key:
        st.warning("Please enter your API key above to use this module.")
    else:
        ARTIFACT_TYPES = ["Positioning Document","Competitive Brief","Product Launch Plan","Sales Enablement / Battle Card","Messaging Framework","Win/Loss Analysis","Customer Research Summary","GTM Strategy","Other"]
        col1, col2 = st.columns(2)
        with col1: artifact_type = st.selectbox("Artifact type", ARTIFACT_TYPES)
        with col2: audience = st.text_input("Intended audience", placeholder="e.g. Sales team, CEO, Product team...")
        context = st.text_area("Company / role context (optional)", placeholder="e.g. Series B B2B SaaS, 50 employees, 2 weeks in...", height=65)
        artifact_text = st.text_area(f"Paste your {artifact_type}", placeholder="Paste your full document or draft here...", height=260)
        st.markdown("<br>", unsafe_allow_html=True)

        REVIEW_SYSTEM = """You are a Principal PMM with 12 years of experience at Series A/B B2B SaaS companies. Give direct, structured, honest feedback covering:
1. **Clarity** — Is the core message immediately clear?
2. **Audience Fit** — Is the content right for the stated audience?
3. **PMM Fundamentals** — Does it demonstrate strong positioning and customer insight?
4. **Business Impact** — Does it tie clearly to revenue or business outcomes?
5. **Gaps & Risks** — What's missing? What question will a stakeholder ask that this doesn't answer?
6. **Top 3 Improvements** — Specific, actionable changes ranked by priority.
Be direct. Don't pad. New PMMs need honest signal, not validation."""

        if st.button("Review My Work"):
            if not artifact_text.strip():
                st.warning("Please paste your artifact text above.")
            else:
                msg = f"Review this {artifact_type}.\nAudience: {audience or 'Not specified'}\nContext: {context or 'Not provided'}\n\n--- ARTIFACT ---\n{artifact_text}\n--- END ---\n\nGive structured feedback."
                client = get_client()
                with st.spinner("Reviewing..."):
                    r = client.messages.create(model="claude-sonnet-4-6", max_tokens=2000, system=REVIEW_SYSTEM, messages=[{"role":"user","content":msg}])
                    feedback = r.content[0].text
                st.markdown("<hr/>", unsafe_allow_html=True)
                st.markdown("<span style='font-family:Inter,sans-serif;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.12em;color:#2053C5;font-weight:600;'>Feedback</span>", unsafe_allow_html=True)
                st.markdown(feedback)
                st.markdown("<hr/>", unsafe_allow_html=True)
                followup = st.text_input("Ask a follow-up question about this feedback...", key="wr_followup")
                if st.button("Ask", key="wr_ask") and followup:
                    fr = client.messages.create(model="claude-sonnet-4-6", max_tokens=800, system=REVIEW_SYSTEM,
                        messages=[{"role":"user","content":msg},{"role":"assistant","content":feedback},{"role":"user","content":followup}])
                    st.markdown(fr.content[0].text)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB: PLAN BUILDER
# ═══════════════════════════════════════════════════════════════════════════════
elif active_tab == "planner":
    st.markdown("""
    <span style='font-family:Inter,sans-serif;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.12em;color:#2053C5;font-weight:600;'>Module 3</span>
    <h1 style='font-size:2rem;margin-bottom:0.3rem;'>30-60-90 Day Plan Builder</h1>
    <p style='color:#4B5563;font-size:0.95rem;margin-bottom:1.75rem;max-width:600px;line-height:1.7;'>
    Answer a few questions about your role and company, and get a tailored onboarding plan built for your specific situation.
    </p>
    """, unsafe_allow_html=True)

    if not api_key:
        st.warning("Please enter your API key above to use this module.")
    else:
        with st.form("plan_form"):
            st.markdown("#### About Your Role")
            col1, col2 = st.columns(2)
            with col1:
                company_stage = st.selectbox("Company Stage", ["Series A","Series B","Series C","Growth / Late Stage","Other"])
                team_size     = st.selectbox("Total Company Size", ["< 25 employees","25–50","50–100","100–200","200+"])
                pmm_team      = st.selectbox("PMM Team Size (including you)", ["Solo PMM","2–3 PMMs","4+ PMMs"])
            with col2:
                product_type  = st.text_input("What does the product do?", placeholder="e.g. Workflow automation for ops teams")
                buyer         = st.text_input("Primary buyer / ICP", placeholder="e.g. VP Operations at mid-market SaaS")
                sales_motion  = st.selectbox("Sales Motion", ["Product-led (PLG)","Sales-led","Hybrid PLG + Sales"])
            st.markdown("#### Your Situation")
            background = st.text_area("Your background", placeholder="e.g. 3 years content marketing + 1 year PM. First official PMM title.", height=70)
            priorities = st.text_area("Priorities shared with you so far", placeholder="e.g. Help sales close deals, improve positioning vs Competitor X...", height=70)
            concerns   = st.text_area("What are you most worried about?", placeholder="e.g. Navigating a strong founder, proving value quickly...", height=70)
            generate_btn = st.form_submit_button("Generate My 30-60-90 Plan")

        PLAN_SYSTEM = """You are a Principal PMM coach specialising in onboarding new PMMs at Series A/B B2B SaaS companies. Create 30-60-90 day plans structured as:
- **Days 1–30: Listen, Learn, Map** — deep understanding before doing
- **Days 31–60: Synthesise, Build, Align** — first deliverables, quick wins
- **Days 61–90: Execute, Measure, Prove** — visible impact, credibility

For each phase: 3-5 weekly priorities, key stakeholders to meet, concrete deliverables, how to show progress, pitfalls to avoid.
Be specific to the details provided. Reference company stage, product type, sales motion, and background directly."""

        if generate_btn:
            if not product_type.strip():
                st.warning("Please fill in at least the product type.")
            else:
                user_msg = f"""Create a personalised 30-60-90 PMM onboarding plan.
Stage: {company_stage} | Size: {team_size} | PMM team: {pmm_team}
Product: {product_type} | Buyer: {buyer or 'Not specified'} | Motion: {sales_motion}
Background: {background or 'Not provided'}
Priorities: {priorities or 'None shared'}
Concerns: {concerns or 'None'}"""
                client = get_client()
                with st.spinner("Building your plan..."):
                    r = client.messages.create(model="claude-sonnet-4-6", max_tokens=3000, system=PLAN_SYSTEM, messages=[{"role":"user","content":user_msg}])
                    plan = r.content[0].text
                st.markdown("<hr/>", unsafe_allow_html=True)
                st.markdown("<span style='font-family:Inter,sans-serif;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.12em;color:#2053C5;font-weight:600;'>Your Plan</span>", unsafe_allow_html=True)
                st.markdown(plan)
                st.download_button("Download as Markdown", data=f"# PMM 30-60-90 Day Plan\n\n{plan}", file_name="pmm_plan.md", mime="text/markdown")
                st.markdown("<hr/>", unsafe_allow_html=True)
                followup = st.text_input("Ask a follow-up about your plan...", key="plan_followup")
                if st.button("Ask", key="plan_ask") and followup:
                    fr = client.messages.create(model="claude-sonnet-4-6", max_tokens=800, system=PLAN_SYSTEM,
                        messages=[{"role":"user","content":user_msg},{"role":"assistant","content":plan},{"role":"user","content":followup}])
                    st.markdown(fr.content[0].text)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB: PRESSURE TEST
# ═══════════════════════════════════════════════════════════════════════════════
elif active_tab == "pressure":
    st.markdown("""
    <span style='font-family:Inter,sans-serif;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.12em;color:#2053C5;font-weight:600;'>Module 4</span>
    <h1 style='font-size:2rem;margin-bottom:0.3rem;'>Pressure Test</h1>
    <p style='color:#4B5563;font-size:0.95rem;margin-bottom:1.75rem;max-width:600px;line-height:1.7;'>
    Explain your thinking or strategy. A senior PMM will push back, challenge assumptions, and help you think sharper before the real meeting.
    </p>
    """, unsafe_allow_html=True)

    PRESSURE_SYSTEM = """You are a Senior Principal PMM. Pressure test the PMM's thinking by asking hard, probing questions and challenging weak assumptions.
Style: direct but constructive, like a tough mentor. Ask 1-2 sharp questions at a time. Push back on vague language. Challenge them to connect work to revenue.
After 4-5 rounds, if the user types SUMMARISE, give: (1) 2-3 strongest parts, (2) 2-3 biggest gaps, (3) the single most important thing to resolve."""

    if not api_key:
        st.warning("Please enter your API key above to use this module.")
    else:
        if "pressure_messages" not in st.session_state: st.session_state["pressure_messages"] = []
        if "pressure_active"   not in st.session_state: st.session_state["pressure_active"]   = False

        col1, col2 = st.columns([3, 1])
        with col1:
            topic = st.text_area("What do you want to pressure test?",
                placeholder="e.g. My plan for the first 30 days is to focus on listening — interviewing customers and sales before producing any deliverables...\n\nOr: I want to reposition our product from 'workflow automation' to 'operational efficiency'...\n\nBe specific.",
                height=130)
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("Start Pressure Test"):
                if topic.strip():
                    st.session_state["pressure_messages"] = [{"role": "user", "content": topic}]
                    st.session_state["pressure_active"] = True
                else:
                    st.warning("Describe what you want to test.")
            if st.session_state["pressure_active"]:
                if st.button("Reset"):
                    st.session_state["pressure_messages"] = []
                    st.session_state["pressure_active"] = False
                    st.rerun()

        st.markdown("<hr/>", unsafe_allow_html=True)

        if st.session_state["pressure_active"] and len(st.session_state["pressure_messages"]) == 1:
            client = get_client()
            full = ""
            with st.chat_message("assistant"):
                ph = st.empty()
                with client.messages.stream(model="claude-sonnet-4-6", max_tokens=600, system=PRESSURE_SYSTEM, messages=st.session_state["pressure_messages"]) as stream:
                    for t in stream.text_stream:
                        full += t
                        ph.markdown(f"**Senior PMM:** {full}▌")
                ph.markdown(f"**Senior PMM:** {full}")
            st.session_state["pressure_messages"].append({"role": "assistant", "content": full})
            st.rerun()

        if st.session_state["pressure_active"] and len(st.session_state["pressure_messages"]) > 1:
            for msg in st.session_state["pressure_messages"]:
                with st.chat_message(msg["role"]):
                    st.markdown(f"**{'Senior PMM' if msg['role']=='assistant' else 'You'}:** {msg['content']}")
            reply = st.chat_input("Your response... (type SUMMARISE for a final assessment)")
            if reply:
                st.session_state["pressure_messages"].append({"role": "user", "content": reply})
                client = get_client()
                full = ""
                with st.chat_message("assistant"):
                    ph = st.empty()
                    with client.messages.stream(model="claude-sonnet-4-6", max_tokens=800, system=PRESSURE_SYSTEM, messages=st.session_state["pressure_messages"]) as stream:
                        for t in stream.text_stream:
                            full += t
                            ph.markdown(f"**Senior PMM:** {full}▌")
                    ph.markdown(f"**Senior PMM:** {full}")
                st.session_state["pressure_messages"].append({"role": "assistant", "content": full})
                st.rerun()
        elif not st.session_state["pressure_active"]:
            st.markdown("<div style='color:#9CA3AF;text-align:center;padding:2.5rem;border:1px dashed #E5E7EB;border-radius:8px;'>Describe your strategy above, then click <strong style='color:#2053C5;'>Start Pressure Test</strong>.</div>", unsafe_allow_html=True)