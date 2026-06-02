from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScannedFile:
    relative_path: str
    absolute_path: str
    file_size_bytes: int
    last_modified_at: str


def scan_directory(directory_path: str) -> list[ScannedFile]:
    root = Path(directory_path).expanduser().resolve()
    files: list[ScannedFile] = []
    for item in sorted(root.rglob("*")):
        if not item.is_file():
            continue
        stat = item.stat()
        files.append(
            ScannedFile(
                relative_path=item.relative_to(root).as_posix(),
                absolute_path=str(item),
                file_size_bytes=stat.st_size,
                last_modified_at=str(stat.st_mtime),
            )
        )
    return files
