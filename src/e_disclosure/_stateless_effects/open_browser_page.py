from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from patchright.async_api import Page, async_playwright


@asynccontextmanager
async def open_browser_page(session_dir: Path) -> AsyncIterator[Page]:
    """Страница Chrome с профилем из ``session_dir``, чтобы пройти защиту от ботов."""
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            session_dir, channel="chrome", headless=False, no_viewport=True
        )
        try:
            yield browser.pages[0] if browser.pages else await browser.new_page()
        finally:
            await browser.close()
