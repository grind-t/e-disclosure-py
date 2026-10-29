import json
import time
from pathlib import PurePath

from e_disclosure._entities.conversion_mode import ConversionMode
from e_disclosure._entities.html_conversion import HtmlConversion
from e_disclosure._stateless_effects.curl import curl

_CONVERT_URL = "https://www.datalab.to/api/v1/convert"
_POLL_INTERVAL = 2


class DatalabError(Exception):
    """datalab.to не смог конвертировать файл."""


def convert_pdf_to_html(
    api_key: str, pdf: PurePath, mode: ConversionMode
) -> HtmlConversion:
    # Заголовок с ключом передаём через stdin, чтобы ключ не попал в argv и трейсбеки
    auth = f"X-API-Key: {api_key}".encode()
    form = {
        "file": f"@{pdf};type=application/pdf",
        "output_format": "html",
        "mode": mode,
        "disable_image_extraction": "true",
        "disable_image_captions": "true",
    }
    form_args = [arg for key, value in form.items() for arg in ("-F", f"{key}={value}")]
    submitted = json.loads(curl("-H", "@-", *form_args, _CONVERT_URL, stdin=auth))
    if not submitted.get("success"):
        raise DatalabError(f"{pdf}: {submitted.get('error')}")

    while True:
        time.sleep(_POLL_INTERVAL)
        result = json.loads(
            curl("-H", "@-", submitted["request_check_url"], stdin=auth)
        )
        if result["status"] != "processing":
            break

    if result["status"] != "complete" or not result.get("success"):
        raise DatalabError(f"{pdf}: {result.get('error')}")
    return HtmlConversion(html=result["html"], page_count=result.get("page_count"))
