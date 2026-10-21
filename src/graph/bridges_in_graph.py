"""143. Bridges in Graph

Given an undirected connected graph with V vertices numbered from 0 to V - 1
and a list of edges, return all bridges in any order.

Each edge [ai, bi] connects vertex ai to vertex bi. An edge is a bridge if
removing it makes some vertex unable to reach another vertex; that is, its
removal disconnects the graph.

Example 1:
    Input: V = 4, edges = [[0, 1], [1, 2], [2, 0], [1, 3]]
    Output: [[1, 3]]
    Explanation: Removing [1, 3] separates vertex 3 from the other vertices,
    dividing the graph into two connected components.

Example 2:
    Input: V = 3, edges = [[0, 1], [1, 2], [2, 0]]
    Output: []
    Explanation: Removing any one edge leaves all vertices connected, so
    there are no bridges.

Practice question:
    Input: V = 2, edges = [[0, 1]]
    Choices: [[0, 1]], []

Constraints:
    - 2 <= V <= 10^4
    - The stated edge-count constraint is 2 <= E <= 10^4, where E is the
      number of edges. The supplied practice question also includes E = 1.
    - 0 <= ai, bi <= V - 1
    - The graph is undirected and connected.

https://www.youtube.com/watch?v=Rhxs4k6DyMM

https://www.youtube.com/watch?v=ZeDNSeilf-Y

"""


def bridges_in_graph(vertices: int, edges: list[list[int]]) -> list[list[int]]:
    """Return every bridge in an undirected graph without parallel edges.

    Args:
        vertices: Number V of vertices, identified by integers 0 through V - 1.
        edges: E undirected edges [u, v]. Endpoints must be valid vertex IDs.
            The problem specifies a connected graph; the outer DFS loop also
            handles disconnected graphs. Parallel edges are not supported.

    Returns:
        Bridge endpoint pairs in DFS traversal order. Each bridge appears once;
        endpoint orientation may differ from the input. A graph with no bridges
        returns []. In a tree, every edge is a bridge. Neither input is modified.

    Approach:
        Tarjan's Bridge-Finding Algorithm using DFS discovery times and low-link
        values. This is the undirected bridge algorithm, not Tarjan's SCC routine.

        1. Initialize discovery, parents, and low arrays. A discovery value of
           -1 means unvisited. Build an adjacency list with BOTH directions for
           each undirected edge. Keep a shared discovery counter starting at -1.
        2. Start DFS from every unvisited vertex. On entry, increment the shared
           counter and assign discovery[node] = low[node] = counter. nonlocal
           lets recursive calls update the same enclosing counter. Discovery
           records entry time, not vertex ID; low starts at that entry time.
        3. For each neighbor, skip the parent vertex: traversing the same tree
           edge backward does not demonstrate an alternative connection.
           If a non-parent neighbor is already discovered, update low[node]
           with discovery[neighbor]. This accounts for a back edge to an
           ancestor. An already discovered descendant has a later discovery
           time and cannot lower low[node]. Do not recurse into visited nodes.
        4. For an unvisited neighbor, record its parent BEFORE recursing. After
           its DFS finishes, propagate low[neighbor] into low[node] using min.
           A parent can travel down to its child and use the earlier connection
           found by that child's subtree. Taking min preserves the earliest
           connection found through any child or back edge.
        5. After that child's DFS, report [node, neighbor] exactly when
           low[neighbor] > discovery[node]. The child's subtree has no back
           connection to node or any ancestor of node, so removing this tree
           edge disconnects it. Equality is NOT enough: equality means there
           is an alternative connection back to node, so the edge is not a
           bridge. Only test DFS tree edges, not already-visited neighbors.
        6. Return all recorded bridges after the outer DFS loop finishes.

        Meaning of low:
            low[u] is the minimum discovery time reachable from u by following
            zero or more downward DFS tree edges and then at most one back
            edge. It summarizes an earlier connection found by u's subtree;
            it is not simply the smallest vertex ID anywhere reachable.

        Visual example:
            edges = [[0, 1], [1, 2], [2, 0], [1, 3]]

                 0
                / \
               2---1---3

            DFS tree: 0 -> 1 -> 2, then 1 -> 3.
            Extra connection: 2 -> 0.

            Vertex:       0  1  2  3
            Discovery:    0  1  2  3
            Final low:    0  0  0  3

        Vertex 2 sees the back edge to 0, so low[2] becomes discovery[0] = 0.
        Vertex 1 inherits that value because it can use the path 1 -> 2 -> 0.
        This route still exists if its own parent edge 0--1 is removed.
        Thus low[1] = min(1, low[2]) = 0. Vertex 3 has only its parent edge,
        which is skipped, so low[3] stays 3.

            Edge 1--2: low[2] = 0 <= discovery[1] = 1 -> not a bridge.
            Edge 0--1: low[1] = 0 == discovery[0] = 0 -> not a bridge.
            Edge 1--3: low[3] = 3 >  discovery[1] = 1 -> bridge.

        The result is [[1, 3]]. The 2--0 back edge is not a candidate tree
        edge; it participates in the cycle and is not reported as a bridge.

    Time Complexity:
        O(V + E), where V is the number of vertices and E is the number of
        undirected input edges. For the example, V = 4 and E = 4.

        1. Initialize three length-V arrays and V empty neighbor lists -> O(V).
        2. Build adjacency lists: each input edge adds two neighbor entries,
           so there are 2E total entries -> O(E).
        3. The outer loop checks V vertices. Each vertex enters DFS once and
           scans its own neighbor list once. Across all calls, those lists
           contain 2E entries, not E entries for every vertex -> O(V + E).
           Each low update and bridge check is constant work. Recording at
           most V - 1 bridges in the connected graph adds at most O(V) work.

        The example stores 8 neighbor entries, all examined once by DFS.
        Recursive calls do not repeat a full graph search: discovery prevents
        revisiting vertices. Sequential phases add:
            O(V) + O(E) + O(V + E) = O(V + E).

    Space Complexity:
        O(V + E) additional space, excluding the input edges list and including
        the returned bridges list. Excluding the output gives the same bound.

        - adjacency_list: V inner lists containing 2E neighbor entries ->
          O(V + E). The example has 4 lists and 8 neighbor entries, not a
          V x V matrix.
        - discovery, parents, low: V integers each -> O(V) per array.
          For V = 4, these arrays contain 4 + 4 + 4 = 12 entries altogether.
        - Recursive DFS stack: at most V nested calls on a long path -> O(V).
          All calls share the arrays; they do not each copy them. Calls that
          have returned no longer occupy stack space.
        - bridges: at most V - 1 endpoint pairs in a connected graph -> O(V).
          Each pair has two entries, a constant-size contribution per bridge.
        - Counter and other local values: constant space per call, already
          accounted for in the recursion stack.

        Add peak live storage and retain dominant terms:
            O((V + E) + V + V + V + V + V) = O(V + E).
        Space measures memory held at once, not all allocations over time.

    Limitations:
        This implementation skips a parent vertex rather than a particular
        edge ID. It assumes no parallel edges; supporting them requires skipping
        only the incoming edge so other edges to the parent remain available.
        Recursive DFS may exceed Python's recursion limit on deep graphs allowed
        by V <= 10000. Shallow maximum-size tests do not cover this limitation.
        The function does not change the recursion limit.

    Interview Summary:
        I record discovery times and the earliest ancestor connection available
        from each DFS subtree. A tree edge to a child is a bridge exactly when
        the child's low value exceeds the parent's discovery time. Time and
        additional space are O(V + E), with the recursion and parallel-edge
        limitations described above.
    """
    # Step 1: Allocate discovery state and build both directions of every edge.
    discovery: list[int] = [-1] * vertices
    parents: list[int] = [-1] * vertices
    low: list[int] = [-1] * vertices
    bridges: list[list[int]] = []

    adjacency_list: list[list[int]] = [[] for _ in range(vertices)]

    for node1, node2 in edges:
        adjacency_list[node1].append(node2)
        adjacency_list[node2].append(node1)

    current_node_discovery_time = -1

    def dfs(node: int) -> None:
        # Step 2: Mark entry using the counter shared by all recursive calls.
        nonlocal current_node_discovery_time
        current_node_discovery_time += 1
        discovery[node] = current_node_discovery_time
        low[node] = discovery[node]

        for neighbor in adjacency_list[node]:
            # Step 3: Skip the incoming tree edge; visited neighbors update low.
            if parents[node] == neighbor:
                continue
            if discovery[neighbor] != -1:
                low[node] = min(low[node], discovery[neighbor])
            else:
                # Step 4: Explore the child, then inherit its earliest connection.
                parents[neighbor] = node
                dfs(node=neighbor)
                low[node] = min(low[neighbor], low[node])
                # Step 5: No alternative route to this node or its ancestors.
                if low[neighbor] > discovery[node]:
                    bridges.append([node, neighbor])

    # Step 2: Cover every component, starting DFS only at unvisited vertices.
    for vertex in range(vertices):
        if discovery[vertex] == -1:
            dfs(node=vertex)

    # Step 6: Return each detected bridge once.
    return bridges


def solve() -> None:
    vertices: int = 4
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 0], [1, 3]]
    expected: list[list[int]] = [[1, 3]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: a single edge is a bridge.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1]]
    expected: list[list[int]] = [[0, 1]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second example: a triangle has no bridges.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 0]]
    expected: list[list[int]] = []
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-edge path: every edge is a bridge.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1], [1, 2]]
    expected: list[list[int]] = [[0, 1], [1, 2]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A branching tree: every edge is a bridge.
    vertices: int = 7
    edges: list[list[int]] = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]]
    expected: list[list[int]] = [edge[:] for edge in edges]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Four-vertex cycle has no bridges.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 3], [3, 0]]
    expected: list[list[int]] = []
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Complete four-vertex graph has no bridges.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    expected: list[list[int]] = []
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two cycles sharing a vertex have no bridges.
    vertices: int = 5
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 2]]
    expected: list[list[int]] = []
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two triangles joined by one bridge.
    vertices: int = 6
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 3]]
    expected: list[list[int]] = [[2, 3]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two triangles joined by two separate connections.
    vertices: int = 6
    edges: list[list[int]] = [
        [0, 1],
        [1, 2],
        [2, 0],
        [3, 4],
        [4, 5],
        [5, 3],
        [1, 4],
        [2, 3],
    ]
    expected: list[list[int]] = []
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A cycle with a two-edge tail.
    vertices: int = 5
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4]]
    expected: list[list[int]] = [[2, 3], [3, 4]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # DFS starts at a leaf leading into a cycle.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 3], [3, 1]]
    expected: list[list[int]] = [[0, 1]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Leaves attached to different cycle vertices.
    vertices: int = 6
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 0], [0, 3], [1, 4], [2, 5]]
    expected: list[list[int]] = [[0, 3], [1, 4], [2, 5]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Bridge appears first in the input.
    vertices: int = 4
    edges: list[list[int]] = [[1, 3], [0, 1], [1, 2], [2, 0]]
    expected: list[list[int]] = [[1, 3]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Bridge appears in the middle with reversed endpoint orientation.
    vertices: int = 4
    edges: list[list[int]] = [[2, 0], [3, 1], [2, 1], [1, 0]]
    expected: list[list[int]] = [[1, 3]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Bridge appears last in the input.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 0], [1, 3]]
    expected: list[list[int]] = [[1, 3]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Longer return path prevents bridges throughout the cycle.
    vertices: int = 6
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 1], [3, 5]]
    expected: list[list[int]] = [[0, 1], [3, 5]]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices: shallow star, all edges are bridges.
    vertices: int = 10000
    edges: list[list[int]] = [[0, vertex] for vertex in range(1, vertices)]
    expected: list[list[int]] = [edge[:] for edge in edges]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and edges: star plus an edge forming one triangle.
    vertices: int = 10000
    edges: list[list[int]] = [[0, vertex] for vertex in range(1, vertices)] + [[1, 2]]
    expected: list[list[int]] = [[0, vertex] for vertex in range(3, vertices)]
    result: list[list[int]] = bridges_in_graph(vertices, edges)
    assert sorted(tuple(sorted(edge)) for edge in result) == sorted(
        tuple(sorted(edge)) for edge in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
