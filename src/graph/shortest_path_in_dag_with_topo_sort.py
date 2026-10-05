"""955. Shortest Path in DAG

Given a Directed Acyclic Graph (DAG) with N vertices labeled from 0 to N - 1
and M weighted directed edges, find the shortest distance from a chosen
source vertex to every vertex.

The graph is provided as a list of edges. Each entry [u, v, weight] represents
a directed edge from u to v with the given distance. A path's distance is the
sum of its edge weights.

Return a list of N distances, where the value at index i is the shortest
distance from source to vertex i. Use -1 for an unreachable vertex. The
distance from source to itself is 0, even if source is isolated.

Pass N as vertices, derive M from len(edges), and pass source explicitly
to choose the starting vertex. The default source is 0.

Example 1:
    Input: N = 4, M = 2, source = 0, edges = [[0, 1, 2], [0, 2, 1]]
    Output: [0, 2, 1, -1]
    Explanation:
        - Vertex 1: path 0 -> 1 has distance 2.
        - Vertex 2: path 0 -> 2 has distance 1.
        - Vertex 3 cannot be reached from vertex 0, so its distance is -1.

Example 2:
    Input: N = 6, M = 7, source = 0, edges = [
        [0, 1, 2],
        [0, 4, 1],
        [4, 5, 4],
        [4, 2, 2],
        [1, 2, 3],
        [2, 3, 6],
        [5, 3, 1],
    ]
    Output: [0, 2, 3, 6, 1, 5]
    Explanation:
        - Vertex 1: 0 -> 1, distance 2.
        - Vertex 2: 0 -> 4 -> 2, distance 1 + 2 = 3.
        - Vertex 3: 0 -> 4 -> 5 -> 3, distance 1 + 4 + 1 = 6.
        - Vertex 4: 0 -> 4, distance 1.
        - Vertex 5: 0 -> 4 -> 5, distance 1 + 4 = 5.

Example 3 (nonzero source):
    Input: N = 6, M = 7, source = 4, edges = [
        [0, 1, 2], [0, 4, 1], [4, 5, 4], [4, 2, 2],
        [1, 2, 3], [2, 3, 6], [5, 3, 1],
    ]
    Output: [-1, -1, 2, 5, 0, 4]
    Explanation: From vertex 4, reach 2 with distance 2 and 5 with distance
    4. The shortest route to 3 is 4 -> 5 -> 3 with distance 5. Vertices 0
    and 1 are unreachable because edges can only be followed forward.

Practice example:
    Input: N = 3, M = 3, source = 0, edges = [[0, 1, 4], [0, 2, 2], [1, 2, 5]]
    Pick the correct output:
        A. [4, 4, 2]
        B. [0, 4, 4]
        C. [0, 2, 2]
        D. [0, 4, 2]

Constraints:
    - 1 <= N, M <= 5 * 10**4, as stated in the supplied question.
    - 0 <= source < N.
    - 0 <= edges[i][0], edges[i][1] < N.
    - 1 <= edges[i][2] < 10**4.
    - The graph is directed and acyclic.

    The supplied endpoint bound was < N - 1, which conflicts with the vertex
    labels and examples; the bound above includes vertex N - 1. Also, N = 1
    cannot have M >= 1 in a DAG, so the stated minimums are not jointly
    achievable for a valid input.

Follow-up questions:
    - What if the graph has negative weights?
    - What if there are multiple shortest paths to a vertex?
    - Can this be modified to find the longest path in a DAG?
    - How can multiple sources be handled instead of a single source?

https://www.youtube.com/watch?v=ZUFQfFaU-8U&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=27

"""


def shortest_path_in_dag_with_topo_sort(
    vertices: int, edges: list[list[int]], source: int = 0
) -> list[int]:
    """Return shortest distances from a chosen source in a weighted DAG.

    Args:
        vertices: Number of vertices V, labeled 0 through V - 1.
        edges: E entries [u, v, weight], each representing a directed edge
            u -> v. Assumes a DAG, valid vertex indices, 1 <= V, E <= 50000,
            and integer weights satisfying 1 <= weight < 10000.
        source: Starting vertex, with 0 <= source < vertices. Defaults to 0.

    Returns:
        A list indexed by vertex containing its shortest distance from source,
        or -1 if unreachable. The source distance is 0 even when isolated.
        Finite distances remain integers because the source starts at integer
        zero and all edge weights are integers. Infinity is only an internal
        sentinel and is replaced with -1. The input edges are not modified.

    Approach:
        Use DAG shortest paths via DFS-based topological sorting and edge
        relaxation. Relaxation replaces a distance when a shorter route is
        found; it does not record the path itself.
        1. Allocate weighted adjacency lists, visited flags, a DFS finishing
           stack, and distances initialized to infinity. Set the chosen
           source's distance to zero before performing relaxation.
        2. Build adjacency: store (v, weight) in adj[u] for each edge u -> v.
           Allocate one list per vertex so isolated vertices are represented.
        3. Run Depth-First Search (DFS) from every unvisited vertex. Mark each
           vertex on entry, explore its unvisited outgoing neighbors, then
           append it to the stack after those searches finish. For a DAG,
           every edge u -> v makes v finish before u. Searching all vertices
           includes disconnected components and vertices unreachable from
           the source.
        4. Pop from the end of the finishing stack to process vertices in
           topological order. No explicit reversal is needed because popping
           already reverses finishing order. For 0 -> 1 -> 2, DFS records
           [2, 1, 0], and popping processes 0, then 1, then 2.
        5. Skip a popped vertex if its distance is still infinity: there is
           no route from source to it. Otherwise, relax every outgoing edge
           using min(current neighbor distance, vertex distance + weight).
           Every predecessor is processed before its destination, so all
           possible incoming routes have been considered by the time a
           vertex is popped. Its distance is therefore final, and one pass
           suffices even when a cheaper route uses more edges.
        6. Return distances in vertex-index order, replacing remaining
           infinities with -1. Unreachable vertices may have edges within
           another component; they need not be isolated. Equal-cost routes
           leave the same distance, so no tie-breaking is required.

    Time Complexity:
        O(V + E). Initialization takes O(V), and building adjacency takes
        O(E). DFS visits each vertex once and scans every edge once. The
        relaxation pass pops V vertices and scans at most E edges. Converting
        the output takes O(V). Bounds assume recursive traversal completes.

    Space Complexity:
        O(V + E) auxiliary space. Adjacency stores V lists and E weighted
        edges. Visited flags, distances, and the finishing stack each use
        O(V). Recursive DFS can use O(V) call frames along a directed path.
        The returned list uses another O(V), leaving the total O(V + E).

    Limitations:
        Cycles are not detected; correctness requires the supplied DAG
        assumption. Recursive DFS can exceed Python's recursion limit on
        long paths, including permitted 50,000-vertex inputs, even in a
        component unreachable from source. Thus this implementation does
        not handle every allowed graph under the default recursion limit.
    """

    # 1. Initialize graph storage, DFS state, and unknown distances.
    adj: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]
    topo_sorted_stack: list[int] = []
    visited: list[bool] = [False] * vertices

    shortest_paths: list[int | float] = [float("inf")] * vertices

    # 2. Represent each outgoing edge as (destination, weight).
    def build_adjacency_list() -> None:
        for node1, node2, weight in edges:
            adj[node1].append((node2, weight))

    # 3. Record DFS finishing order across all components.
    def topo_sort_dfs() -> None:

        def dfs(vertex: int) -> None:
            visited[vertex] = True

            for neighbor, _ in adj[vertex]:
                if not visited[neighbor]:
                    dfs(vertex=neighbor)

            # Append only after all outgoing neighbors have finished.
            topo_sorted_stack.append(vertex)

        for vertex in range(vertices):
            if not visited[vertex]:
                dfs(vertex=vertex)

    # 1. The chosen source is reachable from itself with distance zero.
    shortest_paths[source] = 0

    def find_shortest_paths() -> None:

        # 4. Popping finishing order processes predecessors before destinations.
        while topo_sorted_stack:
            vertex: int = topo_sorted_stack.pop()
            distance: int | float = shortest_paths[vertex]
            # 5. Ignore unreachable vertices; relax edges from reachable ones.
            if distance == float("inf"):
                continue

            for neighbor, distance_to_neighbor in adj[vertex]:
                shortest_paths[neighbor] = min(
                    distance + distance_to_neighbor, shortest_paths[neighbor]
                )

    build_adjacency_list()
    topo_sort_dfs()
    find_shortest_paths()

    # 6. Convert unreachable distances to the required -1 output value.
    return [-1 if distance == float("inf") else distance for distance in shortest_paths]


def solve() -> None:
    vertices: int = 4
    source: int = 0
    edges: list[list[int]] = [[0, 1, 2], [0, 2, 1]]
    expected: list[int] = [0, 2, 1, -1]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest feasible DAG with one minimum-weight edge.
    vertices: int = 2
    source: int = 0
    edges: list[list[int]] = [[0, 1, 1]]
    expected: list[int] = [0, 1]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum allowed edge weight.
    vertices: int = 2
    source: int = 0
    edges: list[list[int]] = [[0, 1, 9999]]
    expected: list[int] = [0, 9999]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Source is the final vertex and a sink.
    vertices: int = 2
    source: int = 1
    edges: list[list[int]] = [[0, 1, 2]]
    expected: list[int] = [-1, 0]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Final vertex as source with an edge to zero.
    vertices: int = 2
    source: int = 1
    edges: list[list[int]] = [[1, 0, 3]]
    expected: list[int] = [3, 0]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated nonzero source.
    vertices: int = 4
    source: int = 2
    edges: list[list[int]] = [[0, 1, 2]]
    expected: list[int] = [-1, -1, 0, -1]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated zero source with edges elsewhere.
    vertices: int = 4
    source: int = 0
    edges: list[list[int]] = [[1, 2, 3], [2, 3, 4]]
    expected: list[int] = [0, -1, -1, -1]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Forward chain requires propagation across several edges.
    vertices: int = 4
    source: int = 0
    edges: list[list[int]] = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
    expected: list[int] = [0, 2, 5, 9]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reverse-labeled chain.
    vertices: int = 4
    source: int = 3
    edges: list[list[int]] = [[3, 2, 2], [2, 1, 3], [1, 0, 4]]
    expected: list[int] = [9, 5, 2, 0]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Middle source cannot reach its predecessors.
    vertices: int = 4
    source: int = 1
    edges: list[list[int]] = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
    expected: list[int] = [-1, 0, 3, 7]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Indirect route beats an expensive direct edge.
    vertices: int = 3
    source: int = 0
    edges: list[list[int]] = [[0, 2, 10], [0, 1, 2], [1, 2, 3]]
    expected: list[int] = [0, 2, 5]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Direct route beats the indirect route.
    vertices: int = 3
    source: int = 0
    edges: list[list[int]] = [[0, 1, 4], [0, 2, 2], [1, 2, 5]]
    expected: list[int] = [0, 4, 2]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two routes tie for the shortest distance.
    vertices: int = 4
    source: int = 0
    edges: list[list[int]] = [[0, 1, 2], [0, 2, 3], [1, 3, 4], [2, 3, 3]]
    expected: list[int] = [0, 2, 3, 6]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reachable and unreachable predecessors share a destination.
    vertices: int = 4
    source: int = 0
    edges: list[list[int]] = [[0, 2, 7], [1, 2, 1], [2, 3, 2]]
    expected: list[int] = [0, -1, 7, 9]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Nonconsecutive labels and shuffled edge order.
    vertices: int = 5
    source: int = 2
    edges: list[list[int]] = [[1, 4, 2], [3, 1, 5], [2, 0, 4], [0, 3, 1]]
    expected: list[int] = [4, 10, 0, 5, 12]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Question Example 2.
    vertices: int = 6
    source: int = 0
    edges: list[list[int]] = [
        [0, 1, 2],
        [0, 4, 1],
        [4, 5, 4],
        [4, 2, 2],
        [1, 2, 3],
        [2, 3, 6],
        [5, 3, 1],
    ]
    expected: list[int] = [0, 2, 3, 6, 1, 5]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Same graph with source four.
    vertices: int = 6
    source: int = 4
    edges: list[list[int]] = [
        [0, 1, 2],
        [0, 4, 1],
        [4, 5, 4],
        [4, 2, 2],
        [1, 2, 3],
        [2, 3, 6],
        [5, 3, 1],
    ]
    expected: list[int] = [-1, -1, 2, 5, 0, 4]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Path total can exceed the maximum individual weight.
    vertices: int = 3
    source: int = 0
    edges: list[list[int]] = [[0, 1, 9999], [1, 2, 9999]]
    expected: list[int] = [0, 9999, 19998]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with one edge to the final index.
    vertices: int = 50000
    source: int = 0
    edges: list[list[int]] = [[0, 49999, 1]]
    expected: list[int] = [0] + [-1] * 49998 + [1]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with the final index as source.
    vertices: int = 50000
    source: int = 49999
    edges: list[list[int]] = [[49999, 0, 9999]]
    expected: list[int] = [9999] + [-1] * 49998 + [0]
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and edges in a shallow two-layer DAG.
    vertices: int = 50000
    source: int = 0
    edges: list[list[int]] = [[u, v, 1] for u in range(250) for v in range(250, 450)]
    expected: list[int] = [0] + [-1] * 249 + [1] * 200 + [-1] * 49550
    result: list[int] = shortest_path_in_dag_with_topo_sort(
        vertices, edges, source=source
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
