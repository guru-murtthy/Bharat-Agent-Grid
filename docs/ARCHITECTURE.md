# Architecture

## Components

1. **Voice I/O (`src/voice`)** — speech-to-text + text-to-speech for 20+ Indian
   languages. Language auto-detect, spoken consent prompts. (Challenge 3)
2. **Planner (`src/orchestrator/planner.py`)** — converts an utterance into a
   structured list of `AgentTask`s. (Challenge 1)
3. **Execution Grid (`src/orchestrator/grid.py`)** — routes tasks to agents,
   invokes the verifier, gates on consent, writes to the ledger. (Challenge 1)
4. **Domain Agents (`src/agents`)** — Scheme + Hospital agents (extensible to
   finance, legal). Each returns an answer + optional `ProposedAction`. (C3)
5. **Grounding Agent (`src/agents/grounding.py`)** — returns verified citations
   from a source-of-truth store. (Challenge 1)
6. **Verifier (`src/agents/verifier.py`)** — blocks ungrounded actions, forces
   human confirmation for irreversible ones. (Challenge 1 novelty)
7. **Trust Ledger (`src/trust_ledger`)** — append-only, hash-chained,
   consent-gated, reversible audit log. (Signature primitive)
8. **Growth (`src/growth`)** — proof-of-help cards + referral loop. (Challenge 2)

## End-to-end flow

```
utterance
  -> detect_language / speech_to_text          [ledger: utterance]
  -> planner.plan()                             [ledger: plan_created]
  -> for each task:
       route -> agent.run()                     [ledger: result]
       if proposed_action:
         verifier.verify()                       [ledger: decision]
           BLOCKED      -> stop, explain
           NEEDS_HUMAN  -> consent prompt
           APPROVED     -> consent prompt
         consent granted -> execute              [ledger: execute + undo]
  -> proof_of_help card                          [growth loop]
```

## Why this is novel (international level)

- **Trust Ledger as a first-class primitive** (consent + reversibility + audit).
- **Action-grounded anti-hallucination**: nothing executes without a trusted
  cited source.
- **Voice-first, low-literacy-first** for 20+ Indian languages.
- **Trust-as-growth flywheel**: the safety mechanism *is* the growth engine.

## Production swap-ins

| Stub | Production |
|------|-----------|
| keyword planner | LLM planner (LangGraph) |
| in-memory grounding | retrieval over gov/health/finance source-of-truth APIs |
| text STT/TTS stub | Bhashini + Whisper |
| in-memory ledger | append-only store / WORM / blockchain anchor |
