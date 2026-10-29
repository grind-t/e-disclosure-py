import re

from e_disclosure._entities.report import Report
from e_disclosure._entities.report_type import ReportType


def select_msfo_report(
    reports: dict[ReportType, list[Report]], period: str | None
) -> tuple[ReportType, Report] | None:
    """Последний размещённый МСФО-отчёт, или последний за ``period``, если он задан.

    Отчёты каждой вкладки идут от новых к старым.
    """
    candidates = [
        (report_type, latest)
        for report_type, type_reports in reports.items()
        if (latest := _latest(report_type, type_reports, period))
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda c: c[1].placement_date)


def _latest(
    report_type: ReportType, reports: list[Report], period: str | None
) -> Report | None:
    return next(
        (
            r
            for r in reports
            if (period is None or r.period == period) and _is_msfo(report_type, r)
        ),
        None,
    )


def _is_msfo(report_type: ReportType, report: Report) -> bool:
    # На вкладке ACCOUNTING МСФО лежит вперемешку с РСБУ
    return report_type is ReportType.CONSOLIDATED or bool(
        re.search("мсфо", report.type, re.IGNORECASE)
    )
