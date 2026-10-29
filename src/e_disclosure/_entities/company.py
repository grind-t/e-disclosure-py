from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    id: str
    name: str
