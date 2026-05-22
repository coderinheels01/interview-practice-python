from collections import deque
from bs4 import BeautifulSoup, Tag
import requests
from urllib.parse import urljoin, urlparse


def crawl(start_url: str, max_depth: int = 1) -> {}:
    queue: deque[(str, int)] = deque()
    queue.append((start_url, 0))

    sitemap: dict[str, [str]] = dict()
    visited: set[str] = set()

    parsed_url = urlparse(start_url)
    domain: str = f"{parsed_url.scheme}://{parsed_url.netloc}"

    while queue:
        parent_url, current_depth = queue.popleft()
        if parent_url in visited or current_depth > max_depth:
            continue

        children_links: [str] = crawl_each_page(parent_url=parent_url, domain=domain)
        visited.add(parent_url)

        for link in children_links:
            queue.append((link, current_depth + 1))

    return sitemap


def crawl_each_page(parent_url: str, domain: str) -> [str]:
    response = requests.get(parent_url)
    html = response.text

    links: [str] = extract_links(html, domain)

    print(f"DEBUG: crawl_each_page- links {links}")
    return links


def extract_links(html: str, domain: str) -> [str]:
    bs = BeautifulSoup(html, "html.parser")
    tags: list[Tag] = bs.find_all("a", href=True)

    print(f"DEBUG: extract_links- domain {domain}")

    links: [str] = [
        urljoin(domain, tag["href"])
        for tag in tags
        if not (tag["href"].startswith(("#", "mailto:", "javascript:")))
    ]

    print(f"DEBUG: extract_links- links {links}")

    return links


if __name__ == "__main__":
    result = crawl("http://www.ogee.com", 2)
    print("-----DONE-----")
    print(result)
