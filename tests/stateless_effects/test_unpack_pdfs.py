import io
import zipfile

import pytest

from e_disclosure._entities.downloaded_file import DownloadedFile
from e_disclosure._stateless_effects.unpack_pdfs import unpack_pdfs


def _zip(entries: dict[str, bytes]) -> DownloadedFile:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, body in entries.items():
            archive.writestr(name, body)
    return DownloadedFile(name="report.zip", body=buffer.getvalue())


def test_archive_yields_pdfs_at_any_depth() -> None:
    archive = _zip(
        {
            "top.pdf": b"top",
            "МСФО/2026/nested.PDF": b"nested",
            "МСФО/readme.txt": b"skip",
        }
    )

    assert unpack_pdfs(archive) == [
        DownloadedFile(name="top.pdf", body=b"top"),
        DownloadedFile(name="nested.PDF", body=b"nested"),
    ]


def test_archive_without_pdfs_is_rejected() -> None:
    with pytest.raises(ValueError, match="No PDF"):
        unpack_pdfs(_zip({"readme.txt": b"skip"}))
