from pathlib import Path

from app.core.config import settings


def validate_directory_path(path: str) -> Path:
    resolved = Path(path).expanduser().resolve()
    if not resolved.exists():
        raise ValueError("Directory path does not exist")
    if not resolved.is_dir():
        raise ValueError("Path is not a directory")
    base_path = settings.default_allowed_base_path.strip()
    if base_path:
        base = Path(base_path).expanduser().resolve()
        if resolved != base and base not in resolved.parents:
            raise ValueError("Directory path is outside the allowed base path")
    return resolved
