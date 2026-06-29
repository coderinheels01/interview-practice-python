# https://www.youtube.com/watch?v=7gqFcunrFH0


class DSURollback:
    def __init__(self, n: int):
        self.parents: list[int] = list(range(n))
        self.rank: list[int] = [0] * n
        self.history: list = []
        self.components: int = n

    def snapshot(self) -> int:
        return len(self.history)

    def find(self, x: int) -> int:
        # Iterative find — no path compression to keep rollback valid
        while self.parents[x] != x:
            x = self.parents[x]
        return x

    def union(self, a: int, b: int) -> None:
        parent_a: int = self.find(a)
        parent_b: int = self.find(b)

        if parent_a == parent_b:
            self.history.append(None)
            return

        self.history.append(
            (parent_b, self.parents[parent_b], parent_a, self.rank[parent_a])
        )

        if self.rank[parent_a] == self.rank[parent_b]:
            self.parents[parent_b] = parent_a
            self.rank[parent_a] += 1
        elif self.rank[parent_a] > self.rank[parent_b]:
            self.parents[parent_b] = parent_a
        else:
            self.parents[parent_a] = parent_b

        self.components -= 1

    def rollback(self, snap: int) -> None:
        while len(self.history) > snap:
            record = self.history.pop()

            if record is None:
                continue

            b, parent_b, a, rank = record
            self.parents[b] = parent_b
            self.rank[a] = rank
            self.components += 1


class SegmentTree:
    def __init__(self, m: int):
        self.tree: list[list] = [[] for _ in range(4 * m)]

    def add_edge(
        self,
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        edge: tuple[int, int],
    ) -> None:
        if query_right < left or right < query_left:
            return
        if query_left <= left and right <= query_right:
            self.tree[node].append(edge)
            return

        mid = left + (right - left) // 2

        self.add_edge(node * 2, left, mid, query_left, query_right, edge)
        self.add_edge(node * 2 + 1, mid + 1, right, query_left, query_right, edge)


def earliest_acquaintance_time(n: int, logs: list[tuple[int, int, int, str]]) -> int:
    if not logs:
        return -1

    logs.sort(key=lambda x: x[0])

    m: int = len(logs)
    segment_tree: SegmentTree = SegmentTree(m)
    active_edges: dict[tuple[int, int], int] = {}

    for current_index, (_, a, b, operation) in enumerate(logs):
        edge: tuple[int, int] = (min(a, b), max(a, b))
        if operation == "add":
            if edge not in active_edges:
                active_edges[edge] = current_index
        else:
            start_index = active_edges.pop(edge, None)
            if start_index is not None:
                segment_tree.add_edge(1, 0, m - 1, start_index, current_index - 1, edge)

    for edge, start_index in active_edges.items():
        segment_tree.add_edge(1, 0, m - 1, start_index, m - 1, edge)

    dsu = DSURollback(n)
    answer: int | None = None

    def dfs(node: int, left: int, right: int) -> None:
        nonlocal answer
        snap = dsu.snapshot()

        for u, v in segment_tree.tree[node]:
            dsu.union(u, v)

        if left == right:
            if dsu.components == 1:
                timestamp = logs[left][0]
                if answer is None:
                    answer = timestamp
                else:
                    answer = min(answer, timestamp)
        else:
            mid = left + (right - left) // 2
            dfs(node * 2, left, mid)
            dfs(node * 2 + 1, mid + 1, right)

        dsu.rollback(snap)

    dfs(1, 0, m - 1)

    return answer if answer is not None else -1


# ── Test cases ────────────────────────────────────────────────────────────────


def run_tests():
    passed = 0
    failed = 0

    def check(name: str, result, expected):
        nonlocal passed, failed
        if result == expected:
            print(f"  PASS  {name}")
            passed += 1
        else:
            print(f"  FAIL  {name} — got {result!r}, expected {expected!r}")
            failed += 1

    # ── Basic / happy path ────────────────────────────────────────────────

    check(
        "two people — single add",
        earliest_acquaintance_time(2, [(1, 0, 1, "add")]),
        1,
    )
    check(
        "three people — linear chain connects at last edge",
        earliest_acquaintance_time(3, [(1, 0, 1, "add"), (2, 1, 2, "add")]),
        2,
    )
    check(
        "three people — all edges at same timestamp",
        earliest_acquaintance_time(3, [(5, 0, 1, "add"), (5, 1, 2, "add")]),
        5,
    )
    check(
        "logs provided out of order — should still sort correctly",
        earliest_acquaintance_time(3, [(3, 1, 2, "add"), (1, 0, 1, "add")]),
        3,
    )

    # ── Remove / follow-up variant ─────────────────────────────────────────

    check(
        "add then remove then re-add — first full connection wins",
        earliest_acquaintance_time(
            3,
            [
                (1, 0, 1, "add"),
                (2, 1, 2, "add"),  # fully connected here at t=2
                (3, 0, 1, "remove"),
                (4, 0, 1, "add"),
            ],
        ),
        2,
    )
    check(
        "remove nonexistent edge is ignored",
        earliest_acquaintance_time(
            3,
            [
                (1, 0, 2, "remove"),  # edge never existed — no-op
                (2, 0, 1, "add"),
                (3, 1, 2, "add"),
            ],
        ),
        3,
    )
    check(
        "edge added, removed, then re-added before completing the graph",
        earliest_acquaintance_time(
            3,
            [
                (1, 0, 1, "add"),
                (2, 0, 1, "remove"),
                (3, 0, 1, "add"),
                (4, 1, 2, "add"),
            ],
        ),
        4,
    )
    check(
        "all edges removed after full connection — earliest time still returned",
        earliest_acquaintance_time(
            3,
            [
                (1, 0, 1, "add"),
                (2, 1, 2, "add"),  # first full connection at t=2
                (3, 0, 1, "remove"),
                (4, 1, 2, "remove"),
            ],
        ),
        2,
    )

    # ── Impossible / edge cases ────────────────────────────────────────────

    check(
        "never fully connected — returns -1",
        earliest_acquaintance_time(3, [(1, 0, 1, "add")]),
        -1,
    )
    check(
        "empty logs — returns -1",
        earliest_acquaintance_time(3, []),
        -1,
    )
    check(
        "single person — no logs returns -1",
        earliest_acquaintance_time(1, []),
        -1,
    )

    # ── Larger graphs ──────────────────────────────────────────────────────

    check(
        "four people — star topology, connects at last spoke",
        earliest_acquaintance_time(
            4,
            [
                (1, 0, 1, "add"),
                (2, 0, 2, "add"),
                (3, 0, 3, "add"),
            ],
        ),
        3,
    )
    check(
        "four people — two isolated components, never fully connected",
        earliest_acquaintance_time(
            4,
            [
                (1, 0, 1, "add"),
                (2, 2, 3, "add"),
            ],
        ),
        -1,
    )
    check(
        "five people — chain connected one by one",
        earliest_acquaintance_time(
            5,
            [
                (1, 0, 1, "add"),
                (2, 1, 2, "add"),
                (3, 2, 3, "add"),
                (4, 3, 4, "add"),
            ],
        ),
        4,
    )
    check(
        "five people — bridge removed then restored",
        earliest_acquaintance_time(
            5,
            [
                (1, 0, 1, "add"),
                (2, 1, 2, "add"),
                (3, 2, 3, "add"),
                (4, 3, 4, "add"),  # fully connected at t=4
                (5, 2, 3, "remove"),
                (6, 2, 3, "add"),
            ],
        ),
        4,
    )

    print(f"\n{passed} passed, {failed} failed")


run_tests()
