# Risks & Mitigations

This document outlines four operational and technical risks a judge might raise regarding Bharat Agent Grid, along with concrete mitigations.

### 1. Scheme API Access Gaps
* **Risk:** Major government schemes like PM-KISAN and Ayushman Bharat (PM-JAY) do not currently expose public consumer APIs for third-party execution.
* **Mitigation:** We implement a dual-phase data-access strategy: in Phase 1, we use secure browser automation (Selenium/Playwright) on top of the citizen's credentials or route through intermediate CSC (Common Service Center) partner terminals; in Phase 2, we seek integration under the **Digital Public Infrastructure (DPI)** framework as a licensed third-party application provider under the Open Network for Government Services (ONGS).

### 2. DPDP Act 2023 & Voice Biometrics Compliance
* **Risk:** Voice inputs and personal data fall under strict consent and security mandates of India's Digital Personal Data Protection (DPDP) Act 2023.
* **Mitigation:** Bharat Agent Grid processes speech-to-text locally or within a secure state-boundary cloud wrapper (never saving raw audio long-term); consent is obtained via a clear voice prompt gate ("YES/NO") recorded directly in the append-only, hash-chained **Trust Ledger**, ensuring a verifiable, user-accessible, and undo-capable audit trail.

### 3. Silent Grounding Failures & LLM Hallucinations
* **Risk:** The LLM Planner might silently hallucinate coordinates or parameters, bypassing the Verifier if the grounding database has gaps.
* **Mitigation:** The **Verifier** operates on a strict "deny-by-default" policy: any proposed action that does not match an exact, trusted domain citation (e.g. `.gov.in`) is blocked instantly, and any high-stakes, irreversible action (such as financial transactions) defaults to `NEEDS_HUMAN` verification, ensuring a human-in-the-loop fallback.

### 4. Bhashini/Whisper Costs and Latency on 2G/Tier-3 Networks
* **Risk:** High latency and network timeouts of API-based speech translation (Bhashini/Whisper) make voice portals unusable on slow 2G/3G connections in rural areas.
* **Mitigation:** We run a lightweight, client-side, on-device keyword-spotting classifier (compiled to WebAssembly) that auto-detects key intents (e.g. "appointment", "kisan") and drops to a local fallback loop, bypassing external heavy cloud API calls entirely when network speed drops below 250 Kbps.
