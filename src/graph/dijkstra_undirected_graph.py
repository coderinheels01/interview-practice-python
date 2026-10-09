"""109. Dijkstra's Algorithm — Undirected Graph

Given a weighted, undirected graph with vertices numbered from 0 to V - 1,
find the shortest distance from source S to every vertex.

The graph is represented by edges, where each entry [u, v, weight] describes
an undirected edge between vertices u and v with the given weight. An edge
can be traversed in either direction.

Return a list of V integers, where the value at index i is the shortest
distance from S to vertex i. The distance from S to itself is 0. If a vertex
is unreachable, use 10**9 (1,000,000,000) for its distance.

Example 1:
    Input: V = 2, edges = [[0, 1, 9]], S = 0
    Output: [0, 9]
    Explanation:
        The distance from node 0 to itself is 0.
        The shortest distance from node 0 to node 1 is 9.

Example 2:
    Input: V = 3, edges = [[0, 1, 1], [0, 2, 6], [1, 2, 3]], S = 2
    Output: [4, 3, 0]
    Explanation:
        The shortest path to node 0 is 2 -> 1 -> 0, with distance 3 + 1 = 4.
        The shortest path to node 1 is 2 -> 1, with distance 3.
        The distance to node 2 itself is 0.

Now Your Turn:
    Input: V = 4,
           edges = [[0, 1, 1], [0, 3, 2], [1, 2, 4], [2, 3, 3]], S = 0
    Pick the correct output:
        A. [1, 5, 2, 0]
        B. [0, 5, 1, 2]
        C. [0, 1, 5, 2]
        D. [0, 1, 1, 5]

Constraints:
    - 1 <= V <= 10,000.
    - Vertex endpoints satisfy 0 <= u, v < V.
    - Edge weights satisfy 0 <= weight <= 10,000.
    - 1 <= len(edges) <= V * (V - 1) / 2.
    - 0 <= S < V.
    - The stated edge-count bounds cannot be satisfied when V = 1.

Discussion Questions:
    - Why does Dijkstra's algorithm not work with negative weights?
    - Why do we use a priority queue in Dijkstra's algorithm?
    - How would you return the actual shortest paths instead of distances?
    - What if the graph had negative-weight edges?
"""

import heapq
from collections import defaultdict


def dijkstra_undirected_graph(
    vertices: int, edges: list[list[int]], source: int
) -> list[int]:
    """Return shortest distances from source in a weighted undirected graph.

    Args:
        vertices: Number of vertices, labeled 0 through vertices - 1.
        edges: Entries [u, v, weight], each traversable in both directions.
            Weights must be nonnegative and endpoints must be valid vertices.
        source: Starting vertex, with 0 <= source < vertices.

    Returns:
        A list indexed by vertex, containing its shortest distance from source.
        The source has distance 0; unreachable vertices have distance 10**9.
        The input edges are not modified.

    Approach:
        Dijkstra's Algorithm with an adjacency list and a min heap.

        1. Initialize distances to the unreachable sentinel, except source,
           whose distance is zero. Start the heap with (0, source). Distance
           comes first in each tuple so the heap prioritizes the shortest
           available route, breaking equal-distance ties by vertex number.
        2. Use the nested build_adjacency_list helper to build the graph.
           Store each edge twice: u -> v and v -> u, with the same weight.
           The helper fills the enclosing function's local adjacency map.
        3. Pop the smallest available distance. With nonnegative edge weights,
           a current, non-stale entry gives the vertex's final shortest
           distance: extending another route cannot produce a cheaper one.
        4. Skip entries whose distance exceeds the recorded best distance.
           An improved route creates a new heap entry without removing the
           old one, so stale entries must not expand outgoing edges again.
        5. For each neighbor, add its edge weight to the current distance.
           If this candidate is strictly smaller than the recorded distance,
           push the improved route and update distances. This is relaxation.
           Strict comparison avoids repeatedly enqueueing equal-cost routes,
           including routes around zero-weight cycles.
        6. Once the heap is empty, return distances. Unreachable vertices
           were never improved, so they retain the sentinel.

        Example: edges [[0, 1, 1], [0, 2, 6], [1, 2, 3]], source 2.
        Processing 2 discovers distance 6 to 0 and distance 3 to 1.
        Processing 1 improves the distance to 0 to 3 + 1 = 4.
        The heap processes (4, 0) before discarding stale entry (6, 0).
        The result is [4, 3, 0].

        The finite sentinel is safe under the stated constraints: a shortest
        path can be chosen without repeated vertices, so its distance is at
        most (10,000 - 1) * 10,000 = 99,990,000, below 10**9. Larger weights
        outside these constraints would require revisiting this assumption.
        Negative weights are not supported by Dijkstra's algorithm.

    Time Complexity:
        Let V be vertices and E be the number of undirected input edges.
        Initializing distances costs O(V); building adjacency costs O(E).
        Each reachable vertex's adjacency is scanned once from its current
        heap entry. There are 2E stored edge directions, so these scans total
        O(E), with at most O(E) successful relaxations and heap pushes/pops.
        The heap may retain multiple entries for a vertex and grow to O(E).
        Each push/pop costs O(log(E + 1)), giving O(V + E log(E + 1)) expected
        time overall, assuming average constant-time dictionary operations.
        The +1 handles a single-edge graph. For a simple graph, E = O(V^2),
        so the familiar O((V + E) log V) bound also applies for V >= 2.

    Space Complexity:
        O(V + E). Distances holds V values, adjacency stores 2E neighbor
        entries and at most V keys, and the heap holds O(E) entries, including
        stale ones. The helper builds the existing map without making a copy.
        No recursive traversal or full-path storage is used.

    https://www.youtube.com/watch?v=rp1SMw7HSO8&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=37
    """

    # 1. Initialize the source, unreachable distances, and min heap.
    heap: list[tuple[int, int]] = [(0, source)]
    unreachable: int = 10**9
    distances: list[int] = [unreachable] * vertices
    adj: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    distances[source] = 0

    # 2. Keep graph construction in a helper; store both edge directions.
    def build_adjacency_list() -> None:
        for node1, node2, distance in edges:
            adj[node1].append((node2, distance))
            adj[node2].append((node1, distance))

    build_adjacency_list()

    # 3. Always process the smallest available distance first.
    while heap:
        distance, vertex = heapq.heappop(heap)

        # 4. Ignore an outdated route after a shorter one was discovered.
        if distance > distances[vertex]:
            continue

        # 5. Relax each outgoing edge and enqueue only strict improvements.
        for neighbor, weight in adj[vertex]:
            new_distance = distance + weight
            if distances[neighbor] > new_distance:
                heapq.heappush(heap, (new_distance, neighbor))
                distances[neighbor] = new_distance

    # 6. Unreachable vertices retain the required sentinel.
    return distances


def solve() -> None:
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 1], [0, 2, 6], [1, 2, 3]]
    source: int = 2
    expected: list[int] = [4, 3, 0]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest feasible graph: one edge.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, 9]]
    source: int = 0
    expected: list[int] = [0, 9]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Traverse an edge in reverse from the highest source.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, 9]]
    source: int = 1
    expected: list[int] = [9, 0]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero-weight edge.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, 0]]
    source: int = 0
    expected: list[int] = [0, 0]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum edge weight.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, 10000]]
    source: int = 1
    expected: list[int] = [10000, 0]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal shortest paths around a cycle.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1, 1], [0, 3, 2], [1, 2, 4], [2, 3, 3]]
    source: int = 0
    expected: list[int] = [0, 1, 5, 2]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Shorter indirect route creates stale heap entries.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1, 9], [0, 2, 1], [2, 1, 1], [1, 3, 1], [2, 3, 8]]
    source: int = 0
    expected: list[int] = [0, 2, 1, 3]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Middle source with reversed edge endpoints.
    vertices: int = 5
    edges: list[list[int]] = [[1, 0, 2], [2, 1, 3], [3, 2, 4], [4, 3, 5]]
    source: int = 2
    expected: list[int] = [5, 3, 0, 4, 9]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero-weight cycle and a positive exit.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1, 0], [1, 2, 0], [2, 0, 0], [2, 3, 7]]
    source: int = 1
    expected: list[int] = [0, 0, 0, 7]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Direct path beats a longer detour.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 2], [0, 2, 4], [2, 1, 5]]
    source: int = 0
    expected: list[int] = [0, 2, 4]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All vertices connected with equal weights.
    vertices: int = 4
    edges: list[list[int]] = [
        [0, 1, 3],
        [0, 2, 3],
        [0, 3, 3],
        [1, 2, 3],
        [1, 3, 3],
        [2, 3, 3],
    ]
    source: int = 2
    expected: list[int] = [3, 3, 0, 3]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Path distance exceeds maximum individual edge weight.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1, 10000], [1, 2, 10000], [2, 3, 10000]]
    source: int = 0
    expected: list[int] = [0, 10000, 20000, 30000]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Complete graph reaches the edge-count maximum for 100 vertices.
    vertices: int = 100
    edges: list[list[int]] = [
        [u, v, 1] for u in range(vertices) for v in range(u + 1, vertices)
    ]
    source: int = 50
    expected: list[int] = [1] * vertices
    expected[source] = 0
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertex count, highest source, and maximum weights on a chain.
    vertices: int = 10000
    edges: list[list[int]] = [[i, i + 1, 10000] for i in range(vertices - 1)]
    source: int = vertices - 1
    expected: list[int] = [(vertices - 1 - i) * 10000 for i in range(vertices)]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unreachable vertex must use the problem's sentinel.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 4]]
    source: int = 0
    expected: list[int] = [0, 4, 10**9]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated source with an edge elsewhere in the graph.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 4]]
    source: int = 2
    expected: list[int] = [10**9, 10**9, 0]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Separate components, including a zero-weight unreachable component.
    vertices: int = 6
    edges: list[list[int]] = [[0, 1, 2], [1, 2, 3], [3, 4, 0]]
    source: int = 1
    expected: list[int] = [2, 0, 3, 10**9, 10**9, 10**9]
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with minimum edge count.
    vertices: int = 10000
    edges: list[list[int]] = [[0, 9999, 10000]]
    source: int = 9999
    expected: list[int] = [10**9] * vertices
    expected[0] = 10000
    expected[source] = 0
    result: list[int] = dijkstra_undirected_graph(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
