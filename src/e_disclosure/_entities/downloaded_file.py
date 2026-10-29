from dataclasses import dataclass


@dataclass(frozen=True)
class DownloadedFile:
    name: str
    body: bytes
