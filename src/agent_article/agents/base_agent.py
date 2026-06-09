"""Abstract base for all CrewAI agents in the article pipeline."""
from abc import ABC, abstractmethod
from typing import Any

from crewai import Agent

from agent_article.shared.config import get_config
from agent_article.skills.base_skill import FileSkill
from agent_article.tools.base_tool import BaseTool


class BaseAgent(ABC):
    """
    Input:  config_key (str) — key in config/agents.json
    Output: crewai.Agent via build()
    Setup:  config/agents.json, skills/<config_key>/SKILL.md
    """

    def __init__(
        self,
        config_key: str,
        tools: list[BaseTool],
        model_override: str | None = None,
    ) -> None:
        self._cfg = get_config("agents")["agents"][config_key]
        self._skill = FileSkill(self._cfg["skill_ref"])
        self._tools = tools
        self._model_override = model_override

    @abstractmethod
    def build(self) -> Agent: ...

    def _resolve_llm(self) -> Any:
        """Return an LLM object based on config llm key."""
        llm_key = self._cfg.get("llm", "claude-cli")
        if llm_key == "claude-cli":
            from agent_article.shared.claude_cli_llm import ClaudeCLILLM
            if self._model_override:
                return ClaudeCLILLM(model=self._model_override)
            return ClaudeCLILLM()
        return None

    def _make_agent(self) -> Agent:
        backstory = self._cfg["backstory"] + "\n\n---\n\n" + self._skill.content
        llm = self._resolve_llm()
        kwargs: dict[str, Any] = {
            "role": self._cfg["role"],
            "goal": self._cfg["goal"],
            "backstory": backstory,
            "tools": [t.as_crewai_tool() for t in self._tools],
            "verbose": True,
            "max_iter": self._cfg.get("max_iter", 3),
        }
        if llm is not None:
            kwargs["llm"] = llm
        return Agent(**kwargs)
