from dataclasses import dataclass
from urllib.parse import parse_qs, urljoin, urlparse

from patchright.async_api import Page


@dataclass
class Company:
    id: str
    name: str


class SearchCompaniesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.input = page.locator("#textfield")
        self.submit = page.locator("#sendButton")
        self.item_link = page.locator('a[href*="company.aspx?id="]')

    async def goto(self) -> None:
        await self.page.goto("https://www.e-disclosure.ru/poisk-po-kompaniyam")

    async def find_company_by_inn(self, inn: str) -> Company | None:
        await self.input.fill(inn)
        await self.submit.click()

        company = self.item_link.first
        href = await company.get_attribute("href")
        if not href:
            return None

        ids = parse_qs(urlparse(urljoin(self.page.url, href)).query).get("id")
        name = ((await company.text_content()) or "").strip() or inn

        return Company(id=ids[0], name=name) if ids else None
