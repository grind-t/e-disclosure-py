from collections.abc import Awaitable, Callable

from e_disclosure._entities.downloaded_file import DownloadedFile
from e_disclosure._entities.msfo_report import MsfoReport
from e_disclosure._entities.rated_company import RatedCompany
from e_disclosure._stateless_computations.export_file_names import export_file_names
from e_disclosure._stateless_computations.with_pending_rating import (
    with_pending_rating,
)


async def pull_msfo_report(
    inn: str,
    period: str | None,
    *,
    get_msfo_report: Callable[[str, str | None], Awaitable[MsfoReport | None]],
    unpack_files: Callable[[DownloadedFile], list[DownloadedFile]],
    write_export: Callable[[str, bytes], None],
    read_companies: Callable[[], dict[str, RatedCompany]],
    write_companies: Callable[[dict[str, RatedCompany]], None],
) -> MsfoReport | None:
    """Сохранить файлы отчёта в exports; последний отчёт заводит неоценённый период."""
    report = await get_msfo_report(inn, period)
    if not report:
        return None

    files = unpack_files(report.file)
    for name, file in zip(
        export_file_names(inn, report.period, files), files, strict=True
    ):
        write_export(name, file.body)
    # Отчёт за прошлый период дополняет анализ и не заводит новый рейтинг
    if period is None:
        write_companies(with_pending_rating(read_companies(), inn, report))
    return report
