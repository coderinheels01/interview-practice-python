import asyncio
import time
from collections import deque
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import aiohttp
from bs4 import BeautifulSoup
Sure. Here is how you would explain it out loud to an interviewer:

# ---

# **The overall goal:**

# "I am going to build a web crawler that starts at a URL, follows links up to a certain depth, and builds a sitemap of everything it finds. I will start simple and layer on complexity."

# ---

# **Step 1: BFS structure**

# "I will use a queue to hold URLs I need to visit. I will store each URL alongside its depth so I always know how deep I am. I will keep looping until the queue is empty."

# ---

# **Step 2: Dedup**

# "I will use a set to track every URL I have already seen. Before adding any URL to the queue I check the set first. Sets are fast for this because checking membership is instant."

# ---

# **Step 3: Depth limit**

# "When I pop a URL from the queue I check its depth. If it exceeds my max depth I skip it. This guarantees the crawler terminates."

# ---

# **Step 4: Link extraction**

# "For each page I fetch I parse the HTML using BeautifulSoup and find every anchor tag. Some links will be relative like /about so I use urljoin to convert them to absolute URLs. I filter out anything not on the same domain."

# ---

# **Step 5: robots.txt**

# "Before fetching any page I first check the domain's robots.txt to see if I am allowed. I cache the result so I only fetch robots.txt once per domain. If it returns 401 or 403 I treat the whole site as blocked. If it returns 404 I assume I am allowed."

# ---

# **Step 6: Rate limiting**

# "I track the last time I made a request to each domain in a dictionary. Before every request I calculate how much time has passed since the last one. If not enough time has passed I sleep for the difference. I use time.monotonic instead of time.time because it can never jump backwards."

# ---

# **Step 7: Concurrency**

# "I switch from requests to aiohttp so my HTTP calls are non blocking. I convert crawl into an async function and split out crawl_page as a separate worker function that handles one URL at a time. I use asyncio.create_task to launch multiple crawl_page calls concurrently. I use a semaphore to cap how many run at once. I use asyncio.wait with FIRST_COMPLETED to process results as they come in rather than waiting for everything to finish."

# ---

# **Step 8: Timeout handling**

# "I add aiohttp.ClientTimeout with two separate values. connect covers how long to wait to establish a connection. sock_read covers how long to wait for the server to send data back. These are different failure modes so they need separate timeouts. I wrap the fetch in try/except to catch TimeoutError and ClientError gracefully without crashing the crawler."

# ---

# **Step 9: Redirect loops**

# "I handle redirect loops two ways. First I set max_redirects=5 on the session so aiohttp raises TooManyRedirects if a chain gets too long. Second I check if the final URL appeared anywhere in the redirect history. If it did we went in a circle and I return None. These two work together because max_redirects catches long chains and cycle detection catches short loops like A to B back to A."

# ---

# **Step 10: URL normalization**

# "Before storing any URL I strip the fragment which is everything after the hash symbol since that just controls scroll position not page content. I also strip trailing slashes. This prevents the same page from being crawled multiple times under slightly different URL representations."

# ---

# That is the complete walkthrough. Practice saying it out loud a few times before your next round and you will be in great shape.



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
        # strip www. so ogee.com and www.ogee.com are treated as the same
        if urlparse(normalized).netloc != base_domain:
            continue

        links.append(normalized)

    # remove duplicates from this page's links using set
    print(f"[DEBUG] get_links found {len(links)} links on {base_url}")
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
    return True


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

    print(f"[DEBUG] allowed: {url}")

    # enforce rate limit before fetching
    await rate_limit(url, requests_per_second)

    # semaphore limits how many tasks can be inside here at once
    # if 10 tasks are already fetching, the 11th waits here
    # until one of the 10 finishes and releases the semaphore
    async with semaphore:
        try:
            async with session.get(
                url, allow_redirects=True, max_redirects=5
            ) as response:
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

                html = await response.text(errors="replace")
                print(
                    f"[DEBUG] fetched {url} — status {response.status}, {len(html)} chars"
                )
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


async def crawl(
    start_url,
    max_depth,
    requests_per_second=2.0,
    max_concurrent=10,
    request_timeout=10.0,
):
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
    # strip www. prefix so that ogee.com and www.ogee.com are treated as the same domain
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

    async with aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
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
                    crawl_page(
                        session, url, depth, base_domain, semaphore, requests_per_second
                    )
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


async def main():
    # reset caches between runs so stale data doesn't block the crawl
    robots_cache.clear()
    domain_last_request.clear()
    print("[DEBUG] starting crawl...")
    result = await crawl(
        start_url="https://www.ogee.com",
        max_depth=1,
        requests_per_second=2.0,
        max_concurrent=10,
        request_timeout=10.0,
    )

    print(f"[DEBUG] crawl finished, {len(result)} pages found")

    if not result:
        print("[DEBUG] sitemap is empty — no pages were recorded")
        return

    for page, links in result.items():
        print(f"hi \n{page}")
        for link in links:
            print(f"hello  -> {link}")


await main()


# import requests

# res = requests.get("https://www.ogee.com/robots.txt")
# print(res.text)
