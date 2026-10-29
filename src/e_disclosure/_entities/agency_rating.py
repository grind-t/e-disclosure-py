from typing import TypedDict


class AgencyRating(TypedDict):
    """Рейтинг агентства из реестра ЦБ (поля, которые нужны CLI)."""

    objectName: str
    ratingValue: str
    prediction: str
    releaseDate: str
    ratingAction: str
    releaseUrl: str
