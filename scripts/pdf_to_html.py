"""Конвертировать PDF в HTML рядом с ним через datalab.to.

Ключ берётся из переменной окружения ``DATALAB_API_KEY`` или ``datalab login``.
"""

import argparse
from pathlib import Path

from datalab_sdk import ConversionResult, ConvertOptions, DatalabClient

OPTIONS = ConvertOptions(
    output_format="html",
    mode="balanced",
    disable_image_extraction=True,
    disable_image_captions=True,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdfs", nargs="+", type=Path)
    args = parser.parse_args()

    client = DatalabClient()
    for pdf in args.pdfs:
        result = client.convert(pdf, options=OPTIONS)
        # без stream_response_to SDK всегда возвращает ConversionResult
        assert isinstance(result, ConversionResult)
        html_path = pdf.with_suffix(".html")
        html_path.write_text(result.html or "")
        print(f"{html_path} ({result.page_count} стр.)")


if __name__ == "__main__":
    main()
