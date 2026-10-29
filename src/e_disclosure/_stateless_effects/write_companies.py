import json
from pathlib import Path

from e_disclosure._entities.rated_company import RatedCompany


def write_companies(exports_dir: Path, companies: dict[str, RatedCompany]) -> None:
    (exports_dir / "companies.json").write_text(
        json.dumps(companies, ensure_ascii=False, indent=2) + "\n"
    )
