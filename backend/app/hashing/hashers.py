import json
from pathlib import Path

from app.hashing.hashing import generate_argon2id, generate_pbkdf2, generate_sha256
from app.utils.timer import Timer


def _read_file(path: str) -> bytes:
    return Path(path).read_bytes()


def normalize_algorithm(algorithm: str) -> str:
    value = algorithm.strip().upper()
    if value in {"SHA256", "SHA-256"}:
        return "SHA-256"
    if value == "PBKDF2":
        return "PBKDF2"
    if value in {"ARGON2ID", "ARGON2ID"}:
        return "Argon2id"
    raise ValueError(f"Unsupported algorithm: {algorithm}")


def default_params(algorithm: str) -> dict:
    normalized = normalize_algorithm(algorithm)
    if normalized == "PBKDF2":
        return {"hash_name": "sha256", "iterations": 100000, "salt": "fim-static-salt", "dklen": 32}
    if normalized == "Argon2id":
        return {"time_cost": 3, "memory_cost": 65536, "parallelism": 2, "hash_len": 32, "salt": "fim-static-salt-16"}
    return {}


def hash_file(path: str, algorithm: str, params: dict | None = None) -> tuple[str, int, dict]:
    normalized = normalize_algorithm(algorithm)
    effective_params = default_params(normalized)
    if params:
        effective_params.update(params)

    with Timer() as timer:
        data = _read_file(path)
        if normalized == "SHA-256":
            digest = generate_sha256(data)
        elif normalized == "PBKDF2":
            digest = generate_pbkdf2(
                data,
                salt=effective_params["salt"],
                iterations=int(effective_params["iterations"]),
                dklen=int(effective_params["dklen"]),
                hash_name=effective_params["hash_name"],
            )
        else:
            digest = generate_argon2id(
                data,
                salt=effective_params["salt"],
                time_cost=int(effective_params["time_cost"]),
                memory_cost=int(effective_params["memory_cost"]),
                parallelism=int(effective_params["parallelism"]),
                hash_len=int(effective_params["hash_len"]),
            )
    return digest, timer.duration_ms, effective_params


def params_to_json(params: dict | None) -> str:
    return json.dumps(params or {}, sort_keys=True)


def params_from_json(raw: str | None) -> dict:
    if not raw:
        return {}
    return json.loads(raw)
