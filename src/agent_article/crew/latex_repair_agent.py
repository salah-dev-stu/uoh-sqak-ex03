# src/agent_article/crew/latex_repair_agent.py
"""Re-prompt ClaudeCLILLM with error context for unknown LaTeX compile errors."""
from __future__ import annotations

from pathlib import Path

from agent_article.crew.latex_log_parser import LatexError
from agent_article.shared.claude_cli_llm import ClaudeCLILLM
from agent_article.shared.logging_fifo import StructuredLogger

_log = StructuredLogger("latex_repair")

_PROMPT = """\
You are a LaTeX expert. The following file failed to compile with this error:

File: {file}
Line: {line}
Error: {message}

Here is the full file content:
{content}

Fix ONLY the error above. Return the complete corrected LaTeX file.
Do NOT add comments. Do NOT change any other content.\
"""


def repair(errors: list[LatexError], latex_dir: Path) -> None:
    """Re-prompt LLM for each unique file with unknown errors; overwrite file."""
    unknown = [e for e in errors if e.kind == "unknown" and e.file]
    if not unknown:
        return
    llm = ClaudeCLILLM()
    seen: set[str] = set()
    for err in unknown:
        if err.file in seen:
            continue
        seen.add(err.file)
        tex_path = latex_dir / err.file
        if not tex_path.exists():
            _log.warning(f"repair: file not found: {tex_path}")
            continue
        content = tex_path.read_text(encoding="utf-8")
        prompt = _PROMPT.format(
            file=err.file, line=err.line,
            message=err.message, content=content,
        )
        _log.info(f"repair: re-prompting for {err.file}: {err.message[:80]}")
        try:
            fixed = llm.call(prompt)
            if fixed.strip():
                tex_path.write_text(fixed.strip(), encoding="utf-8")
                _log.info(f"repair: wrote fix to {err.file}")
        except Exception as exc:
            _log.error(f"repair: LLM failed for {err.file}: {exc}")
