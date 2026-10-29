from email.message import Message

from patchright.async_api import Page

from e_disclosure._entities.downloaded_file import DownloadedFile


async def download_file(page: Page, url: str) -> DownloadedFile:
    """Файл с именем из ``Content-Disposition``, скачанный в сессии браузера."""
    # Крупные архивы не успевают скачаться за таймаут по умолчанию (30 с)
    response = await page.request.get(url, timeout=300_000)
    disposition = Message()
    disposition["content-disposition"] = response.headers["content-disposition"]
    name = disposition.get_filename()
    if not name:
        raise ValueError(f"No filename in Content-Disposition for {url}")
    return DownloadedFile(name=name, body=await response.body())
