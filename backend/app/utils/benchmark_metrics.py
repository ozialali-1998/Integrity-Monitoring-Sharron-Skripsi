"""Benchmark metric helpers."""

from __future__ import annotations


def calculate_accuracy_percent(total_items: int, matched_items: int) -> float | None:
    """Calculate benchmark verification accuracy as a percentage.

    Args:
        total_items: Number of benchmarked items.
        matched_items: Number of items whose verification hash matched the
            original benchmark hash.

    Returns:
        Accuracy percentage in the range 0..100, or ``None`` when no items were
        benchmarked.

    Raises:
        ValueError: If counts are negative or matched items exceed total items.
    """
    if total_items < 0 or matched_items < 0:
        raise ValueError("Benchmark accuracy counts must not be negative")
    if matched_items > total_items:
        raise ValueError("Matched benchmark items cannot exceed total items")
    if total_items == 0:
        return None
    return (matched_items / total_items) * 100
