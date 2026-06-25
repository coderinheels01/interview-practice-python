# =============================================================================
# PROBLEM: LRU Cache with Even-Score Eviction Policy
# =============================================================================
# Design a cache that stores key→content pairs up to a fixed capacity.
# When the cache is full and a new key needs to be inserted, evict the entry
# whose access score is even AND whose last_accessed timestamp is the oldest
# among all even-scored entries.
#
# Each entry tracks a `score` that increments on every put (update) or get.
# A freshly inserted key starts at score 0 (even), making it immediately
# eligible for eviction if needed.
#
# -----------------------------------------------------------------------------
# DATA STRUCTURES
# -----------------------------------------------------------------------------
# 1. dict[int, Entry]  (self.cache)
#    - Main key→Entry store. O(1) average lookup, insert, delete.
#
# 2. min-heap of (score, last_accessed, key)  (self.even_score_entries)
#    - Tracks entries whose score was even at the time of the push.
#    - Min-heap ordering: smallest score first; ties broken by oldest
#      last_accessed timestamp (smallest float wins).
#    - Uses a *lazy-deletion* strategy: stale entries (whose score or
#      last_accessed no longer matches the live entry) are left in the heap
#      and skipped at eviction time rather than being removed eagerly.
#
# -----------------------------------------------------------------------------
# STEP-BY-STEP FLOW
# -----------------------------------------------------------------------------
# put(key, content):
#   1. If the key already exists → update content, increment score,
#      refresh last_accessed. If the new score is even, push a fresh
#      heap entry.
#   2. If the key is new and the cache is at capacity → call _evict_entry()
#      to free a slot, then insert the new Entry with score=0.
#      Score 0 is even, so a heap entry is pushed immediately.
#
# get(key) → Entry | None:
#   1. Look up the key in the dict. If absent, return None.
#   2. Increment score and refresh last_accessed.
#   3. If the new score is even, push a heap entry for potential future
#      eviction.
#   4. Return the Entry.
#
# _evict_entry():
#   1. Pop from the min-heap (lowest score, oldest timestamp).
#   2. Validate the popped entry: confirm the live Entry in self.cache
#      still has the exact same score AND last_accessed. If not, the
#      heap entry is stale (the entry was accessed again since the push)
#      → discard and pop the next one.
#   3. Once a valid entry is found, delete it from self.cache.
#
# -----------------------------------------------------------------------------
# WHY LAZY DELETION?
# -----------------------------------------------------------------------------
# Eagerly removing a heap entry when a key's score changes would require
# either a heap decrease-key operation (not supported by Python's heapq) or
# maintaining a separate index — both add complexity. Lazy deletion keeps the
# code simple: stale entries are cheap to skip and each entry is popped at
# most once across all operations, preserving O(log n) amortized eviction cost.
#
# -----------------------------------------------------------------------------
# COMPLEXITY SUMMARY
# -----------------------------------------------------------------------------
# put:          O(log n) amortized  |  O(1) space
# get:          O(log n)            |  O(1) space
# _evict_entry: O(log n) amortized  |  O(1) space
# Overall space: O(n) for n = max_size (cache dict + heap entries)
# =============================================================================

import time
import heapq


class Entry:
    def __init__(self, key: int, content: str, score: int = 0):
        self.key: int = key
        self.content: str = content
        self.score: int = score
        self.last_accessed: float = time.time()


class Cache:
    """
    Content cache with even-score eviction policy.

    Overall Space: O(n) — where n is max_size. The cache dict holds at most n
                   entries. The even_score_entries heap can hold at most O(n * k)
                   entries where k is the max number of times a single key's score
                   transitions through even values, but in practice is bounded by
                   the total number of put/get operations across all keys.
    """

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache: dict[int, Entry] = {}
        self.even_score_entries: list[tuple[int, float, int]] = []

    def _add_to_cache(self, key: int, content: str):
        """
        Time:  O(log n) — dict lookup/insert is O(1), but heappush is O(log n)
                          where n is the number of entries in even_score_entries.
        Space: O(1) — no additional space proportional to input; the heap entry
                      pushed is a fixed-size tuple.
        """
        if key in self.cache:
            self.cache[key].content = content
            self.cache[key].score += 1
            self.cache[key].last_accessed = time.time()
        else:
            self.cache[key] = Entry(key, content)
        if self.cache[key].score % 2 == 0:
            heapq.heappush(
                self.even_score_entries,
                (
                    self.cache[key].score,
                    self.cache[key].last_accessed,
                    self.cache[key].key,
                ),
            )

    def _evict_entry(self):
        """
        Time:  O(k log n) — each heappop is O(log n); we may pop k stale entries
                            before finding a valid one. In the worst case k = n,
                            giving O(n log n), but amortized across all operations
                            each heap entry is popped at most once, so the amortized
                            cost per eviction is O(log n).
        Space: O(1) — no additional allocations; stale entries are just discarded.
        """
        if not self.even_score_entries:
            return
        while self.even_score_entries:
            score, last_accessed, key = heapq.heappop(self.even_score_entries)
            entry = self.cache.get(key)
            if entry and entry.score == score and entry.last_accessed == last_accessed:
                del self.cache[key]
                return

    def put(self, key: int, content: str):
        """
        Time:  O(log n) — O(1) for the dict check; if eviction is needed,
                          _evict_entry is O(log n) amortized; _add_to_cache is
                          O(log n) for the potential heappush. Overall O(log n).
        Space: O(1) — no additional space beyond what _add_to_cache and
                      _evict_entry already account for.
        """
        if key not in self.cache and len(self.cache) >= self.max_size:
            self._evict_entry()
        self._add_to_cache(key, content)

    def get(self, key: int) -> str | None:
        """
        Time:  O(log n) — O(1) for the dict lookup and score increment; heappush
                          is O(log n) when the new score is even. Overall O(log n).
        Space: O(1) — at most one fixed-size tuple pushed onto the heap.
        """
        if key in self.cache:
            self.cache[key].score += 1
            self.cache[key].last_accessed = time.time()
            if self.cache[key].score % 2 == 0:
                heapq.heappush(
                    self.even_score_entries,
                    (
                        self.cache[key].score,
                        self.cache[key].last_accessed,
                        self.cache[key].key,
                    ),
                )
            return self.cache[key]
        return None


# Write your solution here
def solve():
    print("=" * 70)
    print("TEST CASE 1: Basic put and get")
    print("=" * 70)
    cache = Cache(max_size=3)
    cache.put(1, "content1")
    cache.put(2, "content2")
    cache.put(3, "content3")

    result = cache.get(1)
    print(f"Get key 1: {result.content}")
    print(f"Cache size: {len(cache.cache)}")
    print()

    print("=" * 70)
    print("TEST CASE 2: Score incrementing on get")
    print("=" * 70)
    cache = Cache(max_size=3)
    cache.put(1, "content1")  # score = 0
    print(f"After put(1): score = {cache.cache[1].score}")

    cache.get(1)  # score should increase
    print(f"After get(1): score = {cache.cache[1].score}")

    cache.get(1)  # score should increase again
    print(f"After get(1) again: score = {cache.cache[1].score}")

    print("=" * 70)
    print("TEST CASE 3: Score incrementing on put update")
    print("=" * 70)
    cache = Cache(max_size=3)
    cache.put(1, "content1")  # score = 0
    print(f"After put(1): score = {cache.cache[1].score}")

    cache.put(1, "new_content")  # update, score should increase
    print(f"After put(1) update: score = {cache.cache[1].score}")
    print()

    print("=" * 70)
    print("TEST CASE 4: Even score tracking")
    print("=" * 70)
    cache = Cache(max_size=5)
    cache.put(1, "content1")  # score = 0 (even)
    cache.get(1)  # score = 1 (odd)
    cache.get(1)  # score = 2 (even)

    print(f"Key 1 score: {cache.cache[1].score}")
    print(f"Is score even? {cache.cache[1].score % 2 == 0}")
    print(f"Even score entries count: {len(cache.even_score_entries)}")
    print()

    print("=" * 70)
    print("TEST CASE 5: Cache capacity and eviction")
    print("=" * 70)
    cache = Cache(max_size=2)
    cache.put(1, "content1")  # score = 0
    print(f"After put(1): cache size = {len(cache.cache)}")

    cache.put(2, "content2")  # score = 0
    print(f"After put(2): cache size = {len(cache.cache)}")

    cache.put(3, "content3")  # should evict
    print(f"After put(3): cache size = {len(cache.cache)}")
    print(f"Keys in cache: {list(cache.cache.keys())}")
    print()

    print("=" * 70)
    print("TEST CASE 6: LRU tiebreaker")
    print("=" * 70)
    cache = Cache(max_size=3)
    cache.put(1, "content1")  # score = 0, accessed at time T1
    time.sleep(0.1)
    cache.put(2, "content2")  # score = 0, accessed at time T2 (later)

    print(f"Key 1 last_accessed: {cache.cache[1].last_accessed}")
    print(f"Key 2 last_accessed: {cache.cache[2].last_accessed}")
    print(
        f"Key 1 is older? {cache.cache[1].last_accessed < cache.cache[2].last_accessed}"
    )
    print()


solve()
