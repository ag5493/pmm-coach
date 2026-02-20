import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.claude_client import get_client

st.set_page_config(page_title="30-60-90 Plan Builder | PMM Coach", layout="wide")

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
<span style='font-family:Syne,sans-serif;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.14em;color:var(--tm-accent);'>Module 3</span>
<h1 style='font-size:2.2rem;margin-bottom:0.3rem;'>30-60-90 Day Plan Builder</h1>
<p style='color:var(--tm-muted);font-size:1rem;margin-bottom:2rem;max-width:560px;'>
Answer a few questions about your role and company, and get a tailored onboarding plan built for fast-moving B2B SaaS environments.
</p>
""", unsafe_allow_html=True)

with st.form("plan_form"):
    st.markdown("### About Your Role")
    col1, col2 = st.columns(2)
    with col1:
        company_stage = st.selectbox("Company Stage", ["Series A", "Series B", "Series C", "Growth / Late Stage", "Other"])
        team_size = st.selectbox("Total Company Size", ["< 25 employees", "25–50", "50–100", "100–200", "200+"])
        pmm_team = st.selectbox("PMM Team Size (including you)", ["Solo PMM", "2–3 PMMs", "4+ PMMs"])
    with col2:
        product_type = st.text_input("What does the product do?", placeholder="e.g. Workflow automation for ops teams")
        buyer = st.text_input("Primary buyer / ICP", placeholder="e.g. VP Operations at mid-market SaaS")
        sales_motion = st.selectbox("Sales Motion", ["Product-led (PLG)", "Sales-led", "Hybrid PLG + Sales"])

    st.markdown("### Your Situation")
    background = st.text_area(
        "Your background (relevant experience)",
        placeholder="e.g. 3 years in content marketing + 1 year in product management. First official PMM title.",
        height=80,
    )
    priorities = st.text_area(
        "What priorities or goals have been shared with you so far?",
        placeholder="e.g. Help sales close deals faster, improve our positioning vs Competitor X, launch new enterprise tier...",
        height=80,
    )
    concerns = st.text_area(
        "What are you most worried about or uncertain on?",
        placeholder="e.g. Navigating a strong founder, proving value quickly, not knowing the product deeply enough...",
        height=80,
    )

    generate_btn = st.form_submit_button("Generate My 30-60-90 Plan →")

PLAN_SYSTEM = """You are a Principal PMM coach who specialises in helping new PMMs onboard successfully at 
Series A and B B2B SaaS companies. You create 30-60-90 day onboarding plans that are specific, actionable, 
and grounded in the reality of fast-moving startups.

Your plans should be structured as:
- **Days 1–30: Listen, Learn, Map** — focused on deep understanding before doing
- **Days 31–60: Synthesise, Build, Align** — first deliverables, stakeholder relationships, quick wins
- **Days 61–90: Execute, Measure, Prove** — visible impact, credibility building, setting the foundation

For each phase include:
- 3-5 specific weekly priorities
- Key stakeholders to meet and what to get from each conversation
- Concrete deliverables with realistic scope
- How to show progress and communicate impact
- Common pitfalls to avoid in this specific environment

Be specific to the details provided. Do not give generic PMM advice. Reference the company stage, 
product type, sales motion, and the person's background directly. Be honest about what's hard."""

if generate_btn:
    if not product_type.strip():
        st.warning("Please fill in at least the product type to generate a plan.")
    else:
        user_message = f"""Please create a personalised 30-60-90 day PMM onboarding plan for me.

**My situation:**
- Company stage: {company_stage}
- Company size: {team_size}
- PMM team: {pmm_team}
- Product: {product_type}
- Primary buyer/ICP: {buyer if buyer else 'Not specified'}
- Sales motion: {sales_motion}
- My background: {background if background else 'Not provided'}
- Shared priorities so far: {priorities if priorities else 'None shared yet'}
- My concerns: {concerns if concerns else 'None specified'}

Create a specific, actionable 30-60-90 day plan tailored to my situation."""

        client = get_client()
        with st.spinner("Building your plan..."):
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=3000,
                system=PLAN_SYSTEM,
                messages=[{"role": "user", "content": user_message}],
            )
            plan = response.content[0].text

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("""
        <span style='font-family:Syne,sans-serif;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.14em;color:#C9A84C;'>Your Plan</span>
        """, unsafe_allow_html=True)
        st.markdown(plan)

        # Download button
        st.download_button(
            label="Download as Markdown",
            data=f"# My PMM 30-60-90 Day Onboarding Plan\n\n{plan}",
            file_name="pmm_30_60_90_plan.md",
            mime="text/markdown",
        )

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("**Want to refine or ask about any part of the plan?**")
        refinement = st.text_input("Ask a follow-up...", placeholder="e.g. How should I handle it if I don't get access to customers in the first 30 days?", key="plan_followup")
        if st.button("Ask →", key="plan_ask") and refinement:
            follow_response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=800,
                system=PLAN_SYSTEM,
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": plan},
                    {"role": "user", "content": refinement},
                ],
            )
            st.markdown(follow_response.content[0].text)
