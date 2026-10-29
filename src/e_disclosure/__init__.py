import argparse
from functools import partial

from patchright.async_api import Page

from e_disclosure._entities.msfo_report import MsfoReport
from e_disclosure._entities.report_type import ReportType
from e_disclosure._stateless_effects.download_file import download_file
from e_disclosure._stateless_effects.fetch_agency_ratings import fetch_agency_ratings
from e_disclosure._stateless_effects.find_company_by_inn import find_company_by_inn
from e_disclosure._stateless_effects.list_reports import list_reports
from e_disclosure._stateless_effects.unpack_files import unpack_files
from e_disclosure._stateless_workflows.describe_agency_ratings import (
    describe_agency_ratings as _describe_agency_ratings,
)
from e_disclosure._stateless_workflows.get_msfo_report import (
    get_msfo_report as _get_msfo_report,
)


async def get_msfo_report(
    page: Page, inn: str, period: str | None = None
) -> MsfoReport | None:
    """Последний МСФО-отчёт компании, или последний за ``period``, если он задан.

    Архив отчёта распакован. Через ``page`` идут запросы к e-disclosure.ru,
    поэтому её браузер должен проходить защиту от ботов.
    """
    return await _get_msfo_report(
        inn,
        period,
        find_company_by_inn=partial(find_company_by_inn, page),
        list_reports=partial(list_reports, page),
        download_file=partial(download_file, page),
        unpack_files=unpack_files,
    )


def describe_agency_ratings(queries: list[str]) -> str:
    """Рейтинги агентств из реестра ЦБ по ИНН или части названия эмитента."""
    return _describe_agency_ratings(queries, fetch_agency_ratings=fetch_agency_ratings)


def main() -> None:
    parser = argparse.ArgumentParser(prog="e-disclosure")
    subparsers = parser.add_subparsers(dest="command", required=True)

    agency_ratings_parser = subparsers.add_parser(
        "agency-ratings", help="показать рейтинги агентств из реестра ЦБ"
    )
    agency_ratings_parser.add_argument(
        "queries", nargs="+", help="ИНН или часть названия эмитента"
    )

    args = parser.parse_args()

    match args.command:
        case "agency-ratings":
            print(describe_agency_ratings(args.queries), end="")


__all__ = [
    "MsfoReport",
    "ReportType",
    "describe_agency_ratings",
    "get_msfo_report",
    "main",
]
