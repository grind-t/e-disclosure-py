import json

import brotli

from e_disclosure._entities.agency_rating import AgencyRating
from e_disclosure._stateless_effects.curl import curl

_URL = (
    "https://raw.githubusercontent.com/grind-t/cbr-ratings/main/exports/issuers.json.br"
)


def fetch_agency_ratings() -> dict[str, dict[str, AgencyRating]]:
    """Рейтинги агентств из реестра ЦБ: ИНН → агентство → рейтинг."""
    return json.loads(brotli.decompress(curl(_URL)))
