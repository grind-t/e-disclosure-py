from collections.abc import Callable
from pathlib import PurePath

from e_disclosure._entities.conversion_mode import ConversionMode
from e_disclosure._entities.html_conversion import HtmlConversion


def pdf_to_html(
    pdf: PurePath,
    mode: ConversionMode,
    *,
    convert_pdf_to_html: Callable[[PurePath, ConversionMode], HtmlConversion],
    write_text: Callable[[PurePath, str], None],
) -> tuple[PurePath, int | None]:
    """Сохранить HTML рядом с PDF; вернуть его путь и число страниц."""
    conversion = convert_pdf_to_html(pdf, mode)
    html_path = pdf.with_suffix(".html")
    write_text(html_path, conversion.html)
    return html_path, conversion.page_count
