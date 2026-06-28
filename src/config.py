"""Runtime configuration. Falls back to stub mode when no keys are present."""
from __future__ import annotations

import os


class Settings:
    def __init__(self) -> None:
        self.llm_provider = os.getenv("LLM_PROVIDER", "").strip()
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.bhashini_api_key = os.getenv("BHASHINI_API_KEY", "").strip()

    @property
    def llm_enabled(self) -> bool:
        return bool(self.llm_provider and self.openai_api_key)


settings = Settings()
