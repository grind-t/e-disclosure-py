import subprocess
import tempfile
from pathlib import Path

from e_disclosure._entities.downloaded_file import DownloadedFile


def unpack_files(file: DownloadedFile) -> list[DownloadedFile]:
    """Файлы верхнего уровня архива ``.zip`` или ``.rar``; иной файл как есть."""
    with tempfile.TemporaryDirectory(prefix="e-disclosure-") as tmp:
        archive = Path(tmp) / file.name
        extract_dir = Path(tmp) / "extracted"
        archive.write_bytes(file.body)

        match archive.suffix:
            case ".zip":
                subprocess.run(["unzip", "-o", archive, "-d", extract_dir], check=True)
            case ".rar":
                subprocess.run(
                    ["7z", "x", f"-o{extract_dir}", "-y", archive], check=True
                )
            case _:
                return [file]

        return [
            DownloadedFile(name=entry.name, body=entry.read_bytes())
            for entry in sorted(extract_dir.iterdir())
            if entry.is_file()
        ]
