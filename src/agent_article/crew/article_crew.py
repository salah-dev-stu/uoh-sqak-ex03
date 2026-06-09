"""Article-writing CrewAI crew — sequential 3-agent phase + parallel LaTeX phase."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from crewai import Crew, Process

from agent_article.agents.editor_agent import EditorAgent
from agent_article.agents.researcher_agent import ResearcherAgent
from agent_article.agents.writer_agent import WriterAgent
from agent_article.crew.latex_runner import run_latex_phase_parallel
from agent_article.shared.config import cfg
from agent_article.shared.logging_fifo import StructuredLogger
from agent_article.tasks.article_tasks import (
    build_edit_task,
    build_latex_tasks,
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

    def run(self) -> CrewResult:
        """Execute full pipeline: sequential 3-agent phase + parallel LaTeX phase."""
        _log.info(f"Starting crew run for topic={self._topic!r}")
        result = CrewResult()
        try:
            researcher = ResearcherAgent()
            writer = WriterAgent()
            editor = EditorAgent()

            t_research = build_research_task(researcher, self._topic)
            t_write = build_write_task(writer, self._topic, [t_research])
            t_edit = build_edit_task(editor, [t_write])

            seq_crew = Crew(
                agents=[researcher.build(), writer.build(), editor.build()],
                tasks=[t_research, t_write, t_edit],
                process=Process.sequential,
                verbose=True,
                respect_context_window=True,
            )
            output = seq_crew.kickoff()
            result.raw_output = str(output)

            latex_tasks = build_latex_tasks([t_edit])
            run_latex_phase_parallel(latex_tasks)

            compiled = self._compile_pdf()
            output_filename = cfg("setup", "output_filename", "uoh-sqak-article.pdf")
            pdf_path = Path("latex/output") / output_filename
            if compiled:
                import shutil
                shutil.copy2(compiled, pdf_path)
                result.success = True
            result.pdf_path = str(pdf_path)
            _log.info(f"Crew run complete: pdf_path={result.pdf_path}")
        except Exception as exc:
            result.errors.append(str(exc))
            _log.error(f"Crew run failed: {exc}")
        return result

    def _compile_pdf(self) -> Path | None:
        """Run lualatex→biber→lualatex→lualatex and return compiled PDF path."""
        from agent_article.tools.latex_compile import LaTeXCompileTool
        try:
            tool = LaTeXCompileTool()
            pdf = tool.run("main.tex")
            _log.info(f"LaTeX compile succeeded: {pdf}")
            return Path(pdf)
        except Exception as exc:
            _log.error(f"LaTeX compile failed: {exc}")
            return None
