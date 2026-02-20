import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.claude_client import get_client

st.set_page_config(page_title="Work Reviewer | PMM Coach", layout="wide")

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
hr{ border-color:var(--tm-border) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<span style='font-family:Syne,sans-serif;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.14em;color:var(--tm-accent);'>Module 2</span>
<h1 style='font-size:2.2rem;margin-bottom:0.3rem;'>Work Reviewer</h1>
<p style='color:var(--tm-muted);font-size:1rem;margin-bottom:2rem;max-width:560px;'>
Paste any PMM artifact and get structured, senior-level feedback before it goes to stakeholders. Honest, specific, actionable.
</p>
""", unsafe_allow_html=True)

ARTIFACT_TYPES = [
    "Positioning Document",
    "Competitive Brief",
    "Product Launch Plan",
    "Sales Enablement / Battle Card",
    "Messaging Framework",
    "Win/Loss Analysis",
    "Customer Research Summary",
    "GTM Strategy",
    "Other",
]

col1, col2 = st.columns([1, 1])
with col1:
    artifact_type = st.selectbox("What type of artifact is this?", ARTIFACT_TYPES)
with col2:
    audience = st.text_input(
        "Who is the intended audience?",
        placeholder="e.g. Sales team, CEO, Product team..."
    )

context = st.text_area(
    "Company / role context (optional but recommended)",
    placeholder="e.g. Series B B2B SaaS, workflow automation for ops teams, 50 employees, I'm 2 weeks in...",
    height=70,
)

artifact_text = st.text_area(
    f"Paste your {artifact_type} here",
    placeholder="Paste your full document or draft here...",
    height=280,
)

st.markdown("<br>", unsafe_allow_html=True)
review_btn = st.button("Review My Work")

REVIEW_SYSTEM = """You are a Principal PMM with 12 years of experience at Series A/B B2B SaaS companies. 
You give direct, structured, honest feedback on PMM artifacts. You are not a cheerleader — you point out 
real gaps clearly but constructively. Your feedback framework covers:

1. **Clarity** — Is the core message immediately clear? Would a non-expert understand it?
2. **Audience Fit** — Is the content right for the stated audience? Tone, depth, vocabulary.
3. **PMM Fundamentals** — Does it demonstrate strong positioning, customer insight, and market understanding?
4. **Business Impact** — Does it tie clearly to revenue, pipeline, or business outcomes?
5. **Gaps & Risks** — What's missing? What could backfire? What question will a stakeholder ask that this doesn't answer?
6. **Top 3 Improvements** — Specific, actionable changes ranked by priority.

Be direct. Don't pad your response. A PMM who is new to this role needs honest signal, not validation."""

if review_btn:
    if not artifact_text.strip():
        st.warning("Please paste your artifact text above.")
    else:
        user_message = f"""Please review this {artifact_type}.

Intended audience: {audience if audience else 'Not specified'}

Company/role context: {context if context else 'Not provided'}

--- ARTIFACT START ---
{artifact_text}
--- ARTIFACT END ---

Give me your honest, structured feedback."""

        client = get_client()
        with st.spinner("Reviewing your work..."):
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2000,
                system=REVIEW_SYSTEM,
                messages=[{"role": "user", "content": user_message}],
            )
            feedback = response.content[0].text

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("""
        <span style='font-family:Syne,sans-serif;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.14em;color:var(--tm-accent);'>Feedback</span>
        """, unsafe_allow_html=True)
        st.markdown(feedback)

        # Follow-up questions
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("**Have a follow-up question about this feedback?**")

        if "reviewer_followups" not in st.session_state:
            st.session_state["reviewer_followups"] = []
            st.session_state["reviewer_artifact"] = artifact_text
            st.session_state["reviewer_feedback"] = feedback
            st.session_state["reviewer_context"] = f"{artifact_type} | Audience: {audience} | Context: {context}"

        followup = st.text_input("Ask a follow-up...", placeholder="e.g. Can you give me an example of better positioning language?")
        if st.button("Ask →", key="followup_btn") and followup:
            messages = [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": feedback},
            ]
            for fq, fa in st.session_state["reviewer_followups"]:
                messages.append({"role": "user", "content": fq})
                messages.append({"role": "assistant", "content": fa})
            messages.append({"role": "user", "content": followup})

            with st.spinner("..."):
                fr = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1000,
                    system=REVIEW_SYSTEM,
                    messages=messages,
                )
                followup_answer = fr.content[0].text

            st.session_state["reviewer_followups"].append((followup, followup_answer))
            st.markdown(f"**Q:** {followup}")
            st.markdown(f"**A:** {followup_answer}")
