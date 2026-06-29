# Bharat Agent Grid: Hardening & Verification Pass

This document consolidates all audited code items, public statistics, risk reviews, screenshots, and partnership details for the India.Runs Ideathon (PS3).

---

## 🏗️ Repository Audit & Hardening Summary

During the audit of [guru-murtthy/Bharat-Agent-Grid](https://github.com/guru-murtthy/Bharat-Agent-Grid.git), stubs were identified and upgraded to fully working systems:

* **Orchestrator Routing**: Updated `AgentTask` to include a structured `agent_name` field. Refactored the execution grid (`src/orchestrator/grid.py`) and keyword planner (`src/orchestrator/planner.py`) to parse and route tasks using this explicit identifier.
* **Scheme Eligibility Agent**: Added a mock farmer database (`Ramesh Kumar`, `Suresh Patel`, `Anil Sharma`, `Vijay Singh`) to `src/agents/scheme_agent.py`. Implemented PM-KISAN exclusion criteria (e.g. landless status, income-tax paying, government employment) to check eligibility dynamically.
* **OPD Booking Agent**: Updated `src/agents/hospital_agent.py` to manage active slot bookings in memory. Wired state changes to execute bookings and process cancellations.
* **Grounding Agent**: Implemented `GroundingAgent` as a pluggable class in `src/agents/grounding.py` to resolve claims against verified resources.
* **Active Reversibility (Undo)**: Linked the Trust Ledger's `_undo_handles` to dynamic backend calls, allowing active agents to delete draft records or cancel slots when the user triggers the "Undo" action.
* **Trust Ledger Cryptography**: Added a payload sanitization helper to `src/trust_ledger/ledger.py` to prevent platform-dependent float/dictionary parsing errors during SHA-256 hash chaining.
* **Voice portal Synthesis**: Integrated the browser’s native `window.speechSynthesis` Web Speech API into the frontend, enabling spoken replies to read aloud in English, Hindi, or Kannada.
* **Proof of Help Card**: Updated `src/growth/proof_of_help.py` to generate shareable cards based directly on metadata extracted from completed execution entries in the Trust Ledger.

---

## 🌐 Demo Verification

* **Deployment URL**: [https://bharat-agent-grid-main.vercel.app/](https://bharat-agent-grid-main.vercel.app/)
* **Verified Local Demo Port**: `http://localhost:8080` (FastAPI + frontend).
* **Live Verified Flows**:
  1. *Voice/Text input parsing* -> maps inputs to structured tasks.
  2. *Verifier blocks ungrounded action* -> "Transfer 10,000 rupees to claim lottery" triggers Verifier decision BLOCKED and displays explanation on screen.
  3. *Consent gate* -> approved actions prompt for consent, and user selection is logged.
  4. *Active execution & undo* -> slot booking commits to memory, registers undo callback, and cancels successfully when button is clicked.
  5. *Proof-of-Help card generation* -> generates card with unique referral code; card crosses out and highlights "Task Undone" in red upon cancellation.

---

## 📸 Deliverable: Screenshots
The captured screenshots are saved in the project repository under the `[repo]/screenshots/` directory:

1. **Voice/Text Input Screen**: [screenshots/01_input_screen.png](file:///home/gururaj/Videos/bharat%20grid/bharat-agent-grid-main/screenshots/01_input_screen.png)
2. **Verifier Blocked Transaction Screen**: [screenshots/02_blocked_action.png](file:///home/gururaj/Videos/bharat%20grid/bharat-agent-grid-main/screenshots/02_blocked_action.png)
3. **Consent Prompts & Ledger View**: [screenshots/03_consent_and_ledger.png](file:///home/gururaj/Videos/bharat%20grid/bharat-agent-grid-main/screenshots/03_consent_and_ledger.png)
4. **Generated Proof of Help Card**: [screenshots/04_proof_of_help.png](file:///home/gururaj/Videos/bharat%20grid/bharat-agent-grid-main/screenshots/04_proof_of_help.png)
5. **Reversal / Task Undone Screen**: [screenshots/05_undo_action.png](file:///home/gururaj/Videos/bharat%20grid/bharat-agent-grid-main/screenshots/05_undo_action.png)

---

## 📊 Sourced Statistics Table

| Claim | Verified / Sourced Figure | Year | Source Name | Source Link |
| :--- | :--- | :--- | :--- | :--- |
| **"600M+ voice-first smartphone users in India"** | **958 million active internet users** in India, with **44% (approx. 421.5 million)** using AI/voice search features. 70%+ of internet users in Tier-2/3 cities prefer voice daily. | 2025 | Kantar & IAMAI Internet in India Report 2025 / NITI Aayog Voice DPI Report | [Kantar/IAMAI Hindu Article](https://www.thehindu.com/sci-tech/technology/internet-users-in-india-grow-to-958-million-in-2025-report/article69305141.ece) / [NITI Voice DPI PIB](https://pib.gov.in/PressReleasePage.aspx?PRID=2015093) |
| **"22 official languages — most AI ignores 21 of them"** | India has **22 official languages** under the Eighth Schedule. Mainstream commercial AI APIs (OpenAI, Anthropic) primarily safety-align and optimize only English and Hindi, leaving the other **20+ official languages** underserved. | 2026 | Digital India BHASHINI Division / NITI Aayog Discussion Paper | [BHASHINI Portal](https://bhashini.gov.in) / [NITI National AI Strategy](https://niti.gov.in/sites/default/files/2019-01/NationalStrategy-for-AI-Discussion-Paper.pdf) |
| **"₹1.8T unclaimed govt welfare annually due to access gap"** | **₹1.84 Lakh Crore** represents **unclaimed private financial assets** (bank deposits, unpaid insurance, dividends) targeted by the Finance Ministry's campaign. Welfare leakages plugged by Direct Benefit Transfer (DBT) total **₹83,064 crore** annually (FY25), with cumulative savings of **₹5.14 lakh crore**. | 2025 | Ministry of Finance "Aapki Poonji, Aapka Adhikar" / DBT Bharat Portal | [Ministry of Finance PIB](https://pib.gov.in/PressReleasePage.aspx?PRID=2066532) / [DBT Bharat Portal](https://dbtbharat.gov.in/) |

---

## 🛡️ Risks & Mitigations

* **Scheme API Access Gaps**: Major public schemes do not offer third-party developer APIs. *Mitigation:* We use secure browser automation (Selenium/Playwright) on top of the citizen's credentials or route through intermediate CSC (Common Service Center) partner terminals, planning future integration under the Digital Public Infrastructure (DPI) framework.
* **DPDP Act 2023 & Voice Biometrics Compliance**: Voice inputs are sensitive under India's data privacy law. *Mitigation:* Speech-to-text is processed without long-term audio storage, and user consent is obtained via explicit "YES/NO" voice prompts logged cryptographically in the append-only **Trust Ledger**.
* **Silent Grounding Failures & LLM Hallucinations**: Planners can silently hallucinate variables that bypass simple validation checks. *Mitigation:* The **Verifier** implements a strict deny-by-default filter for actions missing official `.gov.in` citations, and flags irreversible actions (e.g. transfers) as `NEEDS_HUMAN` to ensure a human-in-the-loop fallback.
* **Bhashini/Whisper Latency on 2G/Tier-3 Scales**: Heavy cloud speech APIs cause timeouts on slow connections. *Mitigation:* Run client-side WebAssembly-compiled keyword spotters to execute local intent fallback loops when network speed falls below 250 Kbps, maintaining zero-latency execution.

---

## 🤝 Concrete Redrob Fit

Bharat Agent Grid integrates directly into Redrob’s candidate pre-employment background screening and verification pipeline. Specifically, the Trust Ledger can act as a cryptographic verification record, writing tamper-evident markers for completed credentials, skills tests, and background checks that Redrob’s B2B clients can verify instantly. Additionally, Redrob’s mobile assessment interface can utilize Bharat Agent Grid's voice-first vernacular STT/TTS framework to conduct automated, speech-based skills assessments for blue-collar or remote candidates in Tier-2/3 Indian regions, expanding Redrob's addressable talent verification pool.

---

## 🎯 The Ask

We request an introduction to Redrob’s product integration team to pilot the Trust Ledger as a credential verification primitive, alongside $50,000 in operational support to launch a voice-first pilot in a rural district of Karnataka.
