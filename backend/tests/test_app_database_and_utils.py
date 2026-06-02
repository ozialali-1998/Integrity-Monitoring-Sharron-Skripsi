from app.core.config import settings
from app.core.constants import FILE_EVENTS, LOG_STATUSES, SUPPORTED_ALGORITHMS
from app.db.database import get_db, init_db
from app.main import app, on_startup
from app.utils.time import utc_now
from app.utils.timer import Timer


def test_settings_and_constants() -> None:
    assert settings.app_name == "FIM Security Monitor"
    assert settings.api_v1_prefix == "/api/v1"
    assert "SHA-256" in SUPPORTED_ALGORITHMS
    assert "MODIFIED" in FILE_EVENTS
    assert "OPEN" in LOG_STATUSES


def test_app_configuration_and_startup() -> None:
    assert app.title == "FIM Security Monitor"
    on_startup()
    init_db()


def test_get_db_yields_and_closes_session() -> None:
    generator = get_db()
    db = next(generator)
    assert db is not None
    try:
        next(generator)
    except StopIteration:
        pass


def test_utc_now_returns_iso_string() -> None:
    assert "T" in utc_now()


def test_timer_measures_duration() -> None:
    with Timer() as timer:
        sum(range(10))
    assert timer.duration_ms >= 0
