from e_disclosure._entities.downloaded_file import DownloadedFile
from e_disclosure._entities.msfo_report import MsfoReport
from e_disclosure._entities.rated_company import RatedCompany
from e_disclosure._entities.report_type import ReportType
from e_disclosure._stateless_workflows.pull_msfo_report import pull_msfo_report

ARCHIVE = DownloadedFile(name="report.zip", body=b"zip")
REPORT = MsfoReport(
    company_id="42",
    type=ReportType.CONSOLIDATED,
    period="2026, 6 месяцев",
    file=ARCHIVE,
)
UNPACKED = [
    DownloadedFile(name="a.pdf", body=b"pdf"),
    DownloadedFile(name="b.xlsx", body=b"xlsx"),
]


async def _pull(
    period: str | None, companies: dict[str, RatedCompany]
) -> tuple[dict[str, bytes], dict[str, RatedCompany]]:
    exports: dict[str, bytes] = {}

    async def get_msfo_report(inn: str, period: str | None) -> MsfoReport | None:
        return REPORT

    def unpack_files(file: DownloadedFile) -> list[DownloadedFile]:
        assert file == ARCHIVE
        return UNPACKED

    def write_companies(updated: dict[str, RatedCompany]) -> None:
        companies.clear()
        companies.update(updated)

    await pull_msfo_report(
        "7700",
        period,
        get_msfo_report=get_msfo_report,
        unpack_files=unpack_files,
        write_export=exports.__setitem__,
        read_companies=lambda: dict(companies),
        write_companies=write_companies,
    )
    return exports, companies


async def test_latest_report_adds_pending_period_to_new_company() -> None:
    exports, companies = await _pull(None, {})

    assert exports == {
        "7700 (2026, 6 месяцев) (1).pdf": b"pdf",
        "7700 (2026, 6 месяцев) (2).xlsx": b"xlsx",
    }
    assert companies == {
        "7700": {
            "id": "42",
            "ratings": [{"period": "2026, 6 месяцев", "value": 0, "outlook": ""}],
            "reportType": ReportType.CONSOLIDATED,
        }
    }


async def test_past_period_report_keeps_companies() -> None:
    _, companies = await _pull("2026, 6 месяцев", {})

    assert companies == {}
