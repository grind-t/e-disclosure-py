from e_disclosure._entities.agency_rating import AgencyRating


def format_agency_ratings(
    query: str, issuers: dict[str, dict[str, AgencyRating]]
) -> str:
    """Рейтинги найденных по ``query`` эмитентов, по строке на агентство."""
    if not issuers:
        return f"{query}: рейтингов агентств нет\n\n"
    blocks = []
    for inn, agencies in issuers.items():
        name = next(iter(agencies.values()))["objectName"]
        lines = [f"{inn} {name}"] + [
            f"  {agency}: {r['ratingValue']}, {r['prediction']}, "
            f"{r['releaseDate']}, {r['ratingAction']}, {r['releaseUrl']}"
            for agency, r in agencies.items()
        ]
        blocks.append("\n".join(lines) + "\n\n")
    return "".join(blocks)
