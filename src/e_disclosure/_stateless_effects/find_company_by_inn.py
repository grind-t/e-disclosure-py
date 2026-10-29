from patchright.async_api import Page

from e_disclosure._entities.company import Company
from e_disclosure._stateless_computations.parse_company_id import parse_company_id


async def find_company_by_inn(page: Page, inn: str) -> Company | None:
    await page.goto("https://www.e-disclosure.ru/poisk-po-kompaniyam")
    await page.locator("#textfield").fill(inn)
    await page.locator("#sendButton").click()

    link = page.locator('a[href*="company.aspx?id="]').first
    href = await link.get_attribute("href")
    company_id = href and parse_company_id(page.url, href)
    if not company_id:
        return None

    name = ((await link.text_content()) or "").strip() or inn
    return Company(id=company_id, name=name)
