import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from patchright.async_api import Page

type ReportType = Literal[3, 4]


@dataclass
class Report:
    type: str
    period: str
    placement_date: datetime
    download_url: str


class ReportsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.rows = page.locator("table.files-table tr")

    @property
    def empty(self) -> bool:
        return "files.aspx" not in self.page.url

    async def goto(self, company_id: str, report_type: ReportType) -> None:
        await self.page.goto(
            f"https://www.e-disclosure.ru/portal/files.aspx?id={company_id}&type={report_type}"
        )

    async def find(self, predicate: Callable[[Report], bool]) -> Report | None:
        if self.empty:
            return None

        for row in await self.rows.all():
            cells = await row.locator("td").all_text_contents()
            if len(cells) < 6:
                continue

            if not re.fullmatch(r"\d+", cells[0].strip()):
                continue
            download_url = (
                await row.locator("td").nth(5).locator("a").get_attribute("href")
            )
            if not download_url:
                continue

            report = Report(
                type=cells[1].strip(),
                period=cells[2].strip(),
                placement_date=datetime.strptime(cells[4].strip(), "%d.%m.%Y"),
                download_url=download_url,
            )

            if predicate(report):
                return report

        return None
