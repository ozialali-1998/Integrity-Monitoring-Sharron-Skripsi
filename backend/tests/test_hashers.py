import json
from pathlib import Path

import pytest

from app.hashing.hashers import default_params, hash_file, normalize_algorithm, params_from_json, params_to_json


def test_normalize_algorithm_supported_aliases() -> None:
    assert normalize_algorithm("sha256") == "SHA-256"
    assert normalize_algorithm("SHA-256") == "SHA-256"
    assert normalize_algorithm("PBKDF2") == "PBKDF2"
    assert normalize_algorithm("argon2id") == "Argon2id"


def test_normalize_algorithm_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="Unsupported algorithm"):
        normalize_algorithm("md5")


def test_default_params() -> None:
    assert default_params("SHA-256") == {}
    assert default_params("PBKDF2")["iterations"] == 100000
    assert default_params("Argon2id")["hash_len"] == 32


def test_hash_file_generates_digest_and_params(tmp_path: Path) -> None:
    target = tmp_path / "file.txt"
    target.write_text("fim")

    digest, duration_ms, params = hash_file(str(target), "PBKDF2", {"iterations": 1, "salt": "salt", "dklen": 8})

    assert len(digest) == 16
    assert duration_ms >= 0
    assert params["iterations"] == 1


def test_params_json_round_trip() -> None:
    raw = params_to_json({"b": 2, "a": 1})
    assert raw == json.dumps({"a": 1, "b": 2}, sort_keys=True)
    assert params_from_json(raw) == {"a": 1, "b": 2}
    assert params_from_json(None) == {}
