import json

import brotli


def encode_brotli_json(data: object) -> bytes:
    """Компактный JSON, сжатый brotli."""
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return brotli.compress(text.encode())
