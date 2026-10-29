from e_disclosure._entities.agency_rating import AgencyRating


def find_agency_ratings(
    issuers: dict[str, dict[str, AgencyRating]], query: str
) -> dict[str, dict[str, AgencyRating]]:
    """Эмитенты с ИНН ``query`` или с ``query`` в названии, без учёта регистра."""
    if query in issuers:
        return {query: issuers[query]}
    needle = query.casefold()
    return {
        inn: agencies
        for inn, agencies in issuers.items()
        if any(needle in r["objectName"].casefold() for r in agencies.values())
    }
