"""190. Detect a Cycle in an Undirected Graph

Given an undirected graph with V vertices labeled from 0 to V - 1,
determine whether it contains any cycles. Return True if it does and False
otherwise. A cycle is a closed path with no repeated vertices except its
starting and ending vertex; traversing one edge out and back is not a cycle.

The graph is represented by an adjacency list: adj[i] contains the vertices
directly connected to vertex i. Each undirected edge appears in both vertices'
neighbor lists. The graph has no self-edges and may be disconnected.

In this function, derive V from len(adj) rather than passing it separately.

Example 1:
    Input: V = 6,
           adj = [[1, 3], [0, 2, 4], [1, 5], [0, 4], [1, 3, 5], [2, 4]]
    Output: True
    Explanation: The graph contains the cycle 1 -> 2 -> 5 -> 4 -> 1.
    The original example's path 0 -> 1 -> 2 -> 5 -> 4 -> 1 reaches this cycle
    from vertex 0; vertex 0 is not part of that particular cycle.

Example 2:
    Input: V = 4, adj = [[1, 2], [0], [0, 3], [2]]
    Output: False
    Explanation: The graph contains no cycles.

Practice example:
    Input: V = 4, adj = [[1, 2], [0, 2], [0, 1, 3], [2]]
    Choose the correct output: True or False.

Constraints:
    - E is the number of undirected edges.
    - 1 <= V, E <= 10**4 (as stated in the supplied question).
    - len(adj) == V.
    - Neighbor indices are in the range 0 to V - 1.
    - No vertex is connected to itself.

    https://www.youtube.com/watch?v=BPlrALf1LDU&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=11
"""

from collections import deque


def detect_cycle_undirected_graph_bfs(adj: list[list[int]]) -> bool:
    """Return whether any component of an undirected graph contains a cycle.

    Args:
        adj: Adjacency list for vertices 0 through len(adj) - 1. Each edge
            appears in both endpoints' neighbor lists. The graph has no
            self-edges and may contain isolated vertices or disconnected
            components. Assumes a simple graph with no parallel edges.

    Returns:
        True as soon as a cycle is detected, otherwise False after checking
        all components. The input adjacency list is not modified.

    Approach:
        Breadth-First Search (BFS) with parent tracking.
        1. Get the vertex count from len(adj) and create one visited flag per
           vertex. Share these flags across all component searches.
        2. Define a helper to search one component. Initialize its queue with
           (starting_vertex, -1), where -1 means the start has no parent.
           Mark the starting vertex visited immediately.
        3. Remove the oldest (current, parent) pair with popleft() and examine
           each neighbor of current. The parent is the vertex from which
           current was first discovered.
        4. Skip the parent connection. Every undirected edge appears in both
           directions, so seeing the edge back to the parent is expected and
           does not by itself indicate a cycle.
        5. For an unvisited non-parent neighbor, enqueue (neighbor, current)
           and mark it visited immediately. Marking on enqueue prevents the
           same vertex from being added multiple times while waiting.
        6. If a non-parent neighbor is already visited, return True. There is
           already a path between the vertices through the BFS discovery
           edges; this additional edge closes a cycle. A visited vertex may
           still be waiting in the queue; it need not have been processed.
        7. If the queue empties without a cycle, return False from the helper.
        8. In the outer loop, start the helper at each still-unvisited vertex.
           This checks disconnected components too, including cycles beyond
           an isolated starting vertex. Return True if any helper finds a
           cycle; otherwise return False after the loop.

        Walkthrough: adj = [[1, 2], [0, 2], [0, 1]]
            - Start at 0: queue = [(0, -1)], visited = [True, False, False].
            - Pop 0. Discover 1 and 2, mark both visited, and enqueue them:
              queue = [(1, 0), (2, 0)].
            - Pop (1, 0). Skip neighbor 0 because it is the parent.
            - Neighbor 2 is already visited and is not the parent. Return
              True: the edges form the cycle 0 -> 1 -> 2 -> 0.

        For adj = [[1], [0]], vertex 1 only sees its parent 0. That edge is
        skipped, the queue empties, and the result is False.

    Time Complexity:
        O(V + E), where V = len(adj) and E is the number of undirected edges.
        The outer loop examines at most V vertices. Each vertex is enqueued
        and dequeued at most once because it is marked when enqueued.
        Across all vertices, the neighbor lists contain 2E entries, since
        each undirected edge is stored at both ends. Thus the total work is
        O(V + 2E) = O(V + E), not O(V * E): each vertex scans only its own
        neighbors, not every edge in the graph. A cycle can stop the search
        early. The input is already an adjacency list; no conversion is needed.

    Space Complexity:
        O(V) auxiliary space, excluding the input adjacency list. visited
        holds V boolean flags, and the queue holds at most V (vertex, parent)
        pairs. A wide BFS frontier can contain many vertices at once. These
        costs add to O(V) + O(V) = O(V). Component searches run sequentially,
        so their queue sizes do not multiply. There is no recursive call stack,
        and the result is a single boolean.
    """
    # 1. Share one visited flag per vertex across all component searches.
    vertices: int = len(adj)
    visited: list[bool] = [False] * vertices

    def detect_cycle(vertex: int) -> bool:
        # 2. Start a component search; the root has no parent.
        queue: deque[tuple[int, int]] = deque([(vertex, -1)])
        visited[vertex] = True

        while queue:
            # 3. Process vertices in FIFO order and inspect their neighbors.
            current, parent = queue.popleft()
            for neighbor in adj[current]:
                # 4. Ignore the reverse edge leading back to the parent.
                if neighbor != parent:
                    if not visited[neighbor]:
                        # 5. Record discovery now, before this vertex is processed.
                        queue.append((neighbor, current))
                        visited[neighbor] = True
                    else:
                        # 6. An already-discovered non-parent neighbor closes a cycle.
                        return True
        # 7. This component contains no cycle.
        return False

    # 8. Check every component, stopping as soon as any cycle is found.
    for vertex in range(vertices):
        if not visited[vertex] and detect_cycle(vertex=vertex):
            return True

    return False


def detect_cycle_undirected_graph_dfs(adj: list[list[int]]) -> bool:
    """Return whether a simple undirected graph contains a cycle.

    Approach:
        Recursive Depth-First Search (DFS) with parent tracking.
        1. Create one visited flag per vertex, shared across all DFS calls.
        2. Start DFS from each unvisited vertex to cover disconnected
           components. Use parent=-1 for each component's starting vertex.
        3. Mark the current vertex visited when entering its DFS call.
        4. Skip the neighbor equal to the parent. Each undirected edge is
           listed in both directions, so the edge back to the parent does
           not indicate a cycle.
        5. If any other neighbor is already visited, return True: that edge
           closes a cycle through vertices already connected by DFS.
        6. Recursively explore each unvisited neighbor with current as its
           parent. If the child returns True, return True too, propagating
           cycle detection through every caller to the outer function.
           If the child returns False, continue to the next neighbor;
           returning False immediately would leave other branches unchecked.
        7. Return False from a DFS call only after all its neighbors have
           been checked. Return False overall if no component has a cycle.

        Example: adj = [[1, 2], [0], [0, 3], [2]]
            DFS follows 0 -> 1. Vertex 1 skips its parent 0 and returns
            False. Vertex 0 resumes its loop and explores 2 -> 3. Each
            vertex only encounters its parent as an already-visited
            neighbor, so all calls return False: this graph is a tree.

    Time Complexity:
        O(V + E). Each vertex is visited once, and each undirected edge
        appears twice across the adjacency lists.

    Space Complexity:
        O(V) auxiliary space for visited flags and the recursion stack.
        A long path can require V nested calls and exceed Python's recursion
        limit. Use iterative DFS when deep graphs must be supported.

    https://www.youtube.com/watch?v=zQ3zgFypzX4&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=13

    """
    vertices: int = len(adj)
    visited: list[bool] = [False] * vertices

    def dfs(current: int, parent: int) -> bool:
        visited[current] = True

        for neighbor in adj[current]:
            if neighbor == parent:
                continue

            if visited[neighbor]:
                return True

            if dfs(neighbor, current):
                return True
        return False

    for vertex in range(vertices):
        if not visited[vertex] and dfs(current=vertex, parent=-1):
            return True

    return False


def solve() -> None:
    adj: list[list[int]] = [
        [1, 3],
        [0, 2, 4],
        [1, 5],
        [0, 4],
        [1, 3, 5],
        [2, 4],
    ]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Example 2: acyclic tree.
    adj: list[list[int]] = [[1, 2], [0], [0, 3], [2]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: triangle with a tail.
    adj: list[list[int]] = [[1, 2], [0, 2], [0, 1, 3], [2]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum edge count: one edge is not a cycle.
    adj: list[list[int]] = [[1], [0]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Three-vertex path.
    adj: list[list[int]] = [[1], [0, 2], [1]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest simple cycle: a triangle.
    adj: list[list[int]] = [[1, 2], [0, 2], [0, 1]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Four-vertex cycle.
    adj: list[list[int]] = [[1, 3], [0, 2], [1, 3], [2, 0]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Star with unsorted neighbors.
    adj: list[list[int]] = [[4, 2, 1, 3], [0], [0], [0], [0]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Dense graph with multiple cycles.
    adj: list[list[int]] = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected forest.
    adj: list[list[int]] = [[1], [0], [3], [2, 4], [3], []]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated vertex 1 with a cycle elsewhere.
    adj: list[list[int]] = [[2, 3], [], [0, 3], [0, 2]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Initial isolated vertices followed by a cycle.
    adj: list[list[int]] = [[], [], [3, 4], [2, 4], [2, 3]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle in a later component after an acyclic component.
    adj: list[list[int]] = [[1], [0], [3, 4], [2, 4], [2, 3]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle at the beginning with trailing isolated vertices.
    adj: list[list[int]] = [[1, 2], [0, 2], [0, 1], [], []]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only one edge after isolated vertices.
    adj: list[list[int]] = [[], [], [3], [2]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with minimum edges.
    adj: list[list[int]] = [[1], [0]] + [[] for _ in range(9998)]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices: long acyclic path.
    adj: list[list[int]] = [
        ([i - 1] if i > 0 else []) + ([i + 1] if i < 9999 else []) for i in range(10000)
    ]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and edges: one large ring.
    adj: list[list[int]] = [[(i - 1) % 10000, (i + 1) % 10000] for i in range(10000)]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices: cycle only in the final three vertices.
    adj: list[list[int]] = [[] for _ in range(9997)] + [
        [9998, 9999],
        [9997, 9999],
        [9997, 9998],
    ]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tests for the iterative DFS implementation.
    adj: list[list[int]] = [
        [1, 3],
        [0, 2, 4],
        [1, 5],
        [0, 4],
        [1, 3, 5],
        [2, 4],
    ]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Example 2: acyclic tree.
    adj: list[list[int]] = [[1, 2], [0], [0, 3], [2]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: triangle with a tail.
    adj: list[list[int]] = [[1, 2], [0, 2], [0, 1, 3], [2]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum edge count: one edge is not a cycle.
    adj: list[list[int]] = [[1], [0]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Three-vertex path.
    adj: list[list[int]] = [[1], [0, 2], [1]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest simple cycle: a triangle.
    adj: list[list[int]] = [[1, 2], [0, 2], [0, 1]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Four-vertex cycle.
    adj: list[list[int]] = [[1, 3], [0, 2], [1, 3], [2, 0]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Star with unsorted neighbors.
    adj: list[list[int]] = [[4, 2, 1, 3], [0], [0], [0], [0]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Dense graph with multiple cycles.
    adj: list[list[int]] = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected forest.
    adj: list[list[int]] = [[1], [0], [3], [2, 4], [3], []]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated vertex 1 with a cycle elsewhere.
    adj: list[list[int]] = [[2, 3], [], [0, 3], [0, 2]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Initial isolated vertices followed by a cycle.
    adj: list[list[int]] = [[], [], [3, 4], [2, 4], [2, 3]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle in a later component after an acyclic component.
    adj: list[list[int]] = [[1], [0], [3, 4], [2, 4], [2, 3]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle at the beginning with trailing isolated vertices.
    adj: list[list[int]] = [[1, 2], [0, 2], [0, 1], [], []]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only one edge after isolated vertices.
    adj: list[list[int]] = [[], [], [3], [2]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with minimum edges.
    adj: list[list[int]] = [[1], [0]] + [[] for _ in range(9998)]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices: cycle only in the final three vertices.
    adj: list[list[int]] = [[] for _ in range(9997)] + [
        [9998, 9999],
        [9997, 9999],
        [9997, 9998],
    ]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # DFS: two branches meet at the same vertex.
    adj: list[list[int]] = [[1, 2], [0, 3], [0, 3], [1, 2]]
    expected: bool = True
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # DFS: branching tree with unsorted neighbors.
    adj: list[list[int]] = [[2, 1], [4, 0, 3], [6, 0, 5], [1], [1], [2], [2]]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # DFS: maximum-size star with many pending vertices.
    adj: list[list[int]] = [list(range(1, 10000))] + [[0] for _ in range(9999)]
    expected: bool = False
    result: bool = detect_cycle_undirected_graph_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
