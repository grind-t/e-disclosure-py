import subprocess
import tempfile
from pathlib import Path

from toolkit.boolean import ensure

from e_disclosure._entities.downloaded_file import DownloadedFile


def unpack_pdfs(file: DownloadedFile) -> list[DownloadedFile]:
    """PDF любой вложенности из архива ``.zip`` или ``.rar``; иной файл как есть."""
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

        return ensure(
            [
                DownloadedFile(name=entry.name, body=entry.read_bytes())
                for entry in sorted(extract_dir.rglob("*"))
                if entry.is_file() and entry.suffix.lower() == ".pdf"
            ],
            f"No PDF in archive {file.name}",
        )
