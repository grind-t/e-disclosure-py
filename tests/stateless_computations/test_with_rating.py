import pytest

from e_disclosure._entities.rated_company import RatedCompany
from e_disclosure._entities.rating_entry import RatingEntry
from e_disclosure._entities.report_type import ReportType
from e_disclosure._stateless_computations.with_rating import with_rating


def _company(*periods: str) -> RatedCompany:
    return RatedCompany(
        id="1",
        ratings=[RatingEntry(period=p, value=0, outlook="") for p in periods],
        reportType=ReportType.CONSOLIDATED,
    )


def test_with_rating_replaces_same_period() -> None:
    companies = {"7700": _company("2025", "2026, 6 месяцев")}
    rating = RatingEntry(period="2025", value=17, outlook="STA")

    ratings = with_rating(companies, "7700", rating)["7700"]["ratings"]

    assert ratings == [rating, companies["7700"]["ratings"][1]]


def test_with_rating_sorts_new_period_after_half_year() -> None:
    companies = {"7700": _company("2025", "2026, 6 месяцев")}
    rating = RatingEntry(period="2026", value=17, outlook="STA")

    ratings = with_rating(companies, "7700", rating)["7700"]["ratings"]

    assert [r["period"] for r in ratings] == ["2025", "2026, 6 месяцев", "2026"]


def test_with_rating_unknown_company() -> None:
    with pytest.raises(ValueError, match="сначала запустите pull-report"):
        with_rating({}, "7700", RatingEntry(period="2025", value=17))
