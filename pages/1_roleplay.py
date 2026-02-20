import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.claude_client import get_client

st.set_page_config(page_title="Stakeholder Roleplay | PMM Coach", layout="wide")

# ── Brand CSS (shared) ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
:root { --tm-bg:#FFFFFF; --tm-text:#0D0D0D; --tm-accent:#C9A84C; --tm-accent-2:#E8C97A; --tm-muted:#6B6B6B; --tm-border:#E6E6E6; }
html,body,[class*="css"]{ font-family:'DM Sans',sans-serif; background-color:var(--tm-bg); color:var(--tm-text); }
h1,h2,h3,h4,h5,h6{ font-family:'Syne',sans-serif !important; font-weight:700 !important; }
.block-container{ padding-top:2rem !important; max-width:960px !important; }
.stButton>button{ background-color:var(--tm-accent) !important; color:var(--tm-text) !important; font-family:'Syne',sans-serif !important; font-weight:700 !important; border:none !important; border-radius:6px !important; padding:0.6rem 1.2rem !important; }
.stButton>button:hover{ background-color:var(--tm-accent-2) !important; }
.stTextInput input,.stTextArea textarea{ background-color:#FFFFFF !important; border:1px solid var(--tm-border) !important; color:var(--tm-text) !important; border-radius:6px !important; }
[data-testid="stChatMessage"]{ background-color:#FAFAFA !important; border-radius:8px !important; border:1px solid var(--tm-border) !important; margin-bottom:0.5rem !important; }
[data-baseweb="select"]>div{ background-color:#FFFFFF !important; border-color:var(--tm-border) !important; }
.stAlert{ background-color:#FFFDF5 !important; border-left:3px solid var(--tm-accent) !important; color:var(--tm-text) !important; }
hr{ border-color:var(--tm-border) !important; }
</style>
""", unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<span style='font-family:Syne,sans-serif;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.14em;color:var(--tm-accent);'>Module 1</span>
<h1 style='font-size:2.2rem;margin-bottom:0.3rem;'>Stakeholder Roleplay</h1>
<p style='color:var(--tm-muted);font-size:1rem;margin-bottom:2rem;max-width:560px;'>
Practice difficult conversations before they happen. Choose a stakeholder scenario and have a live back-and-forth — then get feedback on how you handled it.
</p>
""", unsafe_allow_html=True)

# ── Scenario Selection ────────────────────────────────────────────────────────
SCENARIOS = {
    "Skeptical Founder": {
        "label": "Skeptical Founder",
        "system": """You are a demanding Series B startup founder with high standards and limited patience for marketing fluff. 
You're skeptical of PMM value and constantly push for revenue impact. You ask hard questions like 'How does this move the needle?', 
'What's the ROI?', 'Why should I prioritize this over product work?'. You are direct and data-driven. Stay in character throughout the roleplay. After the user says 'END ROLEPLAY', break character and give structured, honest feedback on how they handled the conversation.""",
        "opener": "I've got 15 minutes. Walk me through what you're planning to work on in your first 30 days and why I should care."
    },
    "Territorial Product Manager": {
        "label": "Territorial PM",
        "system": """You are a Product Manager at a fast-growing B2B SaaS startup who is protective of the roadmap and skeptical of marketing involvement in product decisions. You feel PMM often creates noise without insight. You'll push back on requests for roadmap access, question whether PMM really understands the customer, and challenge the PMM's positioning if it doesn't match your technical understanding. You are professional but guarded. After the user says 'END ROLEPLAY', break character and give structured feedback.""",
        "opener": "So you want to get up to speed on the roadmap. What specifically do you need, and why can't you just read the product docs?"
    },
    "Dismissive Sales Lead": {
        "label": "Dismissive Sales Lead",
        "system": """You are a VP of Sales at a Series B startup who has been burned by marketing before. You think most PMM work is theoretical and doesn't help close deals. You want battle cards, not brand positioning. You're direct and transactional, and will challenge the PMM to prove their value in terms of pipeline and quota attainment. After the user says 'END ROLEPLAY', break character and give structured feedback.""",
        "opener": "Look, I'll be straight with you. The last PMM we had gave us a 40-page brand doc that nobody read. What are you actually going to do to help my team hit quota?"
    },
    "Ambiguous Executive": {
        "label": "Ambiguous Executive",
        "system": """You are a Chief Revenue Officer at a Series B startup who says things like 'I want marketing to be more strategic' but can't clearly articulate what that means. You give vague direction, change priorities frequently, and expect PMM to read your mind. You're not difficult intentionally — you're just moving fast and haven't thought deeply about what you need from PMM. After the user says 'END ROLEPLAY', break character and give structured feedback on how well the PMM navigated ambiguity.""",
        "opener": "I'm glad you're here. We really need PMM to step up and be more strategic. I'd love to hear your thoughts on how you're going to approach that."
    },
}

scenario_key = st.selectbox(
    "Choose your stakeholder scenario",
    list(SCENARIOS.keys()),
    key="scenario_select"
)

scenario = SCENARIOS[scenario_key]

col1, col2 = st.columns([3, 1])
with col1:
    context = st.text_area(
        "Optional: Add context about your company/role (helps personalise the simulation)",
        placeholder="e.g. Series B B2B SaaS, 50 employees, I'm the first dedicated PMM, product is a workflow automation tool for ops teams...",
        height=80,
        key="context_input"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    start_btn = st.button("Start Roleplay", key="start_btn")
    if st.session_state.get("roleplay_active"):
        if st.button("Reset", key="reset_btn"):
            st.session_state["roleplay_messages"] = []
            st.session_state["roleplay_active"] = False
            st.session_state["feedback_given"] = False
            st.rerun()

st.markdown("<hr/>", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────
if "roleplay_messages" not in st.session_state:
    st.session_state["roleplay_messages"] = []
if "roleplay_active" not in st.session_state:
    st.session_state["roleplay_active"] = False
if "feedback_given" not in st.session_state:
    st.session_state["feedback_given"] = False

# ── Start Roleplay ────────────────────────────────────────────────────────────
if start_btn:
    st.session_state["roleplay_messages"] = []
    st.session_state["roleplay_active"] = True
    st.session_state["feedback_given"] = False
    st.session_state["current_scenario"] = scenario_key
    st.session_state["current_context"] = context
    # Add opening message from the stakeholder
    opener = scenario["opener"]
    st.session_state["roleplay_messages"].append({
        "role": "assistant",
        "content": opener
    })

# ── Chat Interface ────────────────────────────────────────────────────────────
if st.session_state["roleplay_active"]:
    current_scenario = SCENARIOS.get(st.session_state.get("current_scenario", scenario_key), scenario)

    st.markdown(f"""
    <div style='background:#FAFAFA;border:1px solid var(--tm-border);border-radius:8px;padding:1rem 1.5rem;margin-bottom:1.5rem;'>
        <span style='color:var(--tm-accent);font-family:Syne,sans-serif;font-weight:700;'>Active Scenario:</span>
        <span style='color:var(--tm-text);margin-left:0.5rem;'>{current_scenario["label"]}</span>
        <span style='color:var(--tm-muted);font-size:0.8rem;margin-left:1rem;'>Type <code style='background:#F5F5F5;padding:2px 6px;border-radius:3px;'>END ROLEPLAY</code> to finish and get feedback</span>
    </div>
    """, unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state["roleplay_messages"]:
        role_label = "Stakeholder" if msg["role"] == "assistant" else "You"
        with st.chat_message(msg["role"]):
            st.markdown(f"**{role_label}:** {msg['content']}")

    # User input
    if not st.session_state["feedback_given"]:
        user_input = st.chat_input("Your response...")
        if user_input:
            st.session_state["roleplay_messages"].append({"role": "user", "content": user_input})

            # Check if ending roleplay
            if "END ROLEPLAY" in user_input.upper():
                st.session_state["feedback_given"] = True
                system_prompt = current_scenario["system"]
                if st.session_state.get("current_context"):
                    system_prompt += f"\n\nContext about the PMM's company/role: {st.session_state['current_context']}"

                client = get_client()
                with st.chat_message("assistant"):
                    with st.spinner("Generating feedback..."):
                        response = client.messages.create(
                            model="claude-sonnet-4-6",
                            max_tokens=1500,
                            system=system_prompt,
                            messages=st.session_state["roleplay_messages"],
                        )
                        feedback = response.content[0].text
                        st.markdown(f"**Feedback:** {feedback}")

                st.session_state["roleplay_messages"].append({"role": "assistant", "content": f"[FEEDBACK] {feedback}"})
                st.rerun()
            else:
                # Normal roleplay turn
                system_prompt = current_scenario["system"]
                if st.session_state.get("current_context"):
                    system_prompt += f"\n\nContext about the PMM's company/role: {st.session_state['current_context']}"

                client = get_client()
                full_response = ""
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    with client.messages.stream(
                        model="claude-sonnet-4-6",
                        max_tokens=512,
                        system=system_prompt,
                        messages=st.session_state["roleplay_messages"],
                    ) as stream:
                        for text in stream.text_stream:
                            full_response += text
                            placeholder.markdown(f"**Stakeholder:** {full_response}▌")
                    placeholder.markdown(f"**Stakeholder:** {full_response}")

                st.session_state["roleplay_messages"].append({"role": "assistant", "content": full_response})
                st.rerun()

    else:
        st.info("Roleplay complete. Press **Reset** to try a different scenario or approach.")
else:
    st.markdown("""
    <div style='color:var(--tm-muted);text-align:center;padding:3rem;border:1px dashed var(--tm-border);border-radius:8px;'>
        Select a scenario above and click <strong style='color:var(--tm-accent);'>Start Roleplay</strong> to begin.
    </div>
    """, unsafe_allow_html=True)
