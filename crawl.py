from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag


def normalize_url(url):
    parsed = urlparse(url)
    host_path = parsed.netloc + parsed.path
    if host_path.endswith("/"):
        host_path = host_path[:-1]
    return host_path


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h_tag = soup.find("h1")
    if not isinstance(h_tag, Tag):
        h_tag = soup.find("h2")
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main_tag = soup.find("main")
    search_root = main_tag if isinstance(main_tag, Tag) else soup
    p_tag = search_root.find("p")
    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""