from functools import partial

from patchright.async_api import Page

from e_disclosure._entities.msfo_report import MsfoReport
from e_disclosure._entities.report_type import ReportType
from e_disclosure._stateless_effects.download_file import download_file
from e_disclosure._stateless_effects.find_company_by_inn import find_company_by_inn
from e_disclosure._stateless_effects.list_reports import list_reports
from e_disclosure._stateless_effects.unpack_report_archive import unpack_report_archive
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
        unpack_report_archive=unpack_report_archive,
    )


__all__ = [
    "MsfoReport",
    "ReportType",
    "get_msfo_report",
]
