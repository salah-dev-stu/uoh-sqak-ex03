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
            self._generate_figures()

            compiled = self._compile_with_repair()
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

    def _generate_figures(self) -> None:
        """Generate all pipeline figures into latex/figures/ before compilation."""
        from agent_article.tools.figure_generators import generate_all
        try:
            paths = generate_all()
            _log.info(f"Generated {len(paths)} figures: {paths}")
        except Exception as exc:
            _log.error(f"Figure generation failed (non-fatal): {exc}")

    def _compile_with_repair(self) -> Path | None:
        """Compile LaTeX with up to max_repair_attempts; patch/re-prompt on failure."""
        from agent_article.crew.latex_log_parser import parse as parse_log
        from agent_article.crew.latex_patcher import apply as patch_errors
        from agent_article.crew.latex_repair_agent import repair as repair_errors
        from agent_article.tools.latex_compile import LaTeXCompileTool

        latex_dir = Path(cfg("latex", "main_file", "latex/main.tex")).parent
        max_attempts = cfg("latex", "max_repair_attempts", 3)
        log_path = latex_dir / "output" / "main.log"
        tool = LaTeXCompileTool()

        for attempt in range(1, max_attempts + 1):
            try:
                pdf = tool.run("main.tex")
                _log.info(f"LaTeX compile succeeded on attempt {attempt}: {pdf}")
                return Path(pdf)
            except Exception as exc:
                _log.warning(f"Compile attempt {attempt}/{max_attempts} failed: {exc}")
                if attempt == max_attempts:
                    break
                errors = parse_log(log_path)
                if not errors:
                    _log.error("No parseable errors in log; giving up")
                    break
                known = [e for e in errors if e.kind != "unknown"]
                if known:
                    n = patch_errors(known, latex_dir)
                    _log.info(f"Patched {n} file(s) with {len(known)} known fix(es)")
                if attempt >= 2:
                    unknown_errs = [e for e in errors if e.kind == "unknown"]
                    if unknown_errs:
                        repair_errors(unknown_errs, latex_dir)

        _log.error(f"Repair exhausted after {max_attempts} attempts")
        return None
