import pytest

from conftest import FakeDB
from fastapi import HTTPException

from app.api.routes import api_router
from app.api.v1.baselines import generate_baseline_endpoint, list_baseline_files_endpoint
from app.api.v1.benchmarks import list_benchmarks_endpoint
from app.api.v1.directories import (
    create_directory_endpoint,
    delete_directory_endpoint,
    get_directory_endpoint,
    list_directory_endpoint,
    update_directory_endpoint,
    validate_path_endpoint,
)
from app.api.v1.health import health_check
from app.api.v1.logs import list_integrity_logs_endpoint
from app.api.v1.settings import create_setting_endpoint, list_settings_endpoint
from app.api.v1.verifications import list_verification_logs_endpoint, run_verification_endpoint
from app.db.models import BaselineFile, BenchmarkResult, IntegrityLog, MonitoredDirectory, SystemSetting
from app.repositories.baselines import list_baseline_files
from app.repositories.directories import get_directory, list_directories
from app.repositories.logs import list_logs
from app.schemas.baseline import BaselineGenerateRequest
from app.schemas.benchmark import BenchmarkRequest
from app.schemas.directory import DirectoryCreate, DirectoryUpdate, PathValidationRequest
from app.schemas.settings import SystemSettingCreate
from app.schemas.verification import VerificationRequest


def test_api_router_and_health_are_registered() -> None:
    assert api_router is not None
    assert health_check() == {"status": "ok"}


def test_directory_repository_and_endpoints(tmp_path) -> None:
    db = FakeDB()
    directory = MonitoredDirectory(id=1, name="Dataset", path=str(tmp_path), description=None, is_active=1, created_at="now", updated_at="now")
    db.seed(MonitoredDirectory, [directory])

    assert list_directories(db) == [directory]
    assert get_directory(db, 1) == directory
    assert list_directory_endpoint(db=db) == [directory]
    assert get_directory_endpoint(1, db=db) == directory
    assert update_directory_endpoint(1, DirectoryUpdate(name="Updated"), db=db).name == "Updated"
    delete_directory_endpoint(1, db=db)
    assert db.deleted == [directory]


def test_directory_endpoints_raise_not_found() -> None:
    db = FakeDB()
    with pytest.raises(HTTPException) as detail_exc:
        get_directory_endpoint(999, db=db)
    assert detail_exc.value.status_code == 404

    with pytest.raises(HTTPException) as update_exc:
        update_directory_endpoint(999, DirectoryUpdate(name="x"), db=db)
    assert update_exc.value.status_code == 404

    with pytest.raises(HTTPException) as delete_exc:
        delete_directory_endpoint(999, db=db)
    assert delete_exc.value.status_code == 404


def test_create_directory_and_validate_path_endpoint(tmp_path) -> None:
    db = FakeDB()
    created = create_directory_endpoint(DirectoryCreate(name="Dataset", path=str(tmp_path)), db=db)
    assert created.name == "Dataset"

    valid = validate_path_endpoint(PathValidationRequest(path=str(tmp_path)))
    assert valid.valid is True

    invalid = validate_path_endpoint(PathValidationRequest(path=str(tmp_path / "missing")))
    assert invalid.valid is False


def test_baseline_repository_and_endpoint(monkeypatch, tmp_path) -> None:
    db = FakeDB()
    directory = MonitoredDirectory(id=1, name="Dataset", path=str(tmp_path), description=None, is_active=1, created_at="now", updated_at="now")
    baseline = BaselineFile(
        id=1,
        monitored_directory_id=1,
        relative_path="a.txt",
        absolute_path=str(tmp_path / "a.txt"),
        file_size_bytes=1,
        last_modified_at="now",
        algorithm="SHA-256",
        algorithm_params="{}",
        hash_value="hash",
        hash_duration_ms=1,
        baseline_created_at="now",
        created_at="now",
        updated_at="now",
    )
    db.seed(MonitoredDirectory, [directory])
    db.seed(BaselineFile, [baseline])

    assert list_baseline_files(db, directory_id=1, algorithm="SHA-256") == [baseline]
    assert list_baseline_files_endpoint(directory_id=1, algorithm="SHA-256", db=db) == [baseline]

    monkeypatch.setattr("app.api.v1.baselines.generate_baseline", lambda db, directory, algorithm, params: ([baseline], 1, 2))
    response = generate_baseline_endpoint(BaselineGenerateRequest(monitored_directory_id=1), db=db)
    assert response.total_files == 1
    assert response.total_size_bytes == 1


def test_baseline_endpoint_not_found() -> None:
    with pytest.raises(HTTPException) as exc:
        generate_baseline_endpoint(BaselineGenerateRequest(monitored_directory_id=404), db=FakeDB())
    assert exc.value.status_code == 404


def test_logs_repository_and_endpoints() -> None:
    db = FakeDB()
    log = IntegrityLog(id=1, monitored_directory_id=1, baseline_file_id=None, event_type="ADDED", relative_path="a.txt", previous_hash=None, current_hash="hash", previous_size_bytes=None, current_size_bytes=1, previous_modified_at=None, current_modified_at="now", severity="MEDIUM", status="OPEN", message="added", checked_at="now", verification_duration_ms=1, created_at="now")
    db.seed(IntegrityLog, [log])

    assert list_logs(db, directory_id=1, event_type="ADDED") == [log]
    assert list_integrity_logs_endpoint(directory_id=1, event_type="ADDED", db=db) == [log]
    assert list_verification_logs_endpoint(directory_id=1, event_type="ADDED", db=db) == [log]


def test_verification_endpoint(monkeypatch, tmp_path) -> None:
    db = FakeDB()
    directory = MonitoredDirectory(id=1, name="Dataset", path=str(tmp_path), description=None, is_active=1, created_at="now", updated_at="now")
    log = IntegrityLog(id=1, monitored_directory_id=1, baseline_file_id=None, event_type="ADDED", relative_path="a.txt", previous_hash=None, current_hash="hash", previous_size_bytes=None, current_size_bytes=1, previous_modified_at=None, current_modified_at="now", severity="MEDIUM", status="OPEN", message="added", checked_at="now", verification_duration_ms=1, created_at="now")
    db.seed(MonitoredDirectory, [directory])
    counts = {"UNCHANGED": 0, "MODIFIED": 0, "ADDED": 1, "DELETED": 0, "ERROR": 0}
    monkeypatch.setattr("app.api.v1.verifications.verify_directory", lambda db, directory, algorithm: ([log], counts, 5))

    response = run_verification_endpoint(VerificationRequest(monitored_directory_id=1), db=db)

    assert response.total_checked == 1
    assert response.added_count == 1


def test_verification_endpoint_not_found() -> None:
    with pytest.raises(HTTPException) as exc:
        run_verification_endpoint(VerificationRequest(monitored_directory_id=404), db=FakeDB())
    assert exc.value.status_code == 404


def test_benchmark_and_settings_endpoints() -> None:
    db = FakeDB()
    benchmark = BenchmarkResult(id=1, monitored_directory_id=1, algorithm="SHA-256", algorithm_params="{}", total_files=1, total_size_bytes=1, total_duration_ms=1, average_duration_ms=1.0, min_duration_ms=1.0, max_duration_ms=1.0, throughput_mb_per_sec=1.0, benchmark_started_at="now", benchmark_finished_at="now", created_at="now")
    setting = SystemSetting(id=1, setting_key="default_hash_algorithm", setting_value="SHA-256", value_type="string", description=None, is_editable=1, created_at="now", updated_at="now")
    db.seed(BenchmarkResult, [benchmark])
    db.seed(SystemSetting, [setting])

    assert list_benchmarks_endpoint(db=db) == [benchmark]
    assert list_settings_endpoint(db=db) == [setting]
    created = create_setting_endpoint(SystemSettingCreate(setting_key="scan_hidden_files", setting_value="true", value_type="boolean"), db=db)
    assert created.setting_key == "scan_hidden_files"


def test_benchmark_request_schema_defaults() -> None:
    request = BenchmarkRequest(monitored_directory_id=1)
    assert request.algorithms == ["SHA-256", "PBKDF2", "Argon2id"]
