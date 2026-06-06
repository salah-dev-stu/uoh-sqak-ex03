"""Fast pipeline: 4 direct claude calls with per-step timing."""
import subprocess
import sys
import time
from pathlib import Path

_LUALATEX = "/usr/local/texlive/2025/bin/universal-darwin/lualatex"
_BIBER = "/usr/local/texlive/2025/bin/universal-darwin/biber"


def _tick(label: str) -> float:
    t = time.time()
    print(f"\n[{label}]", flush=True)
    return t


def _tock(t0: float) -> None:
    print(f"  done in {time.time() - t0:.1f}s", flush=True)


def _claude(prompt: str) -> str:
    t0 = time.time()
    print("  → claude -p ... ", end="", flush=True)
    r = subprocess.run(
        ["claude", "-p", prompt, "--model", "claude-sonnet-4-6"],
        capture_output=True, text=True, timeout=300,
    )
    print(f"{time.time() - t0:.1f}s", flush=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:200])
    return r.stdout.strip()


def _latex_pass(cmd: list, cwd: Path, label: str) -> None:
    t0 = time.time()
    print(f"  → {label} ... ", end="", flush=True)
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180)
    print(f"{time.time() - t0:.1f}s  rc={r.returncode}", flush=True)


def _save_chaps(content: str, base: Path, suffix: str) -> int:
    parts = content.split("===")
    n = 0
    for i, seg in enumerate(parts):
        words = seg.strip().split()
        if not words:
            continue
        last = words[-1]
        body_idx = i + 1
        if body_idx >= len(parts):
            continue
        body = parts[body_idx].strip()
        if not body:
            continue
        fname = last if last.endswith(".md") else f"ch{n+1:02d}{suffix}.md"
        (base / fname).write_text(body)
        n += 1
    if not n:
        (base / f"chapters{suffix}.md").write_text(content)
    return n


def main() -> int:
    topic = " ".join(sys.argv[1:]) or "Multi-Agent Orchestration Patterns"
    ws = Path("workspace")
    ch = ws / "chapters"
    ws.mkdir(exist_ok=True)
    ch.mkdir(exist_ok=True)
    t_total = time.time()
    print(f"\n=== Fast pipeline: {topic!r} ===\n")

    t = _tick("1/4 ResearcherAgent")
    notes = _claude(
        f'Write 800-word research notes on "{topic}". '
        "Include: overview, 3 frameworks (CrewAI/LangGraph/AutoGen), "
        "production patterns, and 5 [AuthorYear] citations."
    )
    (ws / "research_notes.md").write_text(notes)
    print(f"  saved research_notes.md ({len(notes)} chars)")
    _tock(t)

    t = _tick("2/4 WriterAgent")
    chapters = _claude(
        f'Write 6 short Markdown chapters (~200 words each) on "{topic}".\n'
        "ch01: intro. ch02: architectures (include one | table |). "
        "ch03: frameworks (include one | table |). ch04: production "
        "(mark one formula as [NEEDS_FORMULA]). "
        "ch05: write 2 Hebrew paragraphs mixed with English. ch06: case study.\n"
        "Separate with: === chNN_name.md ==="
    )
    saved = _save_chaps(chapters, ch, "")
    print(f"  saved {max(saved, 1)} chapter file(s)")
    _tock(t)

    t = _tick("3/4 EditorAgent")
    edited = _claude(
        "Quick edit: verify [NEEDS_FORMULA] exists in ch04, "
        "Hebrew paragraphs exist in ch05, tables use | syntax. "
        "Return edited chapters with === chNN_edited.md === separators.\n\n"
        + chapters[:1800]
    )
    saved_e = _save_chaps(edited, ch, "_ed")
    print(f"  saved {max(saved_e, 1)} edited file(s)")
    _tock(t)

    t = _tick("4/4 LaTeXAgent — enrich equations")
    eq_latex = _claude(
        "Replace [NEEDS_FORMULA] with a real LaTeX equation block. "
        "Output only: \\begin{equation}...\\end{equation} with 2 lines of context.\n\n"
        + (edited if edited else chapters)[:800]
    )
    ch04 = Path("latex/chapters/ch04_production.tex")
    if ch04.exists():
        ch04.write_text(ch04.read_text() + "\n% generated\n" + eq_latex[:600])
    print("  enriched ch04_production.tex")
    _tock(t)

    t = _tick("LaTeX 4-pass compile")
    ld = Path("latex")
    od = ld / "output"
    od.mkdir(exist_ok=True)
    _latex_pass([_LUALATEX, "--output-directory=output", "--interaction=nonstopmode", "main.tex"], ld, "lualatex 1")
    _latex_pass([_BIBER, "--input-directory=output", "--output-directory=output", "main"], ld, "biber")
    _latex_pass([_LUALATEX, "--output-directory=output", "--interaction=nonstopmode", "main.tex"], ld, "lualatex 3")
    _latex_pass([_LUALATEX, "--output-directory=output", "--interaction=nonstopmode", "main.tex"], ld, "lualatex 4")
    pdf_src = od / "main.pdf"
    pdf_dst = od / "uoh-sqak-article.pdf"
    if pdf_src.exists():
        pdf_dst.write_bytes(pdf_src.read_bytes())
        print(f"  ✓ {pdf_dst}  ({pdf_dst.stat().st_size // 1024} KB)")
        _tock(t)
        print(f"\n=== Total: {time.time() - t_total:.1f}s ===")
        return 0
    print("  ✗ PDF not found — check latex/output/main.log")
    return 1


if __name__ == "__main__":
    sys.exit(main())
