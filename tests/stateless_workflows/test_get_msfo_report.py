from datetime import date

from e_disclosure._entities.company import Company
from e_disclosure._entities.downloaded_file import DownloadedFile
from e_disclosure._entities.msfo_report import MsfoReport
from e_disclosure._entities.report import Report
from e_disclosure._entities.report_type import ReportType
from e_disclosure._stateless_workflows.get_msfo_report import get_msfo_report

COMPANY = Company(id="42", name="ПАО Компания")


def _report(type_: str, period: str, placed: date) -> Report:
    return Report(
        type=type_, period=period, placement_date=placed, download_url=f"{period}.zip"
    )


REPORTS = {
    ReportType.CONSOLIDATED: [
        _report("Консолидированная", "2026, 6 месяцев", date(2026, 8, 30)),
        _report("Консолидированная", "2025", date(2026, 4, 30)),
    ],
    ReportType.ACCOUNTING: [
        _report("РСБУ", "2026, 9 месяцев", date(2026, 10, 30)),
        _report("Индивидуальная МСФО", "2025", date(2026, 5, 15)),
    ],
}


async def _get(inn: str, period: str | None) -> MsfoReport | None:
    async def find_company_by_inn(query: str) -> Company | None:
        return COMPANY if query == inn else None

    async def list_reports(company_id: str, report_type: ReportType) -> list[Report]:
        assert company_id == COMPANY.id
        return REPORTS[report_type]

    async def download_file(url: str) -> DownloadedFile:
        return DownloadedFile(name=url, body=b"")

    return await get_msfo_report(
        inn,
        period,
        find_company_by_inn=find_company_by_inn,
        list_reports=list_reports,
        download_file=download_file,
        unpack_report_archive=lambda file: [file],
    )


async def test_latest_skips_non_msfo_accounting_reports() -> None:
    report = await _get("7700", None)

    assert report == MsfoReport(
        company_id="42",
        type=ReportType.CONSOLIDATED,
        period="2026, 6 месяцев",
        files=[DownloadedFile(name="2026, 6 месяцев.zip", body=b"")],
    )


async def test_period_picks_latest_placed_across_tabs() -> None:
    report = await _get("7700", "2025")

    assert report is not None
    assert (report.type, report.period) == (ReportType.ACCOUNTING, "2025")


async def test_period_without_reports() -> None:
    assert await _get("7700", "2024") is None
