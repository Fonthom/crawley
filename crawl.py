from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup, Tag

from typing import TypedDict


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


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


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for a_tag in soup.find_all("a"):
        href = a_tag.get("href")
        if href is None:
            continue
        urls.append(urljoin(base_url, href))
    return urls


def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for img_tag in soup.find_all("img"):
        src = img_tag.get("src")
        if src is None:
            continue
        urls.append(urljoin(base_url, src))
    return urls

def extract_page_data(html: str, base_url: str) -> PageData:
    return PageData(
        url=base_url,
        heading=get_heading_from_html(html),
        first_paragraph=get_first_paragraph_from_html(html),
        outgoing_links=get_urls_from_html(html, base_url),
        image_urls=get_images_from_html(html, base_url)
    )