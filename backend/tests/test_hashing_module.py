import hashlib

import pytest

from app.hashing.hashing import generate_argon2id, generate_pbkdf2, generate_sha256


def test_generate_sha256_matches_hashlib() -> None:
    assert generate_sha256(b"fim") == hashlib.sha256(b"fim").hexdigest()


def test_generate_sha256_accepts_empty_file_content() -> None:
    assert generate_sha256(b"") == hashlib.sha256(b"").hexdigest()


def test_generate_sha256_rejects_non_bytes() -> None:
    with pytest.raises(TypeError, match="data must be bytes"):
        generate_sha256("fim")  # type: ignore[arg-type]


def test_generate_pbkdf2_matches_hashlib() -> None:
    expected = hashlib.pbkdf2_hmac("sha256", b"fim", b"salt", 10, dklen=16).hex()
    assert generate_pbkdf2(b"fim", "salt", iterations=10, dklen=16) == expected


@pytest.mark.parametrize(
    ("kwargs", "error"),
    [
        ({"salt": ""}, "salt must not be empty"),
        ({"salt": "salt", "iterations": 0}, "iterations must be greater than 0"),
        ({"salt": "salt", "dklen": 0}, "dklen must be greater than 0"),
        ({"salt": "salt", "hash_name": ""}, "hash_name must not be empty"),
        ({"salt": "salt", "hash_name": "missing-hash"}, "Failed to generate PBKDF2"),
    ],
)
def test_generate_pbkdf2_error_handling(kwargs: dict, error: str) -> None:
    with pytest.raises(ValueError, match=error):
        generate_pbkdf2(b"fim", **kwargs)


def test_generate_pbkdf2_rejects_bad_hash_name_type() -> None:
    with pytest.raises(TypeError, match="hash_name must be a string"):
        generate_pbkdf2(b"fim", "salt", hash_name=123)  # type: ignore[arg-type]


def test_generate_argon2id_is_deterministic() -> None:
    first = generate_argon2id(b"fim", "12345678", time_cost=1, memory_cost=8, parallelism=1, hash_len=16)
    second = generate_argon2id(b"fim", "12345678", time_cost=1, memory_cost=8, parallelism=1, hash_len=16)
    assert first == second
    assert len(first) == 32


@pytest.mark.parametrize(
    ("kwargs", "error"),
    [
        ({"salt": "short"}, "salt must be at least 8 bytes"),
        ({"salt": "12345678", "time_cost": 0}, "time_cost must be greater than 0"),
        ({"salt": "12345678", "memory_cost": 0}, "memory_cost must be greater than 0"),
        ({"salt": "12345678", "parallelism": 0}, "parallelism must be greater than 0"),
        ({"salt": "12345678", "hash_len": 0}, "hash_len must be greater than 0"),
    ],
)
def test_generate_argon2id_error_handling(kwargs: dict, error: str) -> None:
    with pytest.raises(ValueError, match=error):
        generate_argon2id(b"fim", **kwargs)
