from collections import deque
from bs4 import BeautifulSoup, Tag
import requests
from urllib.parse import urljoin, urlparse, ParseResult
from urllib.robotparser import RobotFileParser
import time


class Crawler:
    def __init__(
        self,
        start_url: str,
        max_redirect: int,
        max_depth: int = 1,
        requests_per_second: int = 2,
    ):
        parsed_url = urlparse(start_url)
        self.domain: str = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.sitemap: dict[str, [str]] = dict()
        self.visited: set[str] = set()
        self.robots_cache: dict[str, RobotFileParser] = dict()
        self.requests_per_second = requests_per_second
        self.last_request = {}
        self.max_depth = max_depth
        self.max_redirects = max_redirect

    def _build_normalized_absolute_url(self, href: str) -> str:
        absolute: str = urljoin(self.domain, href)
        parsed_result: ParseResult = urlparse(absolute)
        normalized: str = parsed_result._replace(fragment="").geturl().rstrip()
        return normalized

    def _extract_links(self, html: str) -> [str]:
        bs = BeautifulSoup(html, "html.parser")
        tags: list[Tag] = bs.find_all("a", href=True)

        links: [str] = [
            self._build_normalized_absolute_url(tag["href"])
            for tag in tags
            if not (tag["href"].startswith(("#", "mailto:", "javascript:")))
        ]

        print(f"DEBUG: extract_links- links {links}")

        return links

    def _detect_cycle(
        self, current_url: str, history: list[requests.Response] = []
    ) -> bool:

        visted_url: [str] = [h.url for h in history]

        return current_url in visted_url

    def _rate_limit(self):
        min_interval: float = 1 / self.requests_per_second
        current_time: float = time.monotonic()
        duration: float = current_time - self.last_request.get(self.domain, 0)

        if duration < min_interval:
            time.sleep(min_interval - duration)

        self.last_request[self.domain] = time.monotonic()

    def _is_allowed(self, current_url: str) -> bool:
        try:
            parser = RobotFileParser()
            if current_url not in self.robots_cache:
                robot_text_url = urljoin(self.domain, "robots.txt")
                response = requests.get(robot_text_url)
                if response.status_code == 200:
                    content = response.text
                    parser.parse(content.splitlines())
                    self.robots_cache[current_url] = parser
                elif response.status_code in (401, 403):
                    self.robots_cache[current_url] = None
                else:
                    # 404 or anything else — cache empty parser, allows all
                    self.robots_cache[current_url] = parser
        except Exception:
            self.robots_cache[current_url] = parser

        rp = self.robots_cache[current_url]

        if rp is None:
            return False
        return rp.can_fetch("*", current_url)

    def _crawl_each_page(self, parent_url: str) -> [str]:
        self._rate_limit()

        try:
            session: requests.Session = requests.Session()
            session.max_redirects = self.max_redirects
            response = session.get(parent_url, allow_redirects=True)
            html = response.text
            print(f"DEBUG: crawling page {parent_url}")
        except requests.TooManyRedirects:
            return []

        cycle_detected: bool = self._detect_cycle(
            current_url=parent_url, history=response.history
        )

        if cycle_detected:
            return []

        links: [str] = self._extract_links(html)

        return links

    def crawl(self) -> {}:
        queue: deque[(str, int)] = deque()
        queue.append((self.domain, 0))
        while queue:
            parent_url, current_depth = queue.popleft()
            if (
                parent_url in self.visited
                or current_depth > self.max_depth
                or not self._is_allowed(parent_url)
            ):
                continue

            children_links: [str] = self._crawl_each_page(parent_url=parent_url)
            self.visited.add(parent_url)
            self.sitemap[parent_url] = children_links

            for link in children_links:
                queue.append((link, current_depth + 1))

        return self.sitemap

    def print_sitemap(self, result: dict):
        for key, values in result.items():
            print(key)
            for value in values:
                print(f"\t{value}")


if __name__ == "__main__":
    crawler = Crawler(start_url="http://www.ogee.com", max_redirect=5, max_depth=1)
    result = crawler.crawl()
    print("-----DONE-----")
    print(len(result.keys()))
    print(len(result.items()))

    crawler.print_sitemap(result)
