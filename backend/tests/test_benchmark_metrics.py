import pytest

from app.utils.benchmark_metrics import calculate_accuracy_percent
from app.utils.resource_monitor import ResourceMonitor


def test_calculate_accuracy_percent() -> None:
    assert calculate_accuracy_percent(4, 3) == 75.0
    assert calculate_accuracy_percent(0, 0) is None


@pytest.mark.parametrize(("total", "matched"), [(-1, 0), (1, -1), (1, 2)])
def test_calculate_accuracy_percent_rejects_invalid_counts(total: int, matched: int) -> None:
    with pytest.raises(ValueError):
        calculate_accuracy_percent(total, matched)


def test_resource_monitor_summary_collects_cpu_and_memory() -> None:
    with ResourceMonitor() as monitor:
        monitor.sample()
    summary = monitor.summary()

    assert summary.average_cpu_percent is not None
    assert summary.max_cpu_percent is not None
    assert summary.memory_start_bytes > 0
    assert summary.memory_end_bytes > 0
    assert summary.memory_peak_bytes >= summary.memory_start_bytes
