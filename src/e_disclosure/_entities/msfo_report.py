from dataclasses import dataclass

from e_disclosure._entities.downloaded_file import DownloadedFile
from e_disclosure._entities.report_type import ReportType


@dataclass(frozen=True)
class MsfoReport:
    company_id: str
    type: ReportType
    period: str
    files: list[DownloadedFile]
