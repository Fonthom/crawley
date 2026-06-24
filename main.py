import asyncio
import sys
from crawl import get_html, crawl_page, crawl_site_async

def main():
    args = sys.argv[1:]

    if len(args) < 1:
        print("no website provided")
        sys.exit(1)

    if len(args) > 1:
        print("too many arguments provided")
        sys.exit(1)

    base_url = args[0]
    print(f"starting crawl: {base_url}")

    '''
    html = get_html(base_url)
    print(html)
    '''

    '''
    page_data = crawl_page(base_url)
    '''

    page_data = await crawl_site_async(base_url, max_concurrency=5)
    
    print(f"\nfound {len(page_data)} pages")
    for url, data in page_data.items():
        print(f"\n--- {url} ---")
        for key, value in data.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
