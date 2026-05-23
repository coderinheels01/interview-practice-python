from collections import deque
from bs4 import BeautifulSoup, Tag
import requests
from urllib.parse import urljoin, urlparse, ParseResult
from urllib.robotparser import RobotFileParser
import time
import aiohttp
import asyncio


class Crawler:
    def __init__(
        self,
        start_url: str,
        max_redirect: int,
        max_depth: int = 1,
        max_concurrency: int = 10,
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
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.timeout = aiohttp.ClientTimeout(total=10, connect=5, sock_read=10)

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

    async def _is_allowed(self, current_url: str) -> bool:
        try:
            parser = RobotFileParser()
            if current_url not in self.robots_cache:
                robot_text_url = urljoin(self.domain, "robots.txt")
                async with aiohttp.ClientSession() as session:
                    async with session.get(robot_text_url) as response:
                        if response.status == 200:
                            content = await response.text()
                            parser.parse(content.splitlines())
                            self.robots_cache[current_url] = parser
                        elif response.status in (401, 403):
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

    async def _crawl_each_page(
        self, session: aiohttp.ClientSession, parent_url: str
    ) -> [str]:
        self._rate_limit()

        try:
            async with self.semaphore:
                async with session.get(
                    parent_url,
                    allow_redirects=True,
                    max_redirects=self.max_redirects,
                ) as response:
                    html = await response.text()
                    print(f"DEBUG: crawling page {parent_url}")
        except aiohttp.TooManyRedirects:
            return []

        cycle_detected: bool = self._detect_cycle(
            current_url=parent_url, history=response.history
        )

        if cycle_detected:
            return []

        links: [str] = self._extract_links(html)

        return links

    async def crawl(self) -> {}:
        queue: deque[(str, int)] = deque()
        queue.append((self.domain, 0))
        tasks: [(asyncio.Task, int)] = []
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            while queue or tasks:
                print(f"DEBUG: inside queue loop {len(queue)}")
                parent_url, current_depth = queue.popleft()
                if (
                    parent_url in self.visited
                    or current_depth > self.max_depth
                    or not self._is_allowed(parent_url)
                ):
                    continue

                task: asyncio.Task = asyncio.create_task(
                    self._crawl_each_page(session, parent_url=parent_url)
                )

                tasks.append((task, current_depth))
                self.visited.add(parent_url)

                print(f"DEBUG: inside tasks loop {len(tasks)}")
                done, _ = await asyncio.wait(
                    [t for t, _ in tasks], return_when=asyncio.FIRST_COMPLETED
                )

                remaining_tasks: [asyncio.Task, int] = []

                for t in tasks:
                    task, depth = t
                    if task in done:
                        result = task.result()
                        if result:
                            self.sitemap[parent_url] = result
                            for link in result:
                                queue.append((link, depth + 1))
                    else:
                        remaining_tasks.append(t)

                tasks = remaining_tasks

        return self.sitemap

    def print_sitemap(self, result: dict):
        for key, values in result.items():
            print(key)
            for value in values:
                print(f"\t{value}")


if __name__ == "__main__":

    async def main():
        crawler = Crawler(start_url="http://www.ogee.com", max_redirect=5, max_depth=1)
        result = await crawler.crawl()
        print("-----DONE-----")
        print(len(result.keys()))
        print(len(result.items()))
        crawler.print_sitemap(result)

    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(main())
