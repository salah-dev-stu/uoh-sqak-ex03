"""Article-writing CrewAI crew — sequential 4-agent pipeline."""
from dataclasses import dataclass, field
from pathlib import Path

from crewai import Crew, Process

from agent_article.agents.editor_agent import EditorAgent
from agent_article.agents.latex_agent import LaTeXAgent
from agent_article.agents.researcher_agent import ResearcherAgent
from agent_article.agents.writer_agent import WriterAgent
from agent_article.shared.config import cfg
from agent_article.shared.logging_fifo import StructuredLogger
from agent_article.tasks.article_tasks import (
    build_edit_task,
    build_latex_task,
    build_research_task,
    build_write_task,
)

_log = StructuredLogger("crew")


@dataclass
class CrewResult:
    """
    Input:  Crew kickoff result
    Output: pdf_path str, raw_output str
    Setup:  auto-populated by ArticleCrew.run()
    """

    pdf_path: str = ""
    raw_output: str = ""
    success: bool = False
    errors: list[str] = field(default_factory=list)


class ArticleCrew:
    """
    Input:  topic str
    Output: CrewResult with pdf_path
    Setup:  agents/tasks built lazily on run()
    """

    def __init__(self, topic: str) -> None:
        self._topic = topic
        self._workspace = Path(cfg("setup", "workspace_dir", "workspace"))
        self._workspace.mkdir(parents=True, exist_ok=True)

    def _build_crew(self) -> Crew:
        researcher = ResearcherAgent()
        writer = WriterAgent()
        editor = EditorAgent()
        latex = LaTeXAgent()

        t_research = build_research_task(researcher, self._topic)
        t_write = build_write_task(writer, self._topic, [t_research])
        t_edit = build_edit_task(editor, [t_write])
        t_latex = build_latex_task(latex, [t_edit])

        return Crew(
            agents=[researcher.build(), writer.build(), editor.build(), latex.build()],
            tasks=[t_research, t_write, t_edit, t_latex],
            process=Process.sequential,
            verbose=True,
        )

    def run(self) -> CrewResult:
        """Execute the full 4-agent pipeline and return the result."""
        _log.info(f"Starting crew run for topic={self._topic!r}")
        result = CrewResult()
        try:
            crew = self._build_crew()
            output = crew.kickoff()
            result.raw_output = str(output)
            output_filename = cfg("setup", "output_filename", "uoh-sqak-article.pdf")
            result.pdf_path = str(Path("latex/output") / output_filename)
            result.success = True
            _log.info(f"Crew run complete: pdf_path={result.pdf_path}")
        except Exception as exc:
            result.errors.append(str(exc))
            _log.error(f"Crew run failed: {exc}")
        return result
