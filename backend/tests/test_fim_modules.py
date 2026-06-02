from pathlib import Path

import pytest

from app.fim.change_classifier import severity_for_event
from app.fim.file_scanner import scan_directory
from app.fim.path_validator import validate_directory_path


def test_scan_directory_returns_sorted_relative_file_metadata(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_text("b")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "a.txt").write_text("a")

    files = scan_directory(str(tmp_path))

    assert [item.relative_path for item in files] == ["b.txt", "nested/a.txt"]
    assert all(Path(item.absolute_path).exists() for item in files)
    assert all(item.file_size_bytes == 1 for item in files)


def test_validate_directory_path_success(tmp_path: Path) -> None:
    assert validate_directory_path(str(tmp_path)) == tmp_path.resolve()


def test_validate_directory_path_errors(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        validate_directory_path(str(tmp_path / "missing"))

    file_path = tmp_path / "file.txt"
    file_path.write_text("x")
    with pytest.raises(ValueError, match="not a directory"):
        validate_directory_path(str(file_path))


def test_severity_for_event() -> None:
    assert severity_for_event("UNCHANGED") == "INFO"
    assert severity_for_event("ADDED") == "MEDIUM"
    assert severity_for_event("MODIFIED") == "HIGH"
    assert severity_for_event("DELETED") == "HIGH"
    assert severity_for_event("ERROR") == "MEDIUM"
    assert severity_for_event("UNKNOWN") == "INFO"
