"""Public SDK — single entry point for all external callers."""
from pathlib import Path

from agent_article.crew.article_crew import ArticleCrew, CrewResult
from agent_article.shared import version as ver
from agent_article.shared.config import cfg, get_config
from agent_article.shared.gatekeeper import ApiGatekeeper
from agent_article.shared.logging_fifo import StructuredLogger

_log = StructuredLogger("sdk")


class ArticleSDK:
    """
    Input:  topic str
    Output: CrewResult (pdf_path, raw_output, success, errors)
    Setup:  initialised once; call generate() to run the pipeline
    """

    def __init__(self) -> None:
        self._gatekeeper = ApiGatekeeper.instance()
        _log.info(f"ArticleSDK initialised — version={ver.VERSION}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, topic: str) -> CrewResult:
        """Run the full 4-agent pipeline for *topic*."""
        _log.info(f"generate() called with topic={topic!r}")
        crew = ArticleCrew(topic)
        result = crew.run()
        if result.success:
            _log.info(f"generate() succeeded: pdf_path={result.pdf_path}")
        else:
            _log.error(f"generate() failed: {result.errors}")
        return result

    def approve_markdown(self, chapters_dir: str | Path = "workspace/chapters") -> bool:
        """Human-in-the-loop gate: list edited chapters and ask for approval."""
        path = Path(chapters_dir)
        edited = sorted(path.glob("*_edited.md")) if path.exists() else []
        if not edited:
            _log.warning("No edited chapters found for approval")
            return False
        print("\n=== Human-in-the-loop approval gate ===")
        print(f"Edited chapters found ({len(edited)}):")
        for f in edited:
            print(f"  • {f.name}")
        answer = input("Approve and continue to LaTeX compilation? [y/N] ").strip().lower()
        approved = answer in ("y", "yes")
        _log.info(f"Human approval: {approved}")
        return approved

    def spend_report(self) -> dict:
        """Return the ApiGatekeeper spend report."""
        return self._gatekeeper.get_spend_report()

    @staticmethod
    def version() -> str:
        """Return the current SDK version string."""
        return ver.VERSION

    @staticmethod
    def config_summary() -> dict:
        """Return a sanitised summary of loaded configuration."""
        setup = get_config("setup")
        return {
            "version": setup.get("version", "?"),
            "workspace_dir": cfg("setup", "workspace_dir"),
            "output_filename": cfg("setup", "output_filename"),
        }
