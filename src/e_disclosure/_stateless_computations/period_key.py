import re


def period_key(period: str) -> tuple[int, int]:
    """Ключ сортировки периода вида ``2025`` или ``2026, 6 месяцев``."""
    match = re.fullmatch(r"(\d{4})(?:, (\d+) месяц\w*)?", period)
    if not match:
        raise ValueError(f"Неизвестный формат периода: {period}")
    return int(match.group(1)), int(match.group(2) or 12)
