from patchright.async_api import Page
from toolkit.boolean import ensure

from e_disclosure._entities.company import Company
from e_disclosure._stateless_computations.parse_company_id import parse_company_id


async def find_company_by_inn(page: Page, inn: str) -> Company | None:
    await page.goto("https://www.e-disclosure.ru/poisk-po-kompaniyam")
    await page.locator("#textfield").fill(inn)
    await page.locator("#sendButton").click()

    # Блок появляется после ответа поиска, даже если ничего не найдено
    await page.locator("#searchResults .infoblock").wait_for()
    link = page.locator('a[href*="company.aspx?id="]')
    count = await link.count()
    ensure(count <= 1, f"Search by INN {inn} found several companies")
    if not count:
        return None

    href = await link.get_attribute("href")
    company_id = href and parse_company_id(page.url, href)
    if not company_id:
        return None

    name = ((await link.text_content()) or "").strip() or inn
    return Company(id=company_id, name=name)
