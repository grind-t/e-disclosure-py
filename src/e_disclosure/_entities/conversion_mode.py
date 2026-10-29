from enum import StrEnum


class ConversionMode(StrEnum):
    """Режим конвертации datalab.to: от быстрого к точному."""

    LITE = "lite"
    FAST = "fast"
    BALANCED = "balanced"
    ACCURATE = "accurate"
