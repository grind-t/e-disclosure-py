from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Report:
    """Строка таблицы отчётов компании."""

    type: str
    period: str
    placement_date: date
    download_url: str
