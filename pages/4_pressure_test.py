import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.claude_client import get_client

st.set_page_config(page_title="Pressure Test | PMM Coach", layout="wide")

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
[data-baseweb="select"]>div{ background-color:#FFFFFF !important; border-color:var(--tm-border) !important; }
.stAlert{ background-color:#FFFDF5 !important; border-left:3px solid var(--tm-accent) !important; color:var(--tm-text) !important; }
[data-testid="stChatMessage"]{ background-color:#FAFAFA !important; border-radius:8px !important; border:1px solid var(--tm-border) !important; margin-bottom:0.5rem !important; }
hr{ border-color:var(--tm-border) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<span style='font-family:Syne,sans-serif;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.14em;color:#C9A84C;'>Module 4</span>
<h1 style='font-size:2.4rem;margin-bottom:0.3rem;'>Pressure Test</h1>
<p style='color:#6B6B6B;font-size:1rem;margin-bottom:2rem;max-width:560px;'>
Explain your thinking, strategy, or approach out loud. A senior PMM will push back, challenge assumptions, and help you think sharper — before the real meeting.
</p>
""", unsafe_allow_html=True)

PRESSURE_SYSTEM = """You are a Senior Principal PMM with deep experience at Series A and B B2B SaaS companies. 
Your job is to pressure test a PMM's thinking by asking hard, probing questions and challenging weak assumptions.

Your style:
- You are direct but not cruel. Think "tough mentor" not "hostile critic."
- You ask one or two sharp questions at a time — you don't overwhelm
- You point out logical gaps, unstated assumptions, and missing evidence
- You push back on vague language ("we'll improve awareness" — "improve by how much? among whom? measured how?")
- You challenge them to connect their work to revenue and business outcomes
- You ask things like: "Who else has tried this?", "What's your proof?", "What happens if that assumption is wrong?", "What would success actually look like?"
- You don't give the answer — you ask the question that forces them to find it

After 4-5 rounds of back-and-forth, if the user asks for a summary, give them:
1. The 2-3 strongest parts of their thinking
2. The 2-3 biggest gaps or risks they haven't addressed
3. The single most important thing to figure out before moving forward"""

# Session state
if "pressure_messages" not in st.session_state:
    st.session_state["pressure_messages"] = []
if "pressure_active" not in st.session_state:
    st.session_state["pressure_active"] = False

col1, col2 = st.columns([3, 1])
with col1:
    topic_input = st.text_area(
        "What strategy, plan, or idea do you want to pressure test?",
        placeholder="""e.g. "My plan for the first 30 days is to focus entirely on listening — interviewing customers, sales, and the product team before I produce any deliverables. I think this will help me build better positioning later."

Or: "I want to reposition our product away from 'workflow automation' toward 'operational efficiency' because I think it resonates better with our ICP."

Be as specific as you can.""",
        height=140,
    )
with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Start Pressure Test"):
        if topic_input.strip():
            st.session_state["pressure_messages"] = [{"role": "user", "content": topic_input}]
            st.session_state["pressure_active"] = True
            st.session_state["pressure_topic"] = topic_input
        else:
            st.warning("Please describe what you want to pressure test.")

    if st.session_state["pressure_active"]:
        if st.button("Reset"):
            st.session_state["pressure_messages"] = []
            st.session_state["pressure_active"] = False
            st.rerun()

st.markdown("<hr/>", unsafe_allow_html=True)

# Generate first response if just started
if st.session_state["pressure_active"] and len(st.session_state["pressure_messages"]) == 1:
    client = get_client()
    full_response = ""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=PRESSURE_SYSTEM,
            messages=st.session_state["pressure_messages"],
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                placeholder.markdown(f"**Senior PMM:** {full_response}▌")
        placeholder.markdown(f"**Senior PMM:** {full_response}")
    st.session_state["pressure_messages"].append({"role": "assistant", "content": full_response})
    st.rerun()

# Display conversation
if st.session_state["pressure_active"] and len(st.session_state["pressure_messages"]) > 1:
    for msg in st.session_state["pressure_messages"]:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"**You:** {msg['content']}")
        else:
            with st.chat_message("assistant"):
                st.markdown(f"**Senior PMM:** {msg['content']}")

    # Response input
    user_reply = st.chat_input("Your response... (or type 'SUMMARISE' for a final assessment)")
    if user_reply:
        st.session_state["pressure_messages"].append({"role": "user", "content": user_reply})
        client = get_client()
        full_response = ""
        with st.chat_message("assistant"):
            placeholder = st.empty()
            with client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=800,
                system=PRESSURE_SYSTEM,
                messages=st.session_state["pressure_messages"],
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    placeholder.markdown(f"**Senior PMM:** {full_response}▌")
            placeholder.markdown(f"**Senior PMM:** {full_response}")
        st.session_state["pressure_messages"].append({"role": "assistant", "content": full_response})
        st.rerun()

elif not st.session_state["pressure_active"]:
    st.markdown("""
    <div style='color:var(--tm-muted);text-align:center;padding:3rem;border:1px dashed var(--tm-border);border-radius:8px;'>
        Describe your strategy or thinking above, then click <strong style='color:var(--tm-accent);'>Start Pressure Test</strong>.
    </div>
    """, unsafe_allow_html=True)
