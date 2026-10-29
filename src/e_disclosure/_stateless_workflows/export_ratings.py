from collections.abc import Callable

from e_disclosure._entities.rated_company import RatedCompany
from e_disclosure._stateless_computations.encode_brotli_json import (
    encode_brotli_json,
)
from e_disclosure._stateless_computations.latest_ratings import latest_ratings


def export_ratings(
    *,
    read_companies: Callable[[], dict[str, RatedCompany]],
    write_export: Callable[[str, bytes], None],
) -> None:
    """Собрать ``ratings.json.br`` с последним рейтингом каждой компании."""
    write_export(
        "ratings.json.br", encode_brotli_json(latest_ratings(read_companies()))
    )
