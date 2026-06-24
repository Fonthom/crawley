from urllib.parse import urlparse, urljoin
import asyncio
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests


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

def get_html(url):
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
 
    if response.status_code >= 400:
        raise Exception(
            f"Error fetching {url}: status code {response.status_code}"
        )
 
    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type:
        raise Exception(
            f"Error fetching {url}: content type is not text/html, got {content_type}"
        )

    return response.text


def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}
 
    base_domain = urlparse(base_url).netloc
    current_domain = urlparse(current_url).netloc
    if base_domain != current_domain:
        return page_data
 
    normalized_current_url = normalize_url(current_url)
    if normalized_current_url in page_data:
        return page_data
 
    print(f"crawling: {current_url}")
 
    try:
        html = get_html(current_url)
    except Exception as e:
        print(f"error fetching {current_url}: {e}")
        return page_data
 
    page_data[normalized_current_url] = extract_page_data(html, current_url)
 
    next_urls = get_urls_from_html(html, base_url)
    for next_url in next_urls:
        crawl_page(base_url, next_url, page_data)
 
    return page_data

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=5):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
 
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
 
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
 
    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            self.page_data[normalized_url] = None
            return True
 
    async def get_html(self, url):
        async with self.session.get(
            url, headers={"User-Agent": "BootCrawler/1.0"}
        ) as response:
            if response.status >= 400:
                raise Exception(
                    f"Error fetching {url}: status code {response.status}"
                )
 
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                raise Exception(
                    f"Error fetching {url}: content type is not text/html, got {content_type}"
                )
 
            return await response.text()
 
    async def crawl_page(self, current_url=None):
        if current_url is None:
            current_url = self.base_url
 
        current_domain = urlparse(current_url).netloc
        if current_domain != self.base_domain:
            return
 
        normalized_current_url = normalize_url(current_url)
        is_new_page = await self.add_page_visit(normalized_current_url)
        if not is_new_page:
            return
 
        async with self.semaphore:
            print(f"crawling: {current_url}")
 
            try:
                html = await self.get_html(current_url)
            except Exception as e:
                print(f"error fetching {current_url}: {e}")
                return
 
        page_data = extract_page_data(html, current_url)
        async with self.lock:
            self.page_data[normalized_current_url] = page_data
 
        next_urls = get_urls_from_html(html, self.base_url)
        tasks = []
        for next_url in next_urls:
            task = asyncio.create_task(self.crawl_page(next_url))
            tasks.append(task)
 
        if tasks:
            await asyncio.gather(*tasks)
 
    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
 
 
async def crawl_site_async(base_url, max_concurrency=5):
    async with AsyncCrawler(base_url, max_concurrency=max_concurrency) as crawler:
        return await crawler.crawl()