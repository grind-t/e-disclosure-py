from pathlib import Path


def write_export(exports_dir: Path, name: str, data: bytes) -> None:
    (exports_dir / name).write_bytes(data)
