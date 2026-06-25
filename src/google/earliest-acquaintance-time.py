"""
Earliest Acquaintance Time
There are n people in a social group, labeled from 0 to n−1. You are given an array logs where:

logs[i] = [timestamp_i, person_A_i, person_B_i]

This indicates that person_A and person_B became friends at timestamp.

Friendship is symmetric (if A is friends with B, B is friends with A) and transitive (if A is friends with B and B is friends with C, A is acquainted with C).

The Task: Return the earliest timestamp for which every person became acquainted with every other person. If it is impossible, return −1.

Follow-up: Two types of logs

Add Friend - A and B become friends Remove Friend - If A and B are friends, unfriend them Two people can be connected and disconnected multiple times.

Given this, find the earliest timestamp when all of them become friends.


Python
Save

1234567
Output

Run Code

"""

from collections import deque, defaultdict


# def is_connected(n: int, active_edges: set) -> bool:
#     graph: dict[str, set] = collections.defaultdict(set)

#     for i in range(n):
#         graph[i] = {i}

#     for p1, p2 in active_edges:
#         graph[p1] = graph[p1].union(graph[p2])

#         for p3 in graph[p1]:
#             graph[p3] = graph[p1]

#         if len(graph[p1]) == n:
#             return True
#     return False


def is_connected(n: int, active_edges: set) -> bool:
    if n == 1:
        return True

    graph: dict[int, list] = defaultdict(list)

    for p1, p2 in active_edges:
        graph[p1].append(p2)
        graph[p2].append(p1)

    visited: set[int] = {0}
    queue: deque[int] = deque([0])

    while queue:
        node: int = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == n


def earliest_acquaintance_time(n: int, logs: list[tuple[int, int, int, str]]) -> int:
    active_edges: set = set()

    logs = sorted(logs, key=lambda x: x[0])

    for time, p1, p2, operation in logs:
        edge: tuple[int, int] = (min(p1, p2), max(p1, p2))
        if operation == "add":
            active_edges.add(edge)
        elif operation == "remove":
            active_edges.discard(edge)
        if is_connected(n=n, active_edges=active_edges):
            return time
    return -1


def solve():
    pass


solve()


# ── Test cases ──────────────────────────────────────────────────────────────


def run_tests():
    passed = 0
    failed = 0

    def check(name, result, expected):
        nonlocal passed, failed
        if result == expected:
            print(f"  PASS  {name}")
            passed += 1
        else:
            print(f"  FAIL  {name} — got {result}, expected {expected}")
            failed += 1

    # Basic / happy path
    check(
        "two people single add",
        earliest_acquaintance_time(2, [(1, 0, 1, "add")]),
        1,
    )
    check(
        "three people linear chain",
        earliest_acquaintance_time(3, [(1, 0, 1, "add"), (2, 1, 2, "add")]),
        2,
    )
    check(
        "three people all at same timestamp",
        earliest_acquaintance_time(3, [(5, 0, 1, "add"), (5, 1, 2, "add")]),
        5,
    )
    check(
        "logs out of order",
        earliest_acquaintance_time(3, [(3, 1, 2, "add"), (1, 0, 1, "add")]),
        3,
    )

    # Remove / follow-up variant
    check(
        "add then remove breaks connectivity",
        earliest_acquaintance_time(
            3,
            [
                (1, 0, 1, "add"),
                (2, 1, 2, "add"),
                (3, 0, 1, "remove"),
                (4, 0, 1, "add"),
            ],
        ),
        2,  # fully connected at t=2; removal at t=3 happens after first full connection
    )
    check(
        "remove nonexistent edge is ignored",
        earliest_acquaintance_time(
            3,
            [
                (1, 0, 2, "remove"),
                (2, 0, 1, "add"),
                (3, 1, 2, "add"),
            ],
        ),
        3,
    )
    check(
        "reconnect multiple times",
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

    # Impossible cases
    check(
        "never connected returns -1",
        earliest_acquaintance_time(3, [(1, 0, 1, "add")]),
        -1,
    )
    check(
        "empty logs returns -1",
        earliest_acquaintance_time(3, []),
        -1,
    )
    check(
        "all removed after full connection returns first connected time",
        earliest_acquaintance_time(
            3,
            [
                (1, 0, 1, "add"),
                (2, 1, 2, "add"),
                (3, 0, 1, "remove"),
                (4, 1, 2, "remove"),
            ],
        ),
        2,  # fully connected at t=2; removals happen after
    )

    # Larger graph
    check(
        "four people star topology",
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
        "four people missing component returns -1",
        earliest_acquaintance_time(
            4,
            [
                (1, 0, 1, "add"),
                (2, 2, 3, "add"),
            ],
        ),
        -1,
    )

    print(f"\n{passed} passed, {failed} failed")


run_tests()
