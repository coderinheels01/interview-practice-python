"""961. Shortest Path in Undirected Graph with Unit Weights

Given an undirected graph with N vertices labeled from 0 to N - 1 and M
edges, find the shortest distance from a chosen source vertex to every vertex.

Each entry [u, v] in edges represents an undirected edge of weight 1.
It can be traversed from u to v or from v to u. A path's distance is the
number of edges it contains.

Return a list of N distances in vertex-index order. The distance to source
vertex is 0. Return -1 for any vertex that is unreachable from the source.
Return distances, not the sequences of vertices along the paths.

Pass N as vertices and derive M from len(edges). Pass source to select the
starting vertex; it defaults to 0. The examples below use source = 0.

Example 1:
    Input: N = 9, M = 10, edges = [
        [0, 1], [0, 3], [3, 4], [4, 5], [5, 6],
        [1, 2], [2, 6], [6, 7], [7, 8], [6, 8],
    ]
    Output: [0, 1, 2, 1, 2, 3, 3, 4, 4]
    Explanation: Each entry gives the shortest distance from vertex 0.
    Vertices 1 and 3 are one edge away. Vertices 2 and 4 are two edges away.
    Vertices 5 and 6 are three edges away, and vertices 7 and 8 are four
    edges away. All vertices are reachable in this example.

Example 2:
    Input: N = 8, M = 10, edges = [
        [1, 0], [2, 1], [0, 3], [3, 7], [3, 4],
        [7, 4], [7, 6], [4, 5], [4, 6], [6, 5],
    ]
    Output: [0, 1, 2, 1, 2, 3, 3, 2]
    Explanation: Vertices 1 and 3 are one edge from vertex 0. Vertices 2,
    4, and 7 are two edges away. Vertices 5 and 6 are three edges away.

Practice example:
    Input: N = 3, M = 1, edges = [[1, 2]]
    Pick the correct output:
        A. [0, -1, -1]
        B. [-1, -1, -1]
        C. [0, 1, 1]
        D. [0, 0, 0]

Constraints:
    - 1 <= N, M <= 10**4.
    - 0 <= source < N.
    - 0 <= edges[i][j] <= N - 1.
    - Each edge has exactly two endpoints and weight 1.

Follow-up questions:
    - Can this approach handle graphs with negative weights?
    - How does this compare to Dijkstra's algorithm?
    - What if the longest path were needed instead?
    - Why is BFS used for shortest paths in unweighted graphs, and how would
      the solution change if edge weights were not unit weights?

https://www.youtube.com/watch?v=C4gxoTaI71U&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=28

"""

from collections import deque


def shortest_path_undirected_unit_weights(
    vertices: int, edges: list[list[int]], source: int = 0
) -> list[int]:
    """Return shortest unit-weight distances from a chosen source.

    Args:
        vertices: Number of vertices V, labeled 0 through V - 1.
        edges: E pairs [u, v], each representing an undirected edge with
            weight 1. Assumes valid indices and 1 <= V, E <= 10**4.
        source: Starting vertex, with 0 <= source < vertices. Defaults to 0.

    Returns:
        A list of integer distances in vertex-index order. The source has
        distance 0; vertices unreachable from it have distance -1. Distances
        count edges, not the vertices along a path. The input edges are not
        modified. Disconnected graphs, self-loops, and repeated edges are
        handled; an isolated source has distance 0 while all others stay -1.

    Approach:
        Use Breadth-First Search (BFS) with a FIFO queue.
        1. Allocate one adjacency list per vertex and initialize all distances
           to -1. This value means undiscovered during traversal and becomes
           the required unreachable marker for vertices never reached.
        2. For every edge [u, v], add v to adj[u] and u to adj[v]. Both
           directions are necessary because the input graph is undirected.
        3. Set the chosen source's distance to 0 and enqueue it. This marks
           the source discovered before any neighbor can enqueue it again.
        4. Remove the oldest vertex with popleft() and read its recorded
           distance. FIFO processing explores vertices in increasing distance
           layers: first distance 0, then distance 1, then distance 2, etc.
        5. For each neighbor whose distance is still -1, record the current
           distance plus 1 and enqueue it. Set the distance before enqueueing
           so another incoming route cannot queue the same vertex again.
           The first discovery is shortest: any shorter route would come
           through an earlier distance layer and would have discovered that
           neighbor already. Therefore no later distance comparison or update
           is needed. This property relies on every edge having weight 1.
           Already discovered neighbors are skipped, including reverse edges,
           self-loops, and repeated connections.
        6. Continue until the queue empties, then return distances directly.
           Every source-reachable vertex has its shortest distance; vertices
           in other components remain -1. No sorting or conversion is needed.

        Example: for edges = [[0, 1], [1, 2]] and source = 0, begin with
        distances = [0, -1, -1]. Processing 0 discovers 1 and gives [0, 1, -1].
        Processing 1 skips already discovered 0 and discovers 2, giving
        [0, 1, 2]. Processing 2 skips 1, and the queue becomes empty.

    Time Complexity:
        O(V + E). Initializing adjacency and distances takes O(V), and
        building both directions of E edges takes O(E). Each reachable
        vertex is enqueued and dequeued once. Its neighbor list is scanned
        once, with at most 2E adjacency entries examined overall. Deque
        append and popleft take O(1); distance checks and updates take O(1).

    Space Complexity:
        O(V + E) auxiliary space. Adjacency contains V lists and 2E neighbor
        entries, while distances and the queue each use O(V) space. The
        distance list is returned directly without copying. No separate
        visited array or recursive call stack is needed.
    """
    # 1. Initialize adjacency and mark every vertex undiscovered with -1.
    adj: list[list[int]] = [[] for _ in range(vertices)]
    distances: list[int] = [-1] * vertices

    # 2. Store both directions of each undirected edge.
    for node1, node2 in edges:
        adj[node1].append(node2)
        adj[node2].append(node1)

    # 3. Discover the selected source at distance zero and start the queue.
    distances[source] = 0
    queue: deque[int] = deque([source])

    # 4. Process vertices in FIFO order, from nearer layers to farther ones.
    while queue:
        vertex = queue.popleft()
        distance = distances[vertex]
        for neighbor in adj[vertex]:
            # 5. First discovery gives the shortest distance; mark before enqueueing.
            if distances[neighbor] == -1:
                distances[neighbor] = distance + 1
                queue.append(neighbor)

    # 6. Unreached vertices retain -1; all other distances are finalized.
    return distances


def solve() -> None:
    vertices: int = 9
    source: int = 0
    edges: list[list[int]] = [
        [0, 1],
        [0, 3],
        [3, 4],
        [4, 5],
        [5, 6],
        [1, 2],
        [2, 6],
        [6, 7],
        [7, 8],
        [6, 8],
    ]
    expected: list[int] = [0, 1, 2, 1, 2, 3, 3, 4, 4]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single vertex with a self-loop.
    vertices: int = 1
    source: int = 0
    edges: list[list[int]] = [[0, 0]]
    expected: list[int] = [0]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single edge from zero.
    vertices: int = 2
    source: int = 0
    edges: list[list[int]] = [[0, 1]]
    expected: list[int] = [0, 1]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reverse-listed edge must be traversable.
    vertices: int = 2
    source: int = 0
    edges: list[list[int]] = [[1, 0]]
    expected: list[int] = [0, 1]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Source at the final vertex.
    vertices: int = 2
    source: int = 1
    edges: list[list[int]] = [[0, 1]]
    expected: list[int] = [1, 0]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated source from the practice example.
    vertices: int = 3
    source: int = 0
    edges: list[list[int]] = [[1, 2]]
    expected: list[int] = [0, -1, -1]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated nonzero source.
    vertices: int = 4
    source: int = 2
    edges: list[list[int]] = [[0, 1]]
    expected: list[int] = [-1, -1, 0, -1]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unreachable component contains edges.
    vertices: int = 5
    source: int = 0
    edges: list[list[int]] = [[0, 1], [2, 3], [3, 4]]
    expected: list[int] = [0, 1, -1, -1, -1]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Forward chain.
    vertices: int = 5
    source: int = 0
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 3], [3, 4]]
    expected: list[int] = [0, 1, 2, 3, 4]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Chain from its middle vertex.
    vertices: int = 5
    source: int = 2
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 3], [3, 4]]
    expected: list[int] = [2, 1, 0, 1, 2]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed endpoint orientation in a chain.
    vertices: int = 4
    source: int = 0
    edges: list[list[int]] = [[1, 0], [1, 2], [3, 2]]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Triangle cycle.
    vertices: int = 3
    source: int = 0
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 0]]
    expected: list[int] = [0, 1, 1]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diamond with equal-length routes.
    vertices: int = 4
    source: int = 0
    edges: list[list[int]] = [[0, 1], [0, 2], [1, 3], [2, 3]]
    expected: list[int] = [0, 1, 1, 2]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Shortcut beats the longer route.
    vertices: int = 5
    source: int = 0
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 4]]
    expected: list[int] = [0, 1, 2, 2, 1]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Star from a leaf.
    vertices: int = 5
    source: int = 3
    edges: list[list[int]] = [[0, 1], [0, 2], [0, 3], [0, 4]]
    expected: list[int] = [1, 2, 2, 0, 2]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated edges do not change distances.
    vertices: int = 3
    source: int = 0
    edges: list[list[int]] = [[0, 1], [0, 1], [1, 0], [1, 2]]
    expected: list[int] = [0, 1, 2]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Self-loops do not shorten paths.
    vertices: int = 3
    source: int = 0
    edges: list[list[int]] = [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2]]
    expected: list[int] = [0, 1, 2]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reachable vertices at both index boundaries.
    vertices: int = 5
    source: int = 4
    edges: list[list[int]] = [[4, 0], [0, 2]]
    expected: list[int] = [1, -1, 2, -1, 0]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example.
    vertices: int = 8
    source: int = 0
    edges: list[list[int]] = [
        [1, 0],
        [2, 1],
        [0, 3],
        [3, 7],
        [3, 4],
        [7, 4],
        [7, 6],
        [4, 5],
        [4, 6],
        [6, 5],
    ]
    expected: list[int] = [0, 1, 2, 1, 2, 3, 3, 2]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and minimum edges.
    vertices: int = 10000
    source: int = 0
    edges: list[list[int]] = [[0, 9999]]
    expected: list[int] = [0] + [-1] * 9998 + [1]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices in a chain.
    vertices: int = 10000
    source: int = 0
    edges: list[list[int]] = [[i, i + 1] for i in range(9999)]
    expected: list[int] = list(range(10000))
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices in a star.
    vertices: int = 10000
    source: int = 0
    edges: list[list[int]] = [[0, i] for i in range(1, 10000)]
    expected: list[int] = [0] + [1] * 9999
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and edges in a ring.
    vertices: int = 10000
    source: int = 0
    edges: list[list[int]] = [[i, i + 1] for i in range(9999)] + [[9999, 0]]
    expected: list[int] = [min(i, 10000 - i) for i in range(10000)]
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum edges in a complete bipartite component.
    vertices: int = 10000
    source: int = 0
    edges: list[list[int]] = [[u, v] for u in range(100) for v in range(100, 200)]
    expected: list[int] = [0] + [2] * 99 + [1] * 100 + [-1] * 9800
    result: list[int] = shortest_path_undirected_unit_weights(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
