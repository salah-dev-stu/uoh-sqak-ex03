"""CrewAI BaseLLM wrapper that calls the Claude CLI via subprocess."""
from __future__ import annotations

import subprocess
from typing import Any

from crewai.llms.base_llm import BaseLLM
from pydantic import model_validator


def _default_model() -> str:
    try:
        from agent_article.shared.config import cfg
        return cfg("setup", "default_model", "claude-haiku-4-5-20251001")
    except Exception:
        return "claude-haiku-4-5-20251001"


def _timeout_for_model(model: str) -> int:
    try:
        from agent_article.shared.config import cfg
        svc = cfg("rate_limits", "services", {}).get("claude_cli", {})
        if "sonnet" in model or "opus" in model:
            return int(svc.get("sonnet_timeout_seconds", 600))
        return int(svc.get("haiku_timeout_seconds", 300))
    except Exception:
        return 600


class ClaudeCLILLM(BaseLLM):
    """
    Input:  messages str | list[dict]
    Output: str response via claude -p subprocess
    Setup:  claude CLI must be logged in (claude --login)
    """

    timeout: int = 600
    llm_type: str = "claude-cli"

    @model_validator(mode="before")
    @classmethod
    def _set_defaults(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("model"):
                data["model"] = _default_model()
            if "temperature" not in data:
                data["temperature"] = 0
            if "timeout" not in data:
                data["timeout"] = _timeout_for_model(data.get("model", ""))
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

        from agent_article.shared.gatekeeper import ApiGatekeeper

        cmd = ["claude", "-p", prompt, "--model", self.model]

        def _exec() -> subprocess.CompletedProcess:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)

        result = ApiGatekeeper.instance().call("claude_cli", _exec)
        if result.returncode != 0:
            raise RuntimeError(f"claude CLI failed: {result.stderr[:500]}")
        output = result.stdout.strip()
        for stop_seq in (getattr(self, "stop", None) or []):
            if stop_seq in output:
                output = output[: output.index(stop_seq)]
                break
        return output

    def supports_function_calling(self) -> bool:
        return False

    def supports_stop_words(self) -> bool:
        return False

    def supports_multimodal(self) -> bool:
        return False
