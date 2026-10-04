import re
from dataclasses import dataclass
from email.message import Message

from patchright.async_api import Page

from e_disclosure.pages.reports import ReportsPage, ReportType
from e_disclosure.pages.search_companies import SearchCompaniesPage


@dataclass
class MsfoReport:
    company_id: str
    type: ReportType
    period: str
    file_name: str
    body: bytes


async def get_latest_msfo_report(page: Page, inn: str) -> MsfoReport | None:
    search_companies_page = SearchCompaniesPage(page)
    await search_companies_page.goto()
    company = await search_companies_page.find_company_by_inn(inn)

    if not company:
        return None

    reports_page = ReportsPage(page)
    # Вкладка "Консолидированная" (type=4) — если есть, там уже только
    # консолидированная МСФО.
    await reports_page.goto(company.id, 4)
    consolidated_latest = await reports_page.find(lambda _: True)
    # Вкладка "Бухгалтерская (финансовая)" (type=3) может содержать МСФО-отчётность
    # (консолидированную или индивидуальную) вперемешку с обычной бухгалтерской (РСБУ) —
    # берём только строки, где тип документа упоминает МСФО.
    await reports_page.goto(company.id, 3)
    accounting_latest = await reports_page.find(
        lambda report: re.search("мсфо", report.type, re.IGNORECASE) is not None
    )
    candidates = [r for r in (consolidated_latest, accounting_latest) if r]

    if not candidates:
        return None

    report = max(candidates, key=lambda r: r.placement_date)
    response = await page.request.get(report.download_url)
    body = await response.body()
    disposition = Message()
    disposition["content-disposition"] = response.headers["content-disposition"]
    file_name = disposition.get_filename()
    if not file_name:
        raise ValueError(
            f"No filename in Content-Disposition for {report.download_url}"
        )

    return MsfoReport(
        company_id=company.id,
        type=3 if report is accounting_latest else 4,
        period=report.period,
        file_name=file_name,
        body=body,
    )
