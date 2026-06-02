"""Hashing helpers for the File Integrity Monitoring backend.

This module contains algorithm-specific hash generation functions used by the
baseline, verification, and benchmark services. The functions accept in-memory
file bytes and return hexadecimal hash strings.
"""

import hashlib
from collections.abc import Callable

from argon2.exceptions import HashingError
from argon2.low_level import Type, hash_secret_raw

BytesLike = bytes | bytearray | memoryview


def _ensure_bytes(value: BytesLike, field_name: str, allow_empty: bool = True) -> bytes:
    """Validate and normalize bytes-like input.

    Args:
        value: Value that should contain bytes.
        field_name: Human-readable field name for error messages.
        allow_empty: Whether empty bytes are accepted.

    Returns:
        The normalized immutable bytes value.

    Raises:
        TypeError: If the value is not bytes-like.
        ValueError: If the value is empty while ``allow_empty`` is false.
    """
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f"{field_name} must be bytes, bytearray, or memoryview")

    normalized = bytes(value)
    if not allow_empty and not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _ensure_positive_int(value: int, field_name: str) -> int:
    """Validate a positive integer parameter.

    Args:
        value: Integer value to validate.
        field_name: Human-readable field name for error messages.

    Returns:
        The validated integer.

    Raises:
        TypeError: If the value is not an integer.
        ValueError: If the value is less than 1.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value < 1:
        raise ValueError(f"{field_name} must be greater than 0")
    return value


def _normalize_salt(salt: BytesLike | str, field_name: str = "salt") -> bytes:
    """Validate and normalize a salt value.

    Args:
        salt: Salt as bytes-like data or string.
        field_name: Human-readable field name for error messages.

    Returns:
        Salt encoded as bytes.

    Raises:
        TypeError: If the salt is neither string nor bytes-like.
        ValueError: If the salt is empty.
    """
    if isinstance(salt, str):
        salt = salt.encode()
    return _ensure_bytes(salt, field_name, allow_empty=False)


def _wrap_hash_error(generator: Callable[[], str], algorithm: str) -> str:
    """Convert low-level hashing errors into clear ValueError messages.

    Args:
        generator: Zero-argument callable that performs hashing.
        algorithm: Algorithm name used in the error message.

    Returns:
        Hexadecimal hash string returned by the generator.

    Raises:
        ValueError: If the hashing operation fails.
    """
    try:
        return generator()
    except (HashingError, OSError, OverflowError, ValueError) as exc:
        raise ValueError(f"Failed to generate {algorithm} hash: {exc}") from exc


def generate_sha256(data: BytesLike) -> str:
    """Generate a SHA-256 hash for file content.

    Args:
        data: File content as bytes, bytearray, or memoryview.

    Returns:
        SHA-256 digest encoded as a lowercase hexadecimal string.

    Raises:
        TypeError: If data is not bytes-like.
        ValueError: If hashing fails. Empty file content is valid and supported.
    """
    normalized_data = _ensure_bytes(data, "data")
    return _wrap_hash_error(lambda: hashlib.sha256(normalized_data).hexdigest(), "SHA-256")


def generate_pbkdf2(
    data: BytesLike,
    salt: BytesLike | str,
    iterations: int = 100_000,
    dklen: int = 32,
    hash_name: str = "sha256",
) -> str:
    """Generate a PBKDF2-HMAC derived hash for file content.

    Args:
        data: File content as bytes, bytearray, or memoryview.
        salt: Salt as bytes-like data or string.
        iterations: PBKDF2 iteration count. Must be greater than 0.
        dklen: Desired derived key length in bytes. Must be greater than 0.
        hash_name: Hash function name accepted by ``hashlib.pbkdf2_hmac``.

    Returns:
        PBKDF2-HMAC output encoded as a lowercase hexadecimal string.

    Raises:
        TypeError: If data/salt/hash_name/parameters have invalid types.
        ValueError: If salt is empty, numeric parameters are invalid, or
            hashlib cannot generate the requested PBKDF2 output.
    """
    normalized_data = _ensure_bytes(data, "data")
    normalized_salt = _normalize_salt(salt)
    normalized_iterations = _ensure_positive_int(iterations, "iterations")
    normalized_dklen = _ensure_positive_int(dklen, "dklen")

    if not isinstance(hash_name, str):
        raise TypeError("hash_name must be a string")
    if not hash_name.strip():
        raise ValueError("hash_name must not be empty")

    return _wrap_hash_error(
        lambda: hashlib.pbkdf2_hmac(
            hash_name.strip(),
            normalized_data,
            normalized_salt,
            normalized_iterations,
            dklen=normalized_dklen,
        ).hex(),
        "PBKDF2",
    )


def generate_argon2id(
    data: BytesLike,
    salt: BytesLike | str,
    time_cost: int = 3,
    memory_cost: int = 65_536,
    parallelism: int = 2,
    hash_len: int = 32,
) -> str:
    """Generate an Argon2id hash for file content.

    Args:
        data: File content as bytes, bytearray, or memoryview.
        salt: Salt as bytes-like data or string. Argon2 requires a non-empty
            salt, and at least 8 bytes is recommended.
        time_cost: Number of Argon2 iterations. Must be greater than 0.
        memory_cost: Memory cost in KiB. Must be greater than 0.
        parallelism: Degree of parallelism. Must be greater than 0.
        hash_len: Output length in bytes. Must be greater than 0.

    Returns:
        Argon2id raw hash encoded as a lowercase hexadecimal string.

    Raises:
        TypeError: If data/salt/parameters have invalid types.
        ValueError: If salt is empty, numeric parameters are invalid, salt is
            too short, or argon2-cffi cannot generate the hash.
    """
    normalized_data = _ensure_bytes(data, "data")
    normalized_salt = _normalize_salt(salt)
    normalized_time_cost = _ensure_positive_int(time_cost, "time_cost")
    normalized_memory_cost = _ensure_positive_int(memory_cost, "memory_cost")
    normalized_parallelism = _ensure_positive_int(parallelism, "parallelism")
    normalized_hash_len = _ensure_positive_int(hash_len, "hash_len")

    if len(normalized_salt) < 8:
        raise ValueError("salt must be at least 8 bytes for Argon2id")

    return _wrap_hash_error(
        lambda: hash_secret_raw(
            normalized_data,
            normalized_salt,
            time_cost=normalized_time_cost,
            memory_cost=normalized_memory_cost,
            parallelism=normalized_parallelism,
            hash_len=normalized_hash_len,
            type=Type.ID,
        ).hex(),
        "Argon2id",
    )
