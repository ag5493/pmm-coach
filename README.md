# PMM Onboarding Coach

A structured AI-powered practice environment for first-time Product Marketing Managers, built for Series B B2B SaaS reality.

---

## What It Does

This app gives new PMMs a safe space to practice, get feedback, and build confidence before and during their first 90 days — without needing an expensive coach.

### Modules

| Module | What It Does |
|---|---|
| Stakeholder Roleplay | Practice difficult conversations with a skeptical founder, territorial PM, dismissive sales lead, or ambiguous executive. Get feedback after each session. |
| Work Reviewer | Paste any PMM artifact (positioning doc, competitive brief, battle card) and get structured, senior-PMM-level feedback. |
| 30-60-90 Plan Builder | Answer a few questions about your company and role, and get a tailored onboarding plan built for your specific situation. Download it as Markdown. |
| Pressure Test | Explain your strategy out loud. A senior PMM will challenge your assumptions and poke holes — before the real meeting. |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/pmm-coach.git
cd pmm-coach
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Anthropic API key

You can either:

**Option A** — Enter it in the app sidebar (easiest, no setup needed)

**Option B** — Create a `.env` file:
```bash
cp .env.example .env
# Then edit .env and add your key
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## Deploying to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `app.py` as the entry point
4. Add `ANTHROPIC_API_KEY` as a secret in the Streamlit Cloud dashboard (Settings → Secrets):

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

> **Note:** If you add the key as a Streamlit secret, you can remove the sidebar key input from `app.py` and load it with `st.secrets["ANTHROPIC_API_KEY"]` instead.

---

## Project Structure

```
pmm-coach/
├── app.py                     # Home page & navigation
├── pages/
│   ├── 1_roleplay.py          # Stakeholder Roleplay module
│   ├── 2_work_reviewer.py     # Work Reviewer module
│   ├── 3_plan_builder.py      # 30-60-90 Plan Builder module
│   └── 4_pressure_test.py     # Pressure Test module
├── utils/
│   ├── __init__.py
│   └── claude_client.py       # Shared Anthropic API helpers
├── .streamlit/
│   └── config.toml            # Theme configuration
├── .env.example               # Environment variable template
├── requirements.txt
└── README.md
```

---

## Built With

- [Streamlit](https://streamlit.io) — UI framework
- [Anthropic Claude](https://anthropic.com) — AI backbone (claude-sonnet-4-6)
-- Brand design — [teammor.com](https://teammor.com)

---

## License

MIT
