"""212. Kosaraju's Algorithm

You are given a directed graph with V vertices, numbered from 0 to V - 1,
and its adjacency list Adj. Adj[i] contains every vertex j for which there
is a directed edge from vertex i to vertex j.

Return the number of strongly connected components (SCCs) in the graph.
A strongly connected component is a maximal group of vertices in which
every vertex can reach every other vertex by following directed edges.
A vertex on its own can also form a strongly connected component.

Example 1:
    Input: V = 5, Adj = [[2, 3], [0], [1], [4], []]
    Output: 3
    Explanation: The strongly connected components are {0, 1, 2}, {3},
    and {4}.

Example 2:
    Input: V = 8, Adj = [[1], [2], [0, 3], [4], [5, 7], [6], [4, 7], []]
    Output: 4
    Explanation: The strongly connected components are {0, 1, 2}, {3},
    {4, 5, 6}, and {7}.

Practice question:
    Input: V = 3, Adj = [[1], [2], []]
    Choices: 2, 3, 1, 4

Constraints:
    - 1 <= V <= 5000
    - 0 <= E <= V * (V - 1), where E is the number of directed edges.
    - 0 <= ai, bi <= V - 1 for each directed edge from ai to bi.
    - Adj contains V lists.

https://www.youtube.com/watch?v=R6uoSjZ2imo&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=54
"""


def kosaraju_algorithm(vertices: int, adjacency_list: list[list[int]]) -> int:
    """Count strongly connected components in a directed graph.

    Args:
        vertices: Number V of vertices, with 1 <= V <= 5000. IDs are 0 to V - 1.
        adjacency_list: V lists, where adjacency_list[u] contains the endpoints
            of outgoing edges from u. All endpoints must be valid vertex IDs.
            E denotes the total number of entries across these lists.

    Returns:
        The number of maximal groups in which every vertex can reach every
        other vertex through directed paths. Isolated vertices each count as
        one SCC; a graph with no edges returns V. One strongly connected graph
        returns 1. The input adjacency list is not modified.

    Approach:
        Kosaraju's Algorithm using two recursive depth-first search passes.

        1. Build finishing order on the original graph. Mark a vertex visited
           immediately upon entering dfs_finish_order to avoid cycles. Explore
           each unvisited neighbor, then append the vertex AFTER all recursive
           calls return. This is DFS postorder, not discovery order or numeric
           sorting. The outer loop starts DFS at every still-unvisited vertex
           so disconnected and unreachable regions are included.
        2. Reverse every edge. Allocate an independent empty list for each
           vertex, then turn every original u -> v into reversed v -> u.
           Reversing edges preserves SCC membership: mutually reachable
           vertices remain mutually reachable with the paths reversed.
        3. Create a fresh visited_scc set for the second pass. dfs_scc marks
           vertices on entry and follows only the reversed adjacency list.
           Keep this set across all second-pass traversals.
        4. Pop vertices in decreasing finishing order. Skip already visited
           vertices. For each unvisited start, increment scc_count ONCE and
           explore its entire SCC using dfs_scc. Do not increment for every
           popped vertex or every recursive call.
        5. Return scc_count after the finishing-order stack is empty.

        Why the order and reversal work together:
            Treat each SCC as one group. Edges between different groups form
            an acyclic graph. If group A has an edge to group B, A's greatest
            DFS finishing time is larger than B's. Thus the next unvisited
            group in decreasing finish order has no incoming edge from any
            other unprocessed group in the original graph. After reversal,
            it has no outgoing edge to an unprocessed group. DFS can reach
            its own entire SCC, but cannot absorb another unprocessed SCC.
            Edges to groups already processed are stopped by visited_scc.

        Visual example:
            adjacency_list = [[2, 3], [0], [1], [4], []]

            Original edges: 0 -> 2 -> 1 -> 0, plus 0 -> 3 -> 4.

            Enter 0
                Enter 2
                    Enter 1 (0 already visited)
                    Finish 1
                Finish 2
                Enter 3
                    Enter 4
                    Finish 4
                Finish 3
            Finish 0

            Finishing stack: [1, 2, 4, 3, 0]
            Popping order:    0, 3, 4, 2, 1
            Reversed lists:  [[1], [2], [0], [0], [3]]

            Original SCC graph: {0, 1, 2} ---> {3} ---> {4}
            Reversed SCC graph: {0, 1, 2} <--- {3} <--- {4}

            Pop 0: unvisited -> count 1; reversed DFS visits {0, 1, 2}.
            Pop 3: unvisited -> count 2; its edge to 0 reaches a visited node.
            Pop 4: unvisited -> count 3; its edge to 3 reaches a visited node.
            Pop 2 and 1: already visited -> skip. Return 3.

    Time Complexity:
        O(V + E) expected time, assuming average O(1) set operations.
        V is the number of vertices, and E is the number of directed edges.
        In the example above, V = 5 and E = 5: the neighbor-list lengths are
        2 + 1 + 1 + 1 + 0 = 5.

        1. First DFS pass: the outer loop checks V vertices. Each vertex is
           entered once, and its outgoing list is scanned once, so all calls
           together examine E edges. Appending V finished vertices takes O(V).
           Total: O(V + E), not O(V * E).
        2. Reversal: allocate V empty lists and copy E reversed edges into
           them. Total: O(V + E). The nested loops scan each list's own edges,
           whose lengths sum to E; they do not scan all E edges per vertex.
        3. Second pass: pop V stack entries. Shared visited_scc ensures each
           vertex is explored once and every reversed edge is examined once
           across all DFS calls. Total: O(V + E).

        Sequential phases add:
            O(V + E) + O(V + E) + O(V + E) = O(V + E).
        Even with no edges, both passes must consider all V isolated vertices,
        which is why the bound includes V rather than just E.

    Space Complexity:
        O(V + E) additional space, excluding the supplied adjacency list.

        - reversed_adjacency_list: V inner lists and E edge entries -> O(V + E).
          For the example, there are 5 lists containing 5 entries in total.
          This is not a V x V matrix: only the existing edges are stored.
        - visited and visited_scc: up to V vertex IDs each -> O(V) each.
          These sets are shared across their respective DFS calls; each call
          does not allocate its own full visited set.
        - finish_order_stack: each vertex is appended once -> at most V IDs.
        - Recursive calls: a path can have V nested calls -> O(V) stack space.
          The two DFS passes run separately, so their maximum call depths
          do not multiply. This call stack is separate from finish_order_stack.
        - Other local variables: O(1).

        Add peak live storage and retain the dominant terms:
            O((V + E) + V + V + V + V + 1) = O(V + E).
        Space counts memory held at once, not all calls made over the run.

    Limitation:
        Both DFS helpers are recursive. Python's recursion limit may be reached
        on deep graphs allowed by V <= 5000. The finishing-order list records
        results; it does not replace the recursive call stack. This version
        therefore does not reliably handle every permitted input at the default
        recursion limit. Removing deep-recursion tests does not remove this
        limitation. No recursion-limit setting is changed by this function.

    Interview Summary:
        I record DFS finishing order, reverse all edges, and run DFS again in
        decreasing finishing order. Each new second-pass traversal identifies
        one SCC. Time and additional space are O(V + E), with a recursion-depth
        limitation in this recursive Python implementation.
    """
    # Step 1: Build DFS finishing order across the entire original graph.
    visited: set[int] = set()
    finish_order_stack: list[int] = []

    def dfs_finish_order(vertex: int) -> None:
        visited.add(vertex)
        for neighbor in adjacency_list[vertex]:
            if neighbor not in visited:
                dfs_finish_order(vertex=neighbor)
        # Step 1: Append on exit, after every neighbor has been explored.
        finish_order_stack.append(vertex)

    for vertex in range(vertices):
        if vertex in visited:
            continue
        dfs_finish_order(vertex=vertex)

    # Step 2: Reverse every directed edge using independent neighbor lists.
    reversed_adjacency_list: list[list[int]] = [[] for _ in range(vertices)]

    for vertex in range(vertices):
        for neighbor in adjacency_list[vertex]:
            reversed_adjacency_list[neighbor].append(vertex)

    # Step 3: Use fresh visitation state for DFS on the reversed graph.
    scc_count: int = 0
    visited_scc: set[int] = set()

    def dfs_scc(vertex: int) -> None:
        visited_scc.add(vertex)
        for neighbor in reversed_adjacency_list[vertex]:
            if neighbor not in visited_scc:
                dfs_scc(vertex=neighbor)

    # Step 4: Each unvisited start in decreasing finish order identifies one SCC.
    while finish_order_stack:
        start_vertex: int = finish_order_stack.pop()
        if start_vertex not in visited_scc:
            scc_count += 1
            dfs_scc(vertex=start_vertex)

    # Step 5: Return the number of second-pass DFS traversals started.
    return scc_count


def solve() -> None:
    vertices: int = 5
    adjacency_list: list[list[int]] = [[2, 3], [0], [1], [4], []]
    expected: int = 3
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second problem example: four SCCs.
    vertices: int = 8
    adjacency_list: list[list[int]] = [[1], [2], [0, 3], [4], [5, 7], [6], [4, 7], []]
    expected: int = 4
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum vertices and edges: one isolated vertex.
    vertices: int = 1
    adjacency_list: list[list[int]] = [[]]
    expected: int = 1
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two isolated vertices.
    vertices: int = 2
    adjacency_list: list[list[int]] = [[], []]
    expected: int = 2
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One directed edge does not make two vertices strongly connected.
    vertices: int = 2
    adjacency_list: list[list[int]] = [[1], []]
    expected: int = 2
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A single edge from the highest vertex to vertex zero.
    vertices: int = 2
    adjacency_list: list[list[int]] = [[], [0]]
    expected: int = 2
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two vertices connected in both directions.
    vertices: int = 2
    adjacency_list: list[list[int]] = [[1], [0]]
    expected: int = 1
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: a directed chain.
    vertices: int = 3
    adjacency_list: list[list[int]] = [[1], [2], []]
    expected: int = 3
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A directed cycle makes one SCC.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[1], [2], [3], [0]]
    expected: int = 1
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected cycles and an isolated vertex.
    vertices: int = 6
    adjacency_list: list[list[int]] = [[1], [0], [3], [4], [2], []]
    expected: int = 3
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two cycles connected by a one-way bridge.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[1], [0, 2], [3], [2]]
    expected: int = 2
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A return edge merges both cycles into one SCC.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[1], [0, 2], [3], [2, 0]]
    expected: int = 1
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diamond-shaped acyclic graph with converging paths.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[1, 2], [3], [3], []]
    expected: int = 4
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle with an outgoing tail.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1], [2], [0, 3], [4], []]
    expected: int = 3
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Incoming chain leading to a cycle.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1], [2], [3], [4], [2]]
    expected: int = 3
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated first vertex followed by a cycle.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[], [2], [3], [1]]
    expected: int = 2
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated middle vertex beside a cycle.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[2], [], [3], [0]]
    expected: int = 2
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated final vertex after a cycle.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[1], [2], [0], []]
    expected: int = 2
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Neighbor order and branching within one SCC.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[2, 1], [3], [3], [0]]
    expected: int = 1
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All edges point outward from one vertex.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1, 2, 3, 4], [], [], [], []]
    expected: int = 5
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All edges point inward to one vertex.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[], [0], [0], [0], [0]]
    expected: int = 5
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Small complete directed graph: maximum edges for V = 4.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[neighbor for neighbor in range(vertices) if neighbor != vertex] for vertex in range(vertices)]
    expected: int = 1
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with no edges.
    vertices: int = 5000
    adjacency_list: list[list[int]] = [[] for _ in range(vertices)]
    expected: int = 5000
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with one edge between endpoint IDs.
    vertices: int = 5000
    adjacency_list: list[list[int]] = [[vertices - 1]] + [[] for _ in range(vertices - 1)]
    expected: int = 5000
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices: 2500 disconnected two-vertex cycles.
    vertices: int = 5000
    adjacency_list: list[list[int]] = [[vertex ^ 1] for vertex in range(vertices)]
    expected: int = 2500
    result: int = kosaraju_algorithm(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

if __name__ == "__main__":
    solve()
