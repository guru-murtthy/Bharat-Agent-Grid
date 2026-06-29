"""LLM planner with graceful fallback to the keyword planner.

When no LLM key is configured (settings.llm_enabled is False), this delegates to
the deterministic keyword planner so the app always runs with zero keys.
"""
from __future__ import annotations

import json

from src.config import settings
from src.contracts import AgentTask
from src.orchestrator.planner import plan as keyword_plan

_SYSTEM = (
    "You convert a citizen request into a JSON list of tasks. "
    "Each task: {\"intent\": one of [check_scheme, apply_scheme, find_slot, book_slot, transfer_money], "
    "\"agent_name\": one of [scheme_agent, hospital_agent, money_agent], "
    "\"params\": object}. Return ONLY JSON."
)


def plan(utterance: str, language: str = "en") -> list[AgentTask]:
    if not settings.llm_enabled:
        return keyword_plan(utterance, language)
    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": utterance},
            ],
            temperature=0,
        )
        raw = resp.choices[0].message.content or "[]"
        data = json.loads(raw)
        tasks = [
            AgentTask(
                intent=t["intent"],
                agent_name=t.get("agent_name", ""),
                params=t.get("params", {}),
                language=language
            )
            for t in data
            if t.get("intent")
        ]
        return tasks or keyword_plan(utterance, language)
    except Exception:
        # Any failure -> safe deterministic fallback.
        return keyword_plan(utterance, language)
