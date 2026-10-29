import argparse
import asyncio
import os
import sys
from datetime import datetime
from functools import partial
from pathlib import Path

from patchright.async_api import Page

from e_disclosure._entities.conversion_mode import ConversionMode
from e_disclosure._entities.msfo_report import MsfoReport
from e_disclosure._entities.outlook import Outlook
from e_disclosure._stateless_effects.convert_pdf_to_html import (
    DatalabError,
    convert_pdf_to_html,
)
from e_disclosure._stateless_effects.download_file import download_file
from e_disclosure._stateless_effects.fetch_agency_ratings import fetch_agency_ratings
from e_disclosure._stateless_effects.find_company_by_inn import find_company_by_inn
from e_disclosure._stateless_effects.list_reports import list_reports
from e_disclosure._stateless_effects.open_browser_page import open_browser_page
from e_disclosure._stateless_effects.read_companies import read_companies
from e_disclosure._stateless_effects.unpack_files import unpack_files
from e_disclosure._stateless_effects.write_companies import write_companies
from e_disclosure._stateless_effects.write_export import write_export
from e_disclosure._stateless_effects.write_text import write_text
from e_disclosure._stateless_workflows.describe_agency_ratings import (
    describe_agency_ratings as _describe_agency_ratings,
)
from e_disclosure._stateless_workflows.export_ratings import (
    export_ratings as _export_ratings,
)
from e_disclosure._stateless_workflows.get_msfo_report import (
    get_msfo_report as _get_msfo_report,
)
from e_disclosure._stateless_workflows.pdf_to_html import pdf_to_html as _pdf_to_html
from e_disclosure._stateless_workflows.pull_msfo_report import (
    pull_msfo_report as _pull_msfo_report,
)
from e_disclosure._stateless_workflows.set_rating import set_rating as _set_rating


async def get_msfo_report(
    page: Page, inn: str, period: str | None = None
) -> MsfoReport | None:
    """Последний МСФО-отчёт компании, или последний за ``period``, если он задан."""
    return await _get_msfo_report(
        inn,
        period,
        find_company_by_inn=partial(find_company_by_inn, page),
        list_reports=partial(list_reports, page),
        download_file=partial(download_file, page),
    )


async def _get_msfo_report_in_browser(
    session_dir: Path, inn: str, period: str | None
) -> MsfoReport | None:
    async with open_browser_page(session_dir) as page:
        return await get_msfo_report(page, inn, period)


async def pull_msfo_report(
    inn: str, period: str | None, *, exports_dir: Path, session_dir: Path
) -> MsfoReport | None:
    """Скачать МСФО-отчёт в ``exports_dir``; без ``period`` — завести его период."""
    return await _pull_msfo_report(
        inn,
        period,
        get_msfo_report=partial(_get_msfo_report_in_browser, session_dir),
        unpack_files=unpack_files,
        write_export=partial(write_export, exports_dir),
        read_companies=partial(read_companies, exports_dir),
        write_companies=partial(write_companies, exports_dir),
    )


def set_rating(
    inn: str,
    *,
    period: str,
    rating: str,
    outlook: Outlook,
    prompt_version: int,
    model: str,
    exports_dir: Path,
) -> None:
    """Записать рейтинг вида ``ruA-`` в ``companies.json`` с сегодняшней датой."""
    _set_rating(
        inn,
        period=period,
        rating=rating,
        outlook=outlook,
        prompt_version=prompt_version,
        model=model,
        analyzed_at=datetime.now().astimezone().date(),
        read_companies=partial(read_companies, exports_dir),
        write_companies=partial(write_companies, exports_dir),
    )


def export_ratings(exports_dir: Path) -> None:
    """Собрать ``ratings.json.br`` из ``companies.json``."""
    _export_ratings(
        read_companies=partial(read_companies, exports_dir),
        write_export=partial(write_export, exports_dir),
    )


def describe_agency_ratings(queries: list[str]) -> str:
    """Рейтинги агентств из реестра ЦБ по ИНН или части названия эмитента."""
    return _describe_agency_ratings(queries, fetch_agency_ratings=fetch_agency_ratings)


def pdf_to_html(
    pdf: Path, mode: ConversionMode, *, api_key: str
) -> tuple[Path, int | None]:
    """Конвертировать PDF в HTML рядом с ним через datalab.to."""
    html_path, page_count = _pdf_to_html(
        pdf,
        mode,
        convert_pdf_to_html=partial(convert_pdf_to_html, api_key),
        write_text=write_text,
    )
    return Path(html_path), page_count


def main() -> None:
    parser = argparse.ArgumentParser(prog="e-disclosure")
    parser.add_argument("--exports-dir", type=Path, default=Path("exports"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    pull_report = subparsers.add_parser(
        "pull-report", help="скачать последний МСФО-отчёт по ИНН"
    )
    pull_report.add_argument("inn")
    pull_report.add_argument(
        "--period",
        help="период отчёта, например 2025; такой отчёт только сохраняется в exports",
    )
    pull_report.add_argument("--session-dir", type=Path, default=Path(".session"))

    subparsers.add_parser(
        "export-ratings", help="собрать ratings.json.br из companies.json"
    )

    set_rating_parser = subparsers.add_parser(
        "set-rating", help="записать рейтинг компании в companies.json"
    )
    set_rating_parser.add_argument("inn")
    set_rating_parser.add_argument("--period", required=True)
    set_rating_parser.add_argument("--rating", required=True, help="например ruA-")
    set_rating_parser.add_argument(
        "--outlook", required=True, type=Outlook, choices=list(Outlook)
    )
    set_rating_parser.add_argument("--prompt-version", type=int, required=True)
    set_rating_parser.add_argument("--model", required=True)

    agency_ratings_parser = subparsers.add_parser(
        "agency-ratings", help="показать рейтинги агентств из реестра ЦБ"
    )
    agency_ratings_parser.add_argument(
        "queries", nargs="+", help="ИНН или часть названия эмитента"
    )

    pdf_to_html_parser = subparsers.add_parser(
        "pdf-to-html", help="конвертировать PDF в HTML через datalab.to"
    )
    pdf_to_html_parser.add_argument("pdfs", nargs="+", type=Path)
    pdf_to_html_parser.add_argument(
        "--mode",
        type=ConversionMode,
        choices=list(ConversionMode),
        default=ConversionMode.BALANCED,
    )

    args = parser.parse_args()

    try:
        match args.command:
            case "pull-report":
                report = asyncio.run(
                    pull_msfo_report(
                        args.inn,
                        args.period,
                        exports_dir=args.exports_dir,
                        session_dir=args.session_dir,
                    )
                )
                if not report:
                    print("Отчет не найден")
            case "export-ratings":
                export_ratings(args.exports_dir)
            case "set-rating":
                set_rating(
                    args.inn,
                    period=args.period,
                    rating=args.rating,
                    outlook=args.outlook,
                    prompt_version=args.prompt_version,
                    model=args.model,
                    exports_dir=args.exports_dir,
                )
            case "agency-ratings":
                print(describe_agency_ratings(args.queries), end="")
            case "pdf-to-html":
                api_key = os.environ.get("DATALAB_API_KEY")
                if not api_key:
                    sys.exit("Не задан DATALAB_API_KEY")
                for pdf in args.pdfs:
                    html_path, page_count = pdf_to_html(pdf, args.mode, api_key=api_key)
                    print(f"{html_path} ({page_count} стр.)")
    except (ValueError, DatalabError) as error:
        sys.exit(str(error))


__all__ = [
    "ConversionMode",
    "DatalabError",
    "MsfoReport",
    "Outlook",
    "describe_agency_ratings",
    "export_ratings",
    "get_msfo_report",
    "main",
    "pdf_to_html",
    "pull_msfo_report",
    "set_rating",
]
