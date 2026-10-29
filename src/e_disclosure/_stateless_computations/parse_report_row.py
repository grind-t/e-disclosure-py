import re
from datetime import datetime

from e_disclosure._entities.report import Report


def parse_report_row(cells: list[str], download_url: str | None) -> Report | None:
    """Отчёт из строки таблицы отчётов, или None для заголовка и пустых строк."""
    if len(cells) < 6 or not re.fullmatch(r"\d+", cells[0].strip()):
        return None
    if not download_url:
        return None
    return Report(
        type=cells[1].strip(),
        period=cells[2].strip(),
        # в таблице дата без времени и зоны
        placement_date=datetime.strptime(cells[4].strip(), "%d.%m.%Y").date(),  # noqa: DTZ007
        download_url=download_url,
    )
