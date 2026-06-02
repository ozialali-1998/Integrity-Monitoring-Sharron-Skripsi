from app.db.migrations import BENCHMARK_RESULT_COLUMNS, apply_sqlite_migrations


class _Result:
    def __init__(self, rows):
        self._rows = rows

    def fetchall(self):
        return self._rows


class _Connection:
    def __init__(self, rows):
        self.rows = rows
        self.statements = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def exec_driver_sql(self, statement):
        self.statements.append(statement)
        if statement.startswith("PRAGMA"):
            return _Result(self.rows)
        return _Result([])


class _Engine:
    def __init__(self, rows):
        self.connection = _Connection(rows)

    def begin(self):
        return self.connection


def test_apply_sqlite_migrations_adds_missing_benchmark_columns() -> None:
    engine = _Engine(rows=[(0, "id")])

    apply_sqlite_migrations(engine, "sqlite:///fim.sqlite")

    alter_statements = [statement for statement in engine.connection.statements if statement.startswith("ALTER TABLE")]
    assert len(alter_statements) == len(BENCHMARK_RESULT_COLUMNS)
    assert any("verification_duration_ms" in statement for statement in alter_statements)
    assert any("memory_peak_bytes" in statement for statement in alter_statements)


def test_apply_sqlite_migrations_skips_non_sqlite_database() -> None:
    engine = _Engine(rows=[(0, "id")])

    apply_sqlite_migrations(engine, "postgresql://example")

    assert engine.connection.statements == []
