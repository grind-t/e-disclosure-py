from collections.abc import Callable
from datetime import date

from e_disclosure._entities.outlook import Outlook
from e_disclosure._entities.rated_company import RatedCompany
from e_disclosure._entities.rating_entry import RatingEntry
from e_disclosure._stateless_computations.rating_to_value import rating_to_value
from e_disclosure._stateless_computations.with_rating import with_rating


def set_rating(
    inn: str,
    *,
    period: str,
    rating: str,
    outlook: Outlook,
    prompt_version: int,
    model: str,
    analyzed_at: date,
    read_companies: Callable[[], dict[str, RatedCompany]],
    write_companies: Callable[[dict[str, RatedCompany]], None],
) -> None:
    """Записать рейтинг вида ``ruA-`` за период, заменив прежний за тот же период."""
    entry = RatingEntry(
        period=period,
        value=rating_to_value(rating),
        outlook=outlook,
        promptVersion=prompt_version,
        model=model,
        analyzedAt=analyzed_at.isoformat(),
    )
    write_companies(with_rating(read_companies(), inn, entry))
