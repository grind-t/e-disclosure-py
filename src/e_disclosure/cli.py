import argparse
import asyncio
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import brotli
from patchright.async_api import async_playwright

from e_disclosure.get_latest_msfo_report import MsfoReport, get_latest_msfo_report


def main() -> None:
    parser = argparse.ArgumentParser(prog="e-disclosure")
    parser.add_argument("--exports-dir", type=Path, default=Path("exports"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    pull_report = subparsers.add_parser(
        "pull-report", help="скачать последний МСФО-отчёт по ИНН"
    )
    pull_report.add_argument("inn")
    pull_report.add_argument("--session-dir", type=Path, default=Path(".session"))

    subparsers.add_parser(
        "export-ratings", help="собрать ratings.json.br из companies.json"
    )

    args = parser.parse_args()

    if args.command == "pull-report":
        asyncio.run(pull_msfo_report(args.inn, args.exports_dir, args.session_dir))
    else:
        export_ratings(args.exports_dir)


async def pull_msfo_report(inn: str, exports_dir: Path, session_dir: Path) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            session_dir, channel="chrome", headless=False, no_viewport=True
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        report = await get_latest_msfo_report(page, inn)
        await browser.close()

    if not report:
        print("Отчет не найден")
        return

    export_report(inn, report, exports_dir)
    update_company(inn, report, exports_dir)


def export_report(inn: str, report: MsfoReport, exports_dir: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="e-disclosure-") as tmp:
        tmp_dir = Path(tmp)
        extract_dir = tmp_dir / "extracted"
        source_file_path = tmp_dir / report.file_name
        source_file_path.write_bytes(report.body)

        match source_file_path.suffix:
            case ".zip":
                subprocess.run(
                    ["unzip", "-o", source_file_path, "-d", extract_dir], check=True
                )
            case ".rar":
                subprocess.run(
                    ["7z", "x", f"-o{extract_dir}", "-y", source_file_path], check=True
                )
            case _:
                extract_dir.mkdir()
                shutil.copy(source_file_path, extract_dir / report.file_name)

        top_level_files = sorted(
            entry for entry in extract_dir.iterdir() if entry.is_file()
        )

        for index, entry in enumerate(top_level_files):
            suffix = f" ({index + 1})" if len(top_level_files) > 1 else ""
            new_name = f"{inn} ({report.period}){suffix}{entry.suffix}"
            shutil.copy(entry, exports_dir / new_name)


def update_company(inn: str, report: MsfoReport, exports_dir: Path) -> None:
    companies_path = exports_dir / "companies.json"
    companies = json.loads(companies_path.read_text())

    company = companies.setdefault(
        inn, {"id": report.company_id, "ratings": [], "reportType": report.type}
    )
    company["ratings"].append({"period": report.period, "value": 0, "outlook": ""})

    companies_path.write_text(
        json.dumps(companies, ensure_ascii=False, indent=2) + "\n"
    )


def export_ratings(exports_dir: Path) -> None:
    companies = json.loads((exports_dir / "companies.json").read_text())
    ratings = {}

    for inn, company in companies.items():
        latest = company["ratings"][-1]
        ratings[inn] = {k: latest[k] for k in ("value", "outlook") if k in latest}

    data = json.dumps(ratings, ensure_ascii=False, separators=(",", ":"))
    (exports_dir / "ratings.json.br").write_bytes(brotli.compress(data.encode()))
