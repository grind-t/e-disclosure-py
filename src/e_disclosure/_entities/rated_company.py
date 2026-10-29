from typing import TypedDict

from e_disclosure._entities.rating_entry import RatingEntry
from e_disclosure._entities.report_type import ReportType


class RatedCompany(TypedDict):
    """Компания в ``companies.json``; рейтинги отсортированы по периоду."""

    id: str
    ratings: list[RatingEntry]
    reportType: ReportType
