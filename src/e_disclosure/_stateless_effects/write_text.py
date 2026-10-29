from pathlib import Path, PurePath


def write_text(path: PurePath, text: str) -> None:
    Path(path).write_text(text)
