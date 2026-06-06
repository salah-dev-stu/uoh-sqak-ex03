"""API Gatekeeper — rate limiting and token budget for all external calls."""
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Callable

from .config import get_config
from .logging_fifo import StructuredLogger


class GatekeeperError(Exception):
    """Raised when rate limit or token budget is exceeded."""


@dataclass
class UsageRecord:
    tokens_in: int = 0
    tokens_out: int = 0
    calls: int = 0


class ApiGatekeeper:
    """
    Input:  service (str), fn (Callable), *args, **kwargs
    Output: fn(*args, **kwargs) result or raises GatekeeperError
    Setup:  config/rate_limits.json
    """

    _instance: "ApiGatekeeper | None" = None

    def __init__(self) -> None:
        self._cfg = get_config("rate_limits")["services"]
        self._usage: dict[str, UsageRecord] = defaultdict(UsageRecord)
        self._call_times: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()
        self._logger = StructuredLogger("gatekeeper")

    @classmethod
    def instance(cls) -> "ApiGatekeeper":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def call(self, service: str, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        with self._lock:
            self._enforce_rate_limit(service)
            self._check_budget(service)
        result = fn(*args, **kwargs)
        with self._lock:
            self._usage[service].calls += 1
        self._logger.info("gatekeeper_call", service=service)
        return result

    def _enforce_rate_limit(self, service: str) -> None:
        rpm = self._cfg.get(service, {}).get("requests_per_minute", 60)
        times = self._call_times[service]
        now = time.monotonic()
        while times and now - times[0] > 60:
            times.popleft()
        if len(times) >= rpm:
            raise GatekeeperError(f"Rate limit exceeded for {service}: {rpm} RPM")
        times.append(now)

    def _check_budget(self, service: str) -> None:
        svc = self._cfg.get(service, {})
        cap = svc.get("tokens_per_article", float("inf"))
        hard_pct = svc.get("hard_cap_percent", 95) / 100
        used = self._usage[service].tokens_in + self._usage[service].tokens_out
        if cap != float("inf") and used >= cap * hard_pct:
            raise GatekeeperError(f"Token budget exceeded for {service}")

    def get_spend_report(self) -> dict[str, UsageRecord]:
        return dict(self._usage)
