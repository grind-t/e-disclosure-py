from e_disclosure._entities.rated_company import RatedCompany
from e_disclosure._entities.rating_entry import RatingEntry
from e_disclosure._stateless_computations.period_key import period_key


def with_rating(
    companies: dict[str, RatedCompany], inn: str, rating: RatingEntry
) -> dict[str, RatedCompany]:
    """Компании с рейтингом за период, заменяющим прежний за тот же период."""
    company = companies.get(inn)
    if company is None:
        raise ValueError(
            f"Компании {inn} нет в companies.json, сначала запустите pull-report"
        )
    others = [r for r in company["ratings"] if r["period"] != rating["period"]]
    ratings = sorted([*others, rating], key=lambda r: period_key(r["period"]))
    return {
        **companies,
        inn: RatedCompany(
            id=company["id"], ratings=ratings, reportType=company["reportType"]
        ),
    }
