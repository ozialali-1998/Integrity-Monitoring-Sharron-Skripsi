"""Lightweight SQLite-compatible schema migrations.

The project intentionally keeps a small SQLite footprint. These migrations are
idempotent and only add benchmark metric columns when an existing research
SQLite database was created before the extended benchmark schema existed.
"""

from __future__ import annotations

BENCHMARK_RESULT_COLUMNS: dict[str, str] = {
    "verification_duration_ms": "verification_duration_ms INTEGER",
    "accuracy_percent": "accuracy_percent REAL",
    "verification_matches": "verification_matches INTEGER NOT NULL DEFAULT 0",
    "verification_mismatches": "verification_mismatches INTEGER NOT NULL DEFAULT 0",
    "average_cpu_percent": "average_cpu_percent REAL",
    "max_cpu_percent": "max_cpu_percent REAL",
    "memory_start_bytes": "memory_start_bytes INTEGER",
    "memory_end_bytes": "memory_end_bytes INTEGER",
    "memory_peak_bytes": "memory_peak_bytes INTEGER",
}


def apply_sqlite_migrations(engine, database_url: str) -> None:
    """Apply idempotent SQLite migrations for existing local databases.

    Args:
        engine: SQLAlchemy engine.
        database_url: Configured database URL.
    """
    if not database_url.startswith("sqlite"):
        return

    with engine.begin() as connection:
        rows = connection.exec_driver_sql("PRAGMA table_info(benchmark_results)").fetchall()
        existing_columns = {row[1] for row in rows}
        if not existing_columns:
            return

        for column_name, column_definition in BENCHMARK_RESULT_COLUMNS.items():
            if column_name not in existing_columns:
                connection.exec_driver_sql(f"ALTER TABLE benchmark_results ADD COLUMN {column_definition}")
