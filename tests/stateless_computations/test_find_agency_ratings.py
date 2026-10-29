from e_disclosure._entities.agency_rating import AgencyRating
from e_disclosure._stateless_computations.find_agency_ratings import (
    find_agency_ratings,
)


def _rating(name: str) -> AgencyRating:
    return AgencyRating(
        objectName=name,
        ratingValue="ruA",
        prediction="Стабильный",
        releaseDate="2026-01-01",
        ratingAction="Подтверждение",
        releaseUrl="https://example.com",
    )


ISSUERS = {
    "7700": {"АКРА": _rating("ПАО Брусника")},
    "7800": {"АКРА": _rating("ООО Борец")},
}


def test_find_agency_ratings(subtests) -> None:
    cases = {
        "inn": ("7700", ["7700"]),
        "name_case_insensitive": ("брусНИКА", ["7700"]),
        "none": ("Сбер", []),
    }
    for name, (query, inns) in cases.items():
        with subtests.test(name):
            assert list(find_agency_ratings(ISSUERS, query)) == inns
