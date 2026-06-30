import heapq
from collections import defaultdict

# =============================================================================
# Problem: Clearance Bottleneck
# =============================================================================
#
# You're given a graph with V nodes and E edges. Each edge has a security level.
# Given a security key with security level S, you can only traverse edges with
# security levels <= S.
#
# The goal is to find the MINIMUM security level required to travel from u to v.
#
# Example:
#   Nodes: 1, 2, 3, 4
#   Edge   | Security Level
#   (1->2) | 3
#   (1->3) | 1
#   (2->4) | 5
#   (3->4) | 2
#
#   Start node u: 1
#   End node v:   4
#
#   Possible paths:
#     1 -> 2 -> 4  requires security level max(3, 5) = 5
#     1 -> 3 -> 4  requires security level max(1, 2) = 2  ← optimal
#
#   Answer: 2
#
# =============================================================================
# Approach: Modified Dijkstra
# =============================================================================
#
# Instead of minimising the *sum* of edge weights (classic Dijkstra), we
# minimise the *maximum* edge weight along the path — the bottleneck cost.
#
# Key idea:
#   best[node] = the minimum bottleneck cost to reach `node` from `start`.
#
# At each step we pop the node with the smallest current bottleneck from the
# min-heap. For every neighbour we compute:
#
#   new_bottleneck = max(current_bottleneck_to_node, edge_weight)
#
# If new_bottleneck < best[neighbour], we found a better path and push it.
#
# This is a direct analogue of Dijkstra's relaxation step — just swap "sum"
# for "max". The greedy argument holds for the same reason: once a node is
# popped from the min-heap its bottleneck value is already optimal.
#
# Video reference: https://www.youtube.com/watch?v=j0OUwduDOS0
#
# Time  Complexity: O((V + E) log V)
#   - Each node is pushed/popped from the heap at most once per edge → O(E log V)
#   - Initial heap operations → O(V log V)
#
# Space Complexity: O(V + E)
#   - Adjacency list stores all edges → O(E)
#   - `best` array and heap store one entry per node → O(V)
#
# =============================================================================


def minimum_bottleneck_path(
    edges: list[tuple[int, int, int]], n: int, start: int, end: int
) -> int | None:
    """Return the minimum security level needed to travel from start to end.

    Args:
        edges: List of (u, v, weight) directed edges.
        n:     Number of nodes (nodes are labelled 1..n).
        start: Source node.
        end:   Destination node.

    Returns:
        The minimum bottleneck (max edge weight along the best path), or None
        if no path exists.
    """
    if not edges:
        return None

    # Build adjacency list
    neighbors_map: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, weight in edges:
        neighbors_map[u].append((v, weight))

    # best[node] = min bottleneck cost found so far to reach node
    best: list[int | float] = [float("inf")] * (n + 1)
    best[start] = 0

    # Min-heap: (bottleneck_cost, node)
    heap: list[tuple[int | float, int]] = [(0, start)]
    heapq.heapify(heap)

    while heap:
        prev_bottleneck, node = heapq.heappop(heap)

        # Stale entry — a better path was already found
        if prev_bottleneck > best[node]:
            continue

        for neighbor, edge_weight in neighbors_map[node]:
            new_bottleneck = max(edge_weight, prev_bottleneck)
            if new_bottleneck < best[neighbor]:
                best[neighbor] = new_bottleneck
                heapq.heappush(heap, (new_bottleneck, neighbor))

    return None if best[end] == float("inf") else best[end]


# =============================================================================
# Test cases
# =============================================================================


def solve():
    passed = 0
    failed = 0

    def check(description: str, result, expected):
        nonlocal passed, failed
        status = "PASS" if result == expected else "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1
        print(f"[{status}] {description}")
        if status == "FAIL":
            print(f"       expected={expected}, got={result}")

    # ------------------------------------------------------------------
    # Test 1: Example from the problem statement
    # Paths: 1->2->4 (bottleneck 5), 1->3->4 (bottleneck 2)
    # Expected: 2
    # ------------------------------------------------------------------
    check(
        "Example: 1->3->4 is cheaper bottleneck than 1->2->4",
        minimum_bottleneck_path(
            edges=[(1, 2, 3), (1, 3, 1), (2, 4, 5), (3, 4, 2)],
            n=4,
            start=1,
            end=4,
        ),
        expected=2,
    )

    # ------------------------------------------------------------------
    # Test 2: Direct single edge
    # Expected: 7
    # ------------------------------------------------------------------
    check(
        "Single direct edge",
        minimum_bottleneck_path(
            edges=[(1, 2, 7)],
            n=2,
            start=1,
            end=2,
        ),
        expected=7,
    )

    # ------------------------------------------------------------------
    # Test 3: No path exists between start and end
    # Expected: None
    # ------------------------------------------------------------------
    check(
        "No path exists",
        minimum_bottleneck_path(
            edges=[(1, 2, 3), (3, 4, 2)],
            n=4,
            start=1,
            end=4,
        ),
        expected=None,
    )

    # ------------------------------------------------------------------
    # Test 4: Empty edge list
    # Expected: None
    # ------------------------------------------------------------------
    check(
        "Empty edge list",
        minimum_bottleneck_path(
            edges=[],
            n=4,
            start=1,
            end=4,
        ),
        expected=None,
    )

    # ------------------------------------------------------------------
    # Test 5: Start equals end — zero bottleneck needed
    # Expected: 0
    # ------------------------------------------------------------------
    check(
        "Start equals end",
        minimum_bottleneck_path(
            edges=[(1, 2, 5)],
            n=2,
            start=1,
            end=1,
        ),
        expected=0,
    )

    # ------------------------------------------------------------------
    # Test 6: Multiple parallel paths — pick the one with lowest max edge
    # Paths: 1->2->5 (max 10), 1->3->5 (max 4), 1->4->5 (max 8)
    # Expected: 4
    # ------------------------------------------------------------------
    check(
        "Multiple parallel paths — choose lowest bottleneck",
        minimum_bottleneck_path(
            edges=[
                (1, 2, 10),
                (2, 5, 10),
                (1, 3, 4),
                (3, 5, 4),
                (1, 4, 8),
                (4, 5, 8),
            ],
            n=5,
            start=1,
            end=5,
        ),
        expected=4,
    )

    # ------------------------------------------------------------------
    # Test 7: Linear chain — bottleneck is the single max edge in the chain
    # Path: 1->2->3->4->5, edges: 1,2,3,4 → bottleneck = 4
    # Expected: 4
    # ------------------------------------------------------------------
    check(
        "Linear chain — bottleneck is max edge weight",
        minimum_bottleneck_path(
            edges=[(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 5, 4)],
            n=5,
            start=1,
            end=5,
        ),
        expected=4,
    )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(f"\nResults: {passed} passed, {failed} failed")


solve()
