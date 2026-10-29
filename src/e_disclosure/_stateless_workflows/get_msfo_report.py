from collections.abc import Awaitable, Callable

from e_disclosure._entities.company import Company
from e_disclosure._entities.downloaded_file import DownloadedFile
from e_disclosure._entities.msfo_report import MsfoReport
from e_disclosure._entities.report import Report
from e_disclosure._entities.report_type import ReportType
from e_disclosure._stateless_computations.select_msfo_report import (
    select_msfo_report,
)


async def get_msfo_report(
    inn: str,
    period: str | None,
    *,
    find_company_by_inn: Callable[[str], Awaitable[Company | None]],
    list_reports: Callable[[str, ReportType], Awaitable[list[Report]]],
    download_file: Callable[[str], Awaitable[DownloadedFile]],
    unpack_report_archive: Callable[[DownloadedFile], list[DownloadedFile]],
) -> MsfoReport | None:
    """Последний МСФО-отчёт компании, или последний за ``period``, если он задан."""
    company = await find_company_by_inn(inn)
    if not company:
        return None

    # При равной дате размещения выигрывает вкладка, идущая раньше
    reports = {
        report_type: await list_reports(company.id, report_type)
        for report_type in (ReportType.CONSOLIDATED, ReportType.ACCOUNTING)
    }
    selected = select_msfo_report(reports, period)
    if not selected:
        return None

    report_type, report = selected
    return MsfoReport(
        company_id=company.id,
        type=report_type,
        period=report.period,
        files=unpack_report_archive(await download_file(report.download_url)),
    )
