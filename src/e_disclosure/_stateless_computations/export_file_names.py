from pathlib import PurePath

from e_disclosure._entities.downloaded_file import DownloadedFile


def export_file_names(inn: str, period: str, files: list[DownloadedFile]) -> list[str]:
    """Имена вида ``ИНН (период).ext`` с номером, если файлов несколько."""
    return [
        f"{inn} ({period}){f' ({index + 1})' if len(files) > 1 else ''}"
        f"{PurePath(file.name).suffix}"
        for index, file in enumerate(files)
    ]
