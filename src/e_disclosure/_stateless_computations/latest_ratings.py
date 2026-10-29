from e_disclosure._entities.rated_company import RatedCompany


def latest_ratings(companies: dict[str, RatedCompany]) -> dict[str, dict[str, object]]:
    """Значение и прогноз последнего рейтинга каждой компании."""
    return {
        inn: {
            key: company["ratings"][-1][key]
            for key in ("value", "outlook")
            if key in company["ratings"][-1]
        }
        for inn, company in companies.items()
    }
