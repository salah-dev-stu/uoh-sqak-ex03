"""Python wrapper for the 4-pass LuaLaTeX build (alternative to make)."""
import subprocess
import sys
from pathlib import Path

LATEX_DIR = Path(__file__).parent.parent / "latex"
OUTPUT_DIR = LATEX_DIR / "output"
MAIN = "main"
PDF_NAME = "uoh-sqak-article.pdf"
# Use full TeXLive 2025 for Hebrew BiDi support (GNU FreeFont + luabidi)
_TEXLIVE = Path("/usr/local/texlive/2025/bin/universal-darwin")
LUALATEX = str(_TEXLIVE / "lualatex") if _TEXLIVE.exists() else "lualatex"
BIBER = str(_TEXLIVE / "biber") if _TEXLIVE.exists() else "biber"


def _run(cmd: list[str], cwd: Path) -> int:
    result = subprocess.run(cmd, cwd=cwd, capture_output=False)
    return result.returncode


def build() -> int:
    """Run 4-pass LuaLaTeX + biber compilation."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    passes = [
        ([LUALATEX, "--output-directory=output", "--interaction=nonstopmode", f"{MAIN}.tex"],
         "Pass 1: lualatex"),
        ([BIBER, "--input-directory=output", "--output-directory=output", MAIN],
         "Pass 2: biber"),
        ([LUALATEX, "--output-directory=output", "--interaction=nonstopmode", f"{MAIN}.tex"],
         "Pass 3: lualatex"),
        ([LUALATEX, "--output-directory=output", "--interaction=nonstopmode", f"{MAIN}.tex"],
         "Pass 4: lualatex"),
    ]

    for cmd, label in passes:
        print(f"==> {label}")
        rc = _run(cmd, LATEX_DIR)
        if rc != 0 and "lualatex" in cmd[0]:
            print(f"[WARNING] {label} returned {rc} — continuing (check .log for errors)")

    pdf_src = OUTPUT_DIR / f"{MAIN}.pdf"
    pdf_dst = OUTPUT_DIR / PDF_NAME
    if pdf_src.exists():
        pdf_dst.write_bytes(pdf_src.read_bytes())
        print(f"==> Done: {pdf_dst}")
        return 0
    print(f"[ERROR] PDF not generated: {pdf_src}")
    return 1


if __name__ == "__main__":
    sys.exit(build())
