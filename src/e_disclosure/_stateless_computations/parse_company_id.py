from urllib.parse import parse_qs, urljoin, urlparse


def parse_company_id(page_url: str, href: str) -> str | None:
    """Id компании из ссылки ``company.aspx?id=...``."""
    ids = parse_qs(urlparse(urljoin(page_url, href)).query).get("id")
    return ids[0] if ids else None
