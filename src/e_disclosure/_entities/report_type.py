from enum import IntEnum


class ReportType(IntEnum):
    """Вкладка отчётности компании на e-disclosure.ru."""

    ACCOUNTING = 3
    """«Бухгалтерская (финансовая)»: МСФО вперемешку с РСБУ."""
    CONSOLIDATED = 4
    """«Консолидированная»: только консолидированная МСФО."""
