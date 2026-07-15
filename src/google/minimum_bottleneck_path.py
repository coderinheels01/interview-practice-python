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
# =============================================================================
# Step-by-step walkthrough (using the example above)
# =============================================================================
#
# Initial state
# ─────────────
# best = [inf, 0, inf, inf, inf]   (index = node number, best[1]=0 = start)
# heap = [(0, 1)]
#
#          [∞]          [∞]
#           2            3
#          ↗              ↘
#    (3)  /    (1)          \ (2)
#        /                   ↘
#   1 [0]                    4 [∞]
#          \______(5)________↗
#                    via 2
#
# ─────────────────────────────────────────────────────────────────────────────
# Step 1 — pop (0, node=1) from heap
# ─────────────────────────────────────────────────────────────────────────────
#   Process node 1  (bottleneck so far = 0)
#     → neighbor 2:  max(0, 3) = 3  < inf  ✓  best[2] = 3,  parent[2] = 1
#     → neighbor 3:  max(0, 1) = 1  < inf  ✓  best[3] = 1,  parent[3] = 1
#
#   best = [inf, 0, 3, 1, inf]
#   heap = [(1, 3), (3, 2)]
#
#          [3]          [1]
#           2 ←set       3 ←set
#          ↗              ↘
#    (3)  /    (1)          \ (2)
#        /                   ↘
#   1 [0]                    4 [∞]
#
# ─────────────────────────────────────────────────────────────────────────────
# Step 2 — pop (1, node=3) from heap  ← smallest bottleneck wins
# ─────────────────────────────────────────────────────────────────────────────
#   Process node 3  (bottleneck so far = 1)
#     → neighbor 4:  max(1, 2) = 2  < inf  ✓  best[4] = 2,  parent[4] = 3
#
#   best = [inf, 0, 3, 1, 2]
#   heap = [(2, 4), (3, 2)]
#
#          [3]          [1]
#           2            3
#          ↗              ↘ ←set
#    (3)  /    (1)          \ (2)
#        /                   ↘
#   1 [0]                    4 [2]
#
# ─────────────────────────────────────────────────────────────────────────────
# Step 3 — pop (2, node=4) from heap
# ─────────────────────────────────────────────────────────────────────────────
#   Process node 4  (bottleneck so far = 2)
#     → no outgoing edges
#
#   best = [inf, 0, 3, 1, 2]   ← unchanged, end node reached
#   heap = [(3, 2)]
#
# ─────────────────────────────────────────────────────────────────────────────
# Step 4 — pop (3, node=2) from heap
# ─────────────────────────────────────────────────────────────────────────────
#   Process node 2  (bottleneck so far = 3)
#     → neighbor 4:  max(3, 5) = 5  < best[4]=2?  NO ✗  skip (stale path)
#
#   heap = []  → done
#
# ─────────────────────────────────────────────────────────────────────────────
# Final state
# ─────────────────────────────────────────────────────────────────────────────
#
#          [3]          [1]
#           2            3
#          ↗              ↘
#    (3)  /    (1)          \ (2)
#        /                   ↘
#   1 [0]                    4 [2]  ← answer
#
#   Optimal path (via parents): 4 ← 3 ← 1  →  [1, 3, 4]
#   Bottleneck: 2
#
# Key insight: node 3 is processed before node 2 even though node 2 was pushed
# onto the heap first. The min-heap always pops the SMALLEST bottleneck next,
# which steers the algorithm toward the cheap path through 3 (weight 1) and
# away from the expensive path through 2 (weight 3). This is exactly the same
# greedy mechanism as classic Dijkstra — just with max() instead of +.
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
) -> tuple[int, list[int]] | tuple[None, None]:
    """Return the minimum security level and the path from start to end.

    Args:
        edges: List of (u, v, weight) directed edges.
        n:     Number of nodes (nodes are labelled 1..n).
        start: Source node.
        end:   Destination node.

    Returns:
        A tuple of (bottleneck, path) where bottleneck is the minimum max-edge
        weight along the optimal path and path is the list of nodes from start
        to end. Returns (None, None) if no path exists.
    """
    if not edges:
        return None, None

    # Build adjacency list
    neighbors_map: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, weight in edges:
        neighbors_map[u].append((v, weight))

    # best[node] = min bottleneck cost found so far to reach node
    best: list[int | float] = [float("inf")] * (n + 1)
    best[start] = 0

    # parent[node] = the node we came from when we found the best path to node.
    # Used to reconstruct the path once we reach `end`.
    parent: list[int | None] = [None] * (n + 1)

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
                # Record that we reached `neighbor` optimally via `node`
                parent[neighbor] = node
                heapq.heappush(heap, (new_bottleneck, neighbor))

    if best[end] == float("inf"):
        return None, None

    # Reconstruct path by walking parent pointers from end back to start
    path: list[int] = []
    node = end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return best[end], path


# =============================================================================
# Test cases
# =============================================================================


def solve():
    passed = 0
    failed = 0

    def check(description: str, result, expected_cost, expected_path=None):
        nonlocal passed, failed
        cost, path = result
        cost_ok = cost == expected_cost
        path_ok = expected_path is None or path == expected_path
        status = "PASS" if (cost_ok and path_ok) else "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1
        print(f"[{status}] {description}")
        print(f"       bottleneck={cost}  path={path}")
        if status == "FAIL":
            print(f"       expected cost={expected_cost}, path={expected_path}")

    # ------------------------------------------------------------------
    # Test 1: Example from the problem statement
    # Paths: 1->2->4 (bottleneck 5), 1->3->4 (bottleneck 2)
    # Expected bottleneck: 2, path: [1, 3, 4]
    # ------------------------------------------------------------------
    check(
        "Example: 1->3->4 is cheaper bottleneck than 1->2->4",
        minimum_bottleneck_path(
            edges=[(1, 2, 3), (1, 3, 1), (2, 4, 5), (3, 4, 2)],
            n=4,
            start=1,
            end=4,
        ),
        expected_cost=2,
        expected_path=[1, 3, 4],
    )

    # ------------------------------------------------------------------
    # Test 2: Direct single edge
    # Expected bottleneck: 7, path: [1, 2]
    # ------------------------------------------------------------------
    check(
        "Single direct edge",
        minimum_bottleneck_path(
            edges=[(1, 2, 7)],
            n=2,
            start=1,
            end=2,
        ),
        expected_cost=7,
        expected_path=[1, 2],
    )

    # ------------------------------------------------------------------
    # Test 3: No path exists between start and end
    # Expected: (None, None)
    # ------------------------------------------------------------------
    check(
        "No path exists",
        minimum_bottleneck_path(
            edges=[(1, 2, 3), (3, 4, 2)],
            n=4,
            start=1,
            end=4,
        ),
        expected_cost=None,
        expected_path=None,
    )

    # ------------------------------------------------------------------
    # Test 4: Empty edge list
    # Expected: (None, None)
    # ------------------------------------------------------------------
    check(
        "Empty edge list",
        minimum_bottleneck_path(
            edges=[],
            n=4,
            start=1,
            end=4,
        ),
        expected_cost=None,
        expected_path=None,
    )

    # ------------------------------------------------------------------
    # Test 5: Start equals end — zero bottleneck needed
    # Expected bottleneck: 0, path: [1]
    # ------------------------------------------------------------------
    check(
        "Start equals end",
        minimum_bottleneck_path(
            edges=[(1, 2, 5)],
            n=2,
            start=1,
            end=1,
        ),
        expected_cost=0,
        expected_path=[1],
    )

    # ------------------------------------------------------------------
    # Test 6: Multiple parallel paths — pick the one with lowest max edge
    # Paths: 1->2->5 (max 10), 1->3->5 (max 4), 1->4->5 (max 8)
    # Expected bottleneck: 4, path: [1, 3, 5]
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
        expected_cost=4,
        expected_path=[1, 3, 5],
    )

    # ------------------------------------------------------------------
    # Test 7: Linear chain — bottleneck is the single max edge in the chain
    # Path: 1->2->3->4->5, edges: 1,2,3,4 → bottleneck = 4
    # Expected bottleneck: 4, path: [1, 2, 3, 4, 5]
    # ------------------------------------------------------------------
    check(
        "Linear chain — bottleneck is max edge weight",
        minimum_bottleneck_path(
            edges=[(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 5, 4)],
            n=5,
            start=1,
            end=5,
        ),
        expected_cost=4,
        expected_path=[1, 2, 3, 4, 5],
    )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(f"\nResults: {passed} passed, {failed} failed")


solve()
