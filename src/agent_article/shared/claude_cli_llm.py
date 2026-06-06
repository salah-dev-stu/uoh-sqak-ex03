"""CrewAI BaseLLM wrapper that calls the Claude CLI via subprocess."""
from __future__ import annotations

import subprocess
from typing import Any

from crewai.llms.base_llm import BaseLLM
from pydantic import model_validator

_DEFAULT_MODEL = "claude-sonnet-4-6"


class ClaudeCLILLM(BaseLLM):
    """
    Input:  messages str | list[dict]
    Output: str response via claude -p subprocess
    Setup:  claude CLI must be logged in (claude --login)
    """

    timeout: int = 300
    llm_type: str = "claude-cli"

    @model_validator(mode="before")
    @classmethod
    def _set_model_default(cls, data: Any) -> Any:
        if isinstance(data, dict) and not data.get("model"):
            data["model"] = _DEFAULT_MODEL
        return data

    def call(self, messages: str | list[Any], tools: list | None = None, **kwargs: Any) -> str:
        if isinstance(messages, str):
            prompt = messages
        elif isinstance(messages, list):
            parts: list[str] = []
            for m in messages:
                if isinstance(m, dict):
                    parts.append(f"{m.get('role', 'user')}: {m.get('content', '')}")
                else:
                    parts.append(str(getattr(m, "content", m)))
            prompt = "\n".join(parts)
        else:
            prompt = str(messages)

        cmd = ["claude", "-p", prompt, "--model", self.model]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
        if result.returncode != 0:
            raise RuntimeError(f"claude CLI failed: {result.stderr[:500]}")
        return result.stdout.strip()

    def supports_stop_words(self) -> bool:
        return False

    def supports_multimodal(self) -> bool:
        return False
