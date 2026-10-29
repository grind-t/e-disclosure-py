from patchright.async_api import Page

from e_disclosure._entities.report import Report
from e_disclosure._entities.report_type import ReportType
from e_disclosure._stateless_computations.parse_report_row import parse_report_row


async def list_reports(
    page: Page, company_id: str, report_type: ReportType
) -> list[Report]:
    """Отчёты вкладки ``report_type`` в порядке таблицы: от новых к старым."""
    await page.goto(
        f"https://www.e-disclosure.ru/portal/files.aspx?id={company_id}&type={report_type}"
    )
    # Без отчётов на вкладке сайт уводит на другую страницу
    if "files.aspx" not in page.url:
        return []

    reports = []
    for row in await page.locator("table.files-table tr").all():
        cells = row.locator("td")
        texts = await cells.all_text_contents()
        download_url = (
            await cells.nth(5).locator("a").get_attribute("href")
            if len(texts) >= 6
            else None
        )
        if report := parse_report_row(texts, download_url):
            reports.append(report)
    return reports
