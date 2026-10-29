import json
from pathlib import Path

from e_disclosure._entities.rated_company import RatedCompany


def read_companies(exports_dir: Path) -> dict[str, RatedCompany]:
    return json.loads((exports_dir / "companies.json").read_text())
