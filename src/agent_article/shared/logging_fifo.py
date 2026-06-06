"""FIFO structured logger — rotates log files, max 20 files × 500 lines."""
import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import get_config


class StructuredLogger:
    """
    Input:  component (str)
    Output: JSONL lines written to logs/<component>_NNN.jsonl
    Setup:  config/logging_config.json
    """

    def __init__(self, component: str) -> None:
        self._component = component
        _cfg = get_config("logging_config")
        self._log_dir = Path(_cfg["log_dir"])
        self._max_files = int(_cfg["fifo_files"])
        self._max_lines = int(_cfg["max_lines_per_file"])
        self._lock = threading.Lock()
        self._current_lines = 0
        self._file_index = 0
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._fh = self._open_next()

    def _open_next(self):  # noqa: ANN202
        path = self._log_dir / f"{self._component}_{self._file_index:03d}.jsonl"
        self._rotate_if_needed()
        return path.open("a", encoding="utf-8")

    def _rotate_if_needed(self) -> None:
        files = sorted(self._log_dir.glob(f"{self._component}_*.jsonl"))
        while len(files) >= self._max_files:
            files[0].unlink()
            files = files[1:]

    def _write(self, level: str, message: str, **fields: Any) -> None:
        record = {
            "ts": datetime.now(UTC).isoformat(),
            "level": level,
            "component": self._component,
            "message": message,
            **fields,
        }
        with self._lock:
            self._fh.write(json.dumps(record) + "\n")
            self._fh.flush()
            self._current_lines += 1
            if self._current_lines >= self._max_lines:
                self._fh.close()
                self._file_index += 1
                self._current_lines = 0
                self._fh = self._open_next()

    def info(self, message: str, **fields: Any) -> None:
        self._write("INFO", message, **fields)

    def error(self, message: str, **fields: Any) -> None:
        self._write("ERROR", message, **fields)

    def warning(self, message: str, **fields: Any) -> None:
        self._write("WARNING", message, **fields)
