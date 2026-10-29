from e_disclosure._entities.msfo_report import MsfoReport
from e_disclosure._entities.rated_company import RatedCompany
from e_disclosure._entities.rating_entry import RatingEntry


def with_pending_rating(
    companies: dict[str, RatedCompany], inn: str, report: MsfoReport
) -> dict[str, RatedCompany]:
    """Компании с неоценённым периодом ``report``; новая компания добавляется."""
    company = companies.get(inn) or RatedCompany(
        id=report.company_id, ratings=[], reportType=report.type
    )
    pending = RatingEntry(period=report.period, value=0, outlook="")
    ratings = [*company["ratings"], pending]
    return {
        **companies,
        inn: RatedCompany(
            id=company["id"], ratings=ratings, reportType=company["reportType"]
        ),
    }
