from pathlib import Path

from conftest import FakeDB

from app.db.models import BaselineFile, MonitoredDirectory
from app.schemas.directory import DirectoryCreate, DirectoryUpdate
from app.schemas.settings import SystemSettingCreate
from app.services.baseline_service import generate_baseline
from app.services.benchmark_service import run_benchmark
from app.services.directory_service import create_directory, update_directory
from app.services.settings_service import create_setting
from app.services.verification_service import verify_directory

SAME_SHA256 = "0967115f2813a3541eaef77de9d9d5773f1c0c04314b0bbfe4ff3b3b1c55b5d5"


def test_directory_create_and_update(tmp_path: Path) -> None:
    db = FakeDB()
    payload = DirectoryCreate(name="Dataset", path=str(tmp_path), description="test", is_active=True)

    directory = create_directory(db, payload)

    assert directory.name == "Dataset"
    assert directory.path == str(tmp_path.resolve())
    assert directory.is_active == 1
    assert db.commits == 1

    updated = update_directory(db, directory, DirectoryUpdate(name="Updated", is_active=False))
    assert updated.name == "Updated"
    assert updated.is_active == 0
    assert db.commits == 2


def test_generate_baseline_creates_baseline_files(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("alpha")
    db = FakeDB()
    directory = MonitoredDirectory(id=1, name="Dataset", path=str(tmp_path), description=None, is_active=1, created_at="now", updated_at="now")

    files, total_size, duration_ms = generate_baseline(db, directory, "SHA-256")

    assert len(files) == 1
    assert files[0].relative_path == "a.txt"
    assert files[0].hash_value
    assert total_size == 5
    assert duration_ms >= 0
    assert db.commits == 1


def test_verify_directory_detects_modified_added_and_deleted(tmp_path: Path) -> None:
    (tmp_path / "same.txt").write_text("same")
    (tmp_path / "changed.txt").write_text("new")
    (tmp_path / "added.txt").write_text("added")
    db = FakeDB()
    directory = MonitoredDirectory(id=1, name="Dataset", path=str(tmp_path), description=None, is_active=1, created_at="now", updated_at="now")
    baseline_files = [
        BaselineFile(
            id=1,
            monitored_directory_id=1,
            relative_path="same.txt",
            absolute_path=str(tmp_path / "same.txt"),
            file_size_bytes=4,
            last_modified_at="old",
            algorithm="SHA-256",
            algorithm_params="{}",
            hash_value=SAME_SHA256,
            hash_duration_ms=1,
            baseline_created_at="old",
            created_at="old",
            updated_at="old",
        ),
        BaselineFile(
            id=2,
            monitored_directory_id=1,
            relative_path="changed.txt",
            absolute_path=str(tmp_path / "changed.txt"),
            file_size_bytes=3,
            last_modified_at="old",
            algorithm="SHA-256",
            algorithm_params="{}",
            hash_value="old-hash",
            hash_duration_ms=1,
            baseline_created_at="old",
            created_at="old",
            updated_at="old",
        ),
        BaselineFile(
            id=3,
            monitored_directory_id=1,
            relative_path="deleted.txt",
            absolute_path=str(tmp_path / "deleted.txt"),
            file_size_bytes=7,
            last_modified_at="old",
            algorithm="SHA-256",
            algorithm_params="{}",
            hash_value="deleted-hash",
            hash_duration_ms=1,
            baseline_created_at="old",
            created_at="old",
            updated_at="old",
        ),
    ]
    db.seed(BaselineFile, baseline_files)

    logs, counts, duration_ms = verify_directory(db, directory, "SHA-256")

    assert len(logs) == 4
    assert counts == {"UNCHANGED": 1, "MODIFIED": 1, "ADDED": 1, "DELETED": 1, "ERROR": 0}
    assert {log.event_type for log in logs} == {"UNCHANGED", "MODIFIED", "ADDED", "DELETED"}
    assert duration_ms >= 0
    assert db.commits == 1


def test_run_benchmark_persists_result(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("alpha")
    db = FakeDB()
    directory = MonitoredDirectory(id=1, name="Dataset", path=str(tmp_path), description=None, is_active=1, created_at="now", updated_at="now")

    results = run_benchmark(db, directory, ["SHA-256"])

    assert len(results) == 1
    assert results[0].algorithm == "SHA-256"
    assert results[0].total_files == 1
    assert results[0].total_size_bytes == 5
    assert db.commits == 1


def test_create_setting_persists_setting() -> None:
    db = FakeDB()
    setting = create_setting(db, SystemSettingCreate(setting_key="default_hash_algorithm", setting_value="SHA-256"))

    assert setting.setting_key == "default_hash_algorithm"
    assert setting.setting_value == "SHA-256"
    assert setting.is_editable == 1
    assert db.commits == 1
