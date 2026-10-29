import re

_RATING_SCALE = [
    "D", "C", "CC-", "CC", "CC+", "CCC-", "CCC", "CCC+",
    "B-", "B", "B+", "BB-", "BB", "BB+", "BBB-", "BBB", "BBB+",
    "A-", "A", "A+", "AA-", "AA", "AA+", "AAA",
]  # fmt: skip


def rating_to_value(rating: str) -> int:
    """Индекс рейтинга вида ``ruA-`` или ``A-`` в шкале от D до AAA."""
    match = re.fullmatch(r"(?:ru)?([A-D]{1,3}[+-]?)", rating.strip(), re.IGNORECASE)
    grade = match.group(1).upper() if match else None
    if grade not in _RATING_SCALE:
        raise ValueError(f"Неизвестный рейтинг: {rating}")
    return _RATING_SCALE.index(grade)
