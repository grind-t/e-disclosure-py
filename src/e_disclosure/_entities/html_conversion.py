from dataclasses import dataclass


@dataclass(frozen=True)
class HtmlConversion:
    html: str
    page_count: int | None
