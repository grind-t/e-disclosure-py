"""Скачать МСФО-отчёт компании по ИНН в exports.

Печатает JSON с ``companyId``, ``reportType`` и ``period`` скачанного отчёта.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path, PurePath

from patchright.async_api import async_playwright

from e_disclosure import MsfoReport, get_msfo_report

PROJECT_DIR = Path(__file__).resolve().parent.parent
EXPORTS_DIR = PROJECT_DIR / "exports"
SESSION_DIR = PROJECT_DIR / ".session"


def export_file_names(inn: str, report: MsfoReport) -> list[str]:
    """Имена вида ``ИНН (период).ext`` с номером, если файлов несколько."""
    numbered = len(report.files) > 1
    return [
        f"{inn} ({report.period}){f' ({index + 1})' if numbered else ''}"
        f"{PurePath(file.name).suffix}"
        for index, file in enumerate(report.files)
    ]


async def pull_report(inn: str, period: str | None) -> MsfoReport | None:
    """Отчёт через Chrome с профилем ``SESSION_DIR``, чтобы пройти защиту от ботов."""
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            SESSION_DIR, channel="chrome", headless=False, no_viewport=True
        )
        try:
            page = browser.pages[0] if browser.pages else await browser.new_page()
            return await get_msfo_report(page, inn, period)
        finally:
            await browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inn")
    parser.add_argument(
        "--period", help="период отчёта, например 2025; без него — последний отчёт"
    )
    args = parser.parse_args()

    try:
        report = asyncio.run(pull_report(args.inn, args.period))
    except ValueError as error:
        sys.exit(str(error))
    if not report:
        sys.exit("Отчет не найден")

    for name, file in zip(
        export_file_names(args.inn, report), report.files, strict=True
    ):
        (EXPORTS_DIR / name).write_bytes(file.body)
    print(
        json.dumps(
            {
                "companyId": report.company_id,
                "reportType": report.type,
                "period": report.period,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
