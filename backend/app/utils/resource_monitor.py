"""Runtime CPU and memory measurement utilities for benchmark execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from os import getpid
from time import perf_counter

import psutil


@dataclass(slots=True)
class ResourceSample:
    """A single process resource usage sample.

    Attributes:
        elapsed_ms: Milliseconds elapsed since the monitor started.
        cpu_percent: Process CPU utilization percentage since the previous sample.
        memory_rss_bytes: Resident set size memory usage in bytes.
    """

    elapsed_ms: int
    cpu_percent: float
    memory_rss_bytes: int


@dataclass(slots=True)
class ResourceSummary:
    """Aggregated CPU and memory usage for a monitored operation."""

    average_cpu_percent: float | None
    max_cpu_percent: float | None
    memory_start_bytes: int
    memory_end_bytes: int
    memory_peak_bytes: int


@dataclass(slots=True)
class ResourceMonitor:
    """Measure process CPU and RSS memory usage during a benchmark.

    The monitor intentionally samples the current Python process instead of the
    whole machine so benchmark results are scoped to this FastAPI application.
    Call ``sample()`` periodically during long-running work to improve peak
    memory and CPU accuracy.
    """

    process: psutil.Process = field(default_factory=lambda: psutil.Process(getpid()))
    samples: list[ResourceSample] = field(default_factory=list)
    _started_at: float = field(default=0.0, init=False)
    _memory_start_bytes: int = field(default=0, init=False)

    def __enter__(self) -> "ResourceMonitor":
        """Start CPU/memory measurement and prime psutil CPU counters."""
        self._started_at = perf_counter()
        self._memory_start_bytes = self.process.memory_info().rss
        self.process.cpu_percent(interval=None)
        self.sample()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Capture a final resource sample when leaving the context."""
        self.sample()

    def sample(self) -> ResourceSample:
        """Capture the current process CPU percent and RSS memory usage.

        Returns:
            The captured resource sample.
        """
        elapsed_ms = int((perf_counter() - self._started_at) * 1000)
        sample = ResourceSample(
            elapsed_ms=elapsed_ms,
            cpu_percent=float(self.process.cpu_percent(interval=None)),
            memory_rss_bytes=int(self.process.memory_info().rss),
        )
        self.samples.append(sample)
        return sample

    def summary(self) -> ResourceSummary:
        """Return aggregate CPU and memory metrics for collected samples."""
        memory_values = [self._memory_start_bytes, *(sample.memory_rss_bytes for sample in self.samples)]
        cpu_values = [sample.cpu_percent for sample in self.samples if sample.cpu_percent >= 0]
        return ResourceSummary(
            average_cpu_percent=(sum(cpu_values) / len(cpu_values)) if cpu_values else None,
            max_cpu_percent=max(cpu_values) if cpu_values else None,
            memory_start_bytes=self._memory_start_bytes,
            memory_end_bytes=memory_values[-1],
            memory_peak_bytes=max(memory_values),
        )
