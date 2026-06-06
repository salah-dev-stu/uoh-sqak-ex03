"""DuckDuckGo web search tool — no API key required."""
from typing import Any

from .base_tool import BaseTool


class WebSearchTool(BaseTool):
    """
    Input:  query (str), max_results (int, default 5)
    Output: str formatted search results
    Setup:  duckduckgo-search package; rate-limited by ApiGatekeeper
    """

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return (
            "Search the web using DuckDuckGo. "
            "Args: query (str), max_results (int, default 5)"
        )

    def run(self, query: str, max_results: int = 5, **_: Any) -> str:
        from duckduckgo_search import DDGS

        from agent_article.shared.gatekeeper import ApiGatekeeper

        def _search() -> list[dict]:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=max_results))

        results = ApiGatekeeper.instance().call("duckduckgo", _search)
        if not results:
            return f"No results found for: {query}"
        lines = []
        for r in results:
            lines.append(
                f"**{r.get('title', 'No title')}**\n"
                f"{r.get('body', '')}\n"
                f"URL: {r.get('href', '')}"
            )
        return "\n\n---\n\n".join(lines)
