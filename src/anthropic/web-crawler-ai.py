import asyncio
import time
from collections import deque
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import aiohttp
from bs4 import BeautifulSoup


# ------------------------------------------------------------------ #
# Step 4 + Step 10: Link extraction with URL normalization           #
# ------------------------------------------------------------------ #

def get_links(html, base_url, base_domain):
    # parse the raw HTML so we can search through it
    soup = BeautifulSoup(html, "html.parser")

    links = []

    # find every <a> tag that has an href attribute
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()

        # skip empty links, page anchors, emails, javascript
        if not href or href.startswith(("#", "mailto:", "javascript:")):
            continue

        # urljoin converts relative URLs to absolute
        # if href is /about and base_url is https://ogee.com
        # urljoin gives back https://ogee.com/about
        # if href is already absolute it leaves it alone
        absolute = urljoin(base_url, href)

        # step 10: normalize the URL
        # strip fragment: https://ogee.com/about#team -> https://ogee.com/about
        # #team just scrolls the page, it is not a different page
        parsed = urlparse(absolute)._replace(fragment="")

        # get the url back as a string then strip trailing slash
        # https://ogee.com/about/ -> https://ogee.com/about
        # we use rstrip not strip so we dont accidentally touch https://
        normalized = parsed.geturl().rstrip("/")

        # only keep links that are on the same domain
        # we don't want to crawl the entire internet
        if urlparse(normalized).netloc != base_domain:
            continue

        links.append(normalized)

    # remove duplicates from this page's links using set
    return list(set(links))


# ------------------------------------------------------------------ #
# Step 5: robots.txt                                                  #
# ------------------------------------------------------------------ #

# cache robots.txt per domain so we only fetch it once
robots_cache = {}

async def is_allowed(session, url):
    parsed = urlparse(url)

    # build the robots.txt URL for this domain
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    # only fetch robots.txt if we haven't seen this domain before
    if robots_url not in robots_cache:
        rp = RobotFileParser()
        rp.set_url(robots_url)

        try:
            async with session.get(robots_url) as response:
                if response.status == 200:
                    text = await response.text()
                    rp.parse(text.splitlines())
                elif response.status in (401, 403):
                    # if access is denied treat the whole site as blocked
                    rp.parse(["User-agent: *", "Disallow: /"])
                # if 404 or anything else, assume we are allowed
        except Exception:
            # if robots.txt fetch fails for any reason, assume allowed
            pass

        robots_cache[robots_url] = rp

    rp = robots_cache[robots_url]

    # check if our crawler is allowed to visit this specific URL
    # the "*" means we are identifying ourselves as a generic crawler
    return rp.can_fetch("*", url)


# ------------------------------------------------------------------ #
# Step 6: Rate limiting                                               #
# ------------------------------------------------------------------ #

# track the last time we made a request to each domain
domain_last_request = {}

# lock prevents two tasks from reading and writing
# domain_last_request at the same time
# without this two tasks could both read the same last time
# and both think they are allowed to go, breaking the rate limit
rate_lock = asyncio.Lock()

async def rate_limit(url, requests_per_second):
    domain = urlparse(url).netloc

    # how long we must wait between requests
    # 2 requests per second = 1.0 / 2 = 0.5 seconds between requests
    min_interval = 1.0 / requests_per_second

    # only one task can be inside here at a time
    # prevents race conditions on domain_last_request
    async with rate_lock:
        # time.monotonic() is a stopwatch that only goes forward
        # unlike time.time() it can never jump backwards
        now = time.monotonic()

        # if we have never hit this domain before, default to 0
        # 0 means the wait calculation will always be negative
        # which means no wait on the first request
        last = domain_last_request.get(domain, 0)

        time_since_last = now - last

        if time_since_last < min_interval:
            # asyncio.sleep yields control to other tasks while waiting
            # unlike time.sleep which freezes the entire program
            await asyncio.sleep(min_interval - time_since_last)

        domain_last_request[domain] = time.monotonic()


# ------------------------------------------------------------------ #
# Steps 7 + 8 + 9: crawl_page                                        #
# handles one single URL                                              #
# with timeout handling and redirect loop detection                   #
# ------------------------------------------------------------------ #

async def crawl_page(session, url, depth, base_domain, semaphore, requests_per_second):
    # check robots.txt before doing anything
    if not await is_allowed(session, url):
        print(f"[BLOCKED] robots.txt blocked: {url}")
        return None

    # enforce rate limit before fetching
    await rate_limit(url, requests_per_second)

    # semaphore limits how many tasks can be inside here at once
    # if 10 tasks are already fetching, the 11th waits here
    # until one of the 10 finishes and releases the semaphore
    async with semaphore:
        try:
            async with session.get(url, allow_redirects=True) as response:

                # step 9: redirect loop detection
                # response.history = every url visited along the redirect chain
                # response.url     = the final url we landed on
                # if the final url appeared in the history we went in a circle
                seen_in_chain = {str(r.url) for r in response.history}
                if str(response.url) in seen_in_chain:
                    print(f"[CYCLE] redirect cycle detected: {url}")
                    return None

                if response.status != 200:
                    return url, []

                html = await response.text()
                links = get_links(html, url, base_domain)
                return url, links

        except asyncio.TimeoutError:
            # fires when connect or sock_read timeout is exceeded
            # this is the "page that hangs 30 seconds" case
            print(f"[TIMEOUT] {url}")
            return None

        except aiohttp.TooManyRedirects:
            # fires when redirect count exceeds max_redirects=5
            # first line of defense against redirect loops
            print(f"[REDIRECT] too many redirects: {url}")
            return None

        except aiohttp.ClientError as e:
            # catches all other aiohttp network errors
            # server crashes, connection resets, DNS failures etc
            print(f"[ERROR] {url}: {e}")
            return None


# ------------------------------------------------------------------ #
# Steps 1-3 + 7: BFS crawler                                         #
# ------------------------------------------------------------------ #

async def crawl(start_url, max_depth, requests_per_second=2.0, max_concurrent=10, request_timeout=10.0):
    # deque for BFS queue
    # we store tuples of (url, depth) so we always know how deep we are
    # deque is used because removing from the front of a list is slow
    queue = deque()
    queue.append((start_url, 0))

    # visited set for dedup
    # sets are used because checking membership is very fast
    visited = set()
    visited.add(start_url)

    # sitemap dictionary
    # key   = page we visited
    # value = list of links found on that page
    sitemap = {}

    # extract domain once for filtering links
    base_domain = urlparse(start_url).netloc

    # semaphore caps how many pages we fetch at the same time
    # only max_concurrent tickets available at once
    semaphore = asyncio.Semaphore(max_concurrent)

    # step 8: timeout configuration
    # total     = hard ceiling for the entire request start to finish
    # connect   = how long to wait just to connect to the server
    # sock_read = how long to wait for the server to send data back
    timeout = aiohttp.ClientTimeout(
        total=request_timeout,
        connect=5.0,
        sock_read=request_timeout,
    )

    # step 8: TCPConnector limits open connections at the network level
    # separate from semaphore which limits at the application level
    connector = aiohttp.TCPConnector(limit=50)

    # step 9: max_redirects is first line of defense against redirect loops
    # aiohttp raises TooManyRedirects if this limit is exceeded
    async with aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        max_redirects=5,
    ) as session:

        # list to keep track of all currently running tasks
        tasks = []

        # keep going as long as queue has urls OR tasks are still running
        while queue or tasks:

            # drain the entire queue and launch every url as a concurrent task
            while queue:
                url, depth = queue.popleft()

                if depth > max_depth:
                    continue

                # create_task launches crawl_page concurrently
                # it does not wait for it to finish, it just starts it
                task = asyncio.create_task(
                    crawl_page(session, url, depth, base_domain, semaphore, requests_per_second)
                )
                # store task with its depth so we know what level it was at
                tasks.append((task, depth))

            if not tasks:
                break

            # wait for at least one task to finish before continuing
            # FIRST_COMPLETED means we don't wait for ALL tasks
            # we process results as they come in
            done, _ = await asyncio.wait(
                [t for t, _ in tasks],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # separate finished tasks from still running ones
            remaining = []
            for task, depth in tasks:
                if task in done:
                    result = task.result()

                    if result:
                        page_url, links = result

                        # record in sitemap
                        sitemap[page_url] = links

                        # add new unseen links to queue at next depth level
                        for link in links:
                            if link not in visited:
                                visited.add(link)
                                queue.append((link, depth + 1))
                else:
                    # task is still running, keep it in remaining
                    remaining.append((task, depth))

            tasks = remaining

    return sitemap


# ------------------------------------------------------------------ #
# Example usage                                                       #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    result = asyncio.run(crawl(
        start_url="https://ogee.com",
        max_depth=2,
        requests_per_second=2.0,
        max_concurrent=10,
        request_timeout=10.0
    ))

    for page, links in result.items():
        print(f"\n{page}")
        for link in links:
            print(f"  -> {link}")