"""Abstract base class for all CrewAI agent tools."""
from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Input:  *args, **kwargs (tool-specific)
    Output: str or structured result
    Setup:  configured via subclass __init__
    """

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any: ...

    def as_crewai_tool(self) -> Any:
        """Wrap self as a CrewAI-compatible tool callable."""
        from crewai.tools import tool as crewai_tool
        run_fn = self.run
        name_ = self.name
        desc_ = self.description

        @crewai_tool(name_, description=desc_)
        def _tool(*args: Any, **kwargs: Any) -> Any:
            return run_fn(*args, **kwargs)

        return _tool
