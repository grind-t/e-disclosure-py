from typing import NotRequired, TypedDict


class RatingEntry(TypedDict):
    """Рейтинг компании за период в ``companies.json``.

    ``value`` — индекс в шкале рейтингов. У ещё не оценённого периода
    ``value`` равен 0, ``outlook`` пуст, а полей анализа нет.
    """

    period: str
    value: int
    outlook: NotRequired[str]
    promptVersion: NotRequired[int]
    model: NotRequired[str]
    analyzedAt: NotRequired[str]
