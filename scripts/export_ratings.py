"""Собрать exports/ratings.json.br с последним рейтингом каждой компании."""

import json
from pathlib import Path

import brotli

EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"


def main() -> None:
    companies = json.loads((EXPORTS_DIR / "companies.json").read_text())
    latest = {
        inn: {
            key: company["ratings"][-1][key]
            for key in ("value", "outlook")
            if key in company["ratings"][-1]
        }
        for inn, company in companies.items()
    }
    text = json.dumps(latest, ensure_ascii=False, separators=(",", ":"))
    (EXPORTS_DIR / "ratings.json.br").write_bytes(brotli.compress(text.encode()))


if __name__ == "__main__":
    main()
