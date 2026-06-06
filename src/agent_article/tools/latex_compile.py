"""LaTeX compilation tool — lualatex → biber → lualatex → lualatex (4 passes)."""
import subprocess
from pathlib import Path
from typing import Any

from agent_article.shared.config import get_config
from agent_article.shared.logging_fifo import StructuredLogger

from .base_tool import BaseTool


class LaTeXCompileTool(BaseTool):
    """
    Input:  main_tex (str, default 'main.tex')
    Output: str path to compiled PDF or raises RuntimeError
    Setup:  config/latex.json for compiler/biber paths and passes count
    """

    def __init__(self, latex_dir: Path | None = None) -> None:
        cfg = get_config("latex")
        self._latex_dir = latex_dir or Path(cfg["main_file"]).parent
        self._compiler = cfg.get("compiler", "lualatex")
        self._biber = cfg.get("biber", "biber")
        self._logger = StructuredLogger("latex_compile")

    @property
    def name(self) -> str:
        return "latex_compile"

    @property
    def description(self) -> str:
        return (
            "Compile a LaTeX document: lualatex → biber → lualatex → lualatex. "
            "Args: main_tex (str, default 'main.tex')"
        )

    def run(self, main_tex: str = "main.tex", **_: Any) -> str:
        stem = Path(main_tex).stem
        out = self._latex_dir / "output"
        out.mkdir(exist_ok=True)
        flags = ["--interaction=nonstopmode", f"--output-directory={out}"]
        self._run_cmd([self._compiler, *flags, main_tex])
        self._run_cmd([self._biber, f"--input-directory={out}", f"--output-directory={out}", stem])
        self._run_cmd([self._compiler, *flags, main_tex])
        self._run_cmd([self._compiler, *flags, main_tex])
        self._check_log(out / f"{stem}.log")
        return str(out / f"{stem}.pdf")

    def _run_cmd(self, cmd: list[str]) -> None:
        from agent_article.shared.gatekeeper import ApiGatekeeper

        def _exec() -> subprocess.CompletedProcess:
            return subprocess.run(
                cmd, cwd=self._latex_dir,
                capture_output=True, text=True, timeout=120,
            )

        result = ApiGatekeeper.instance().call("lualatex", _exec)
        self._logger.info("latex_cmd", cmd=cmd[0], returncode=result.returncode)
        if result.returncode != 0:
            raise RuntimeError(
                f"LaTeX command failed: {' '.join(cmd)}\n{result.stderr[-2000:]}"
            )

    def _check_log(self, log_path: Path) -> None:
        if not log_path.exists():
            return
        log = log_path.read_text(encoding="utf-8", errors="ignore")
        if "Rerun to get cross-references right" in log:
            self._logger.warning("latex_rerun_needed")
        if "Overfull \\hbox" in log:
            self._logger.warning("latex_overfull_hbox")
