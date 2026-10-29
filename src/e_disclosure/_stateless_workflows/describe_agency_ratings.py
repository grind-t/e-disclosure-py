from collections.abc import Callable

from e_disclosure._entities.agency_rating import AgencyRating
from e_disclosure._stateless_computations.find_agency_ratings import (
    find_agency_ratings,
)
from e_disclosure._stateless_computations.format_agency_ratings import (
    format_agency_ratings,
)


def describe_agency_ratings(
    queries: list[str],
    *,
    fetch_agency_ratings: Callable[[], dict[str, dict[str, AgencyRating]]],
) -> str:
    """Рейтинги агентств эмитентов по ИНН или части названия."""
    issuers = fetch_agency_ratings()
    return "".join(
        format_agency_ratings(query, find_agency_ratings(issuers, query))
        for query in queries
    )
