"""201. Topological Sort or Kahn's Algorithm

Given a Directed Acyclic Graph (DAG) with V vertices labeled from 0 to V - 1,
return any topological ordering of its vertices.

The graph is represented by an adjacency list: adj[u] lists the vertices v
for which a directed edge u -> v exists. Derive V from len(adj) rather than
passing it separately.

A topological ordering contains every vertex exactly once. For every directed
edge u -> v, vertex u must appear before vertex v in the returned list.
A graph may have multiple valid topological orderings; any one is accepted.

The function returns a list of vertices, not a boolean. The driver checks
whether that order is valid and reports True for a valid order or False
otherwise.

Example 1:
    Input: V = 6, adj = [[], [], [3], [1], [0, 1], [0, 2]]
    Output: [5, 4, 2, 3, 1, 0]
    Explanation:
        - Vertex 5 must appear before vertices 0 and 2.
        - Vertex 2 must appear before vertex 3.
        - Vertex 3 must appear before vertex 1.
        - Vertex 4 must appear before vertices 0 and 1.
    The displayed order satisfies every edge constraint.

Example 2:
    Input: V = 4, adj = [[], [0], [0], [0]]
    Output: [3, 2, 1, 0]
    Explanation: Vertices 1, 2, and 3 must all appear before vertex 0.
    Their relative order does not matter, so this is one valid ordering.

Practice example:
    Input: V = 3, adj = [[1], [2], []]
    Pick the correct output:
        A. [0, 2, 1]
        B. [2, 1, 0]
        C. [0, 1, 2]
        D. [1, 2, 0]

Constraints:
    - 1 <= V <= 10**4.
    - 0 <= number of edges <= 10**4.
    - len(adj) == V, and every neighbor index is between 0 and V - 1.
    - The graph is directed and acyclic.

https://www.youtube.com/watch?v=5lZ0iJMrUMk&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=21

"""

from collections import deque


def topological_sort_dfs(adj: list[list[int]]) -> list[int]:
    """Return a topological ordering of a directed acyclic graph.

    Args:
        adj: Adjacency list for V vertices labeled 0 through V - 1. Each
            neighbor v in adj[u] represents an edge u -> v. Assumes a DAG
            with valid neighbor indices, 1 <= V <= 10**4, and at most 10**4
            edges. Isolated vertices and disconnected components are allowed.

    Returns:
        A list containing every vertex exactly once, with u before v for
        every edge u -> v. Any valid order is acceptable; this function does
        not guarantee the lexicographically smallest order. The input
        adjacency list is not modified.

    Approach:
        Use Depth-First Search (DFS) topological sorting via reverse postorder.
        1. Derive V from len(adj), initialize an empty result list, and create
           one visited flag per vertex, shared across all DFS calls.
        2. On entering DFS, mark the vertex visited. Recursively explore each
           unvisited outgoing neighbor. Already visited neighbors are skipped
           to avoid repeatedly processing shared descendants.
        3. Append the current vertex only after exploring all its outgoing
           neighbors. This records DFS finishing order (postorder). In a DAG,
           each neighbor is either completed by this recursive exploration or
           was completed earlier; an edge to an active ancestor would imply
           a cycle, which the input assumptions exclude. Thus, for every
           edge u -> v, v is appended before u.
        4. Start DFS from each still-unvisited vertex in index order. This
           includes disconnected components and isolated vertices, ensuring
           every vertex is appended exactly once.
        5. Reverse the finishing-order list in place and return it. Reversing
           places u before v for every edge u -> v, producing a valid
           topological order. For a single vertex, the result is [0]; with
           no edges, the result is the vertex indices in descending order.

    Time Complexity:
        O(V + E), where E is the total number of adjacency-list entries.
        Initialization and the outer loop take O(V). DFS visits each vertex
        once and scans each outgoing edge once. Appending all vertices costs
        O(V) amortized time, and reversing the list takes O(V). These bounds
        assume traversal completes without exceeding the recursion limit.

    Space Complexity:
        O(V) auxiliary space for visited flags and the recursive DFS stack,
        which can grow to V calls along a directed path. The returned list
        also stores V vertices, so including output space still gives O(V).
        Reversing the list in place uses O(1) additional space.

    Limitations:
        Cycles are not detected; a cyclic input may produce an invalid order.
        A long path can exceed Python's recursion limit and raise
        RecursionError. In particular, this recursive implementation does
        not support every valid 10,000-vertex input under the default limit.

        https://www.youtube.com/watch?v=5lZ0iJMrUMk&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=21
    """
    # 1. Initialize the vertex count, finishing-order list, and visited flags.
    vertices: int = len(adj)
    sorted_vertices: list[int] = []
    visited: list[bool] = [False] * vertices

    def dfs(vertex: int) -> None:
        # 2. Mark this vertex and explore each unvisited outgoing neighbor.
        visited[vertex] = True
        for neighbor in adj[vertex]:
            if not visited[neighbor]:
                dfs(vertex=neighbor)

        # 3. Append after all descendants have finished (DFS postorder).
        sorted_vertices.append(vertex)

    # 4. Cover all components, including isolated vertices.
    for vertex in range(vertices):
        if not visited[vertex]:
            dfs(vertex=vertex)

    # 5. Reverse postorder so every edge points forward in the result.
    sorted_vertices.reverse()

    return sorted_vertices


def topological_sort_bfs(adj: list[list[int]]) -> list[int]:
    """Return a topological ordering using Kahn's algorithm.

    Args:
        adj: Adjacency list for a directed acyclic graph with V vertices
            labeled 0 through V - 1. Each neighbor v in adj[u] represents
            an edge u -> v. Assumes valid neighbor indices, 1 <= V <= 10**4,
            and at most 10**4 edges. Disconnected components and isolated
            vertices are allowed.

    Returns:
        A list containing each vertex exactly once, with u before v for
        every edge u -> v. Multiple orders may be valid; this function does
        not guarantee the lexicographically smallest order. The input
        adjacency list is not modified.

    Approach:
        Use Kahn's algorithm (queue-based topological sorting).
        1. Derive V from len(adj). Initialize an empty deque, an output list,
           and an in-degree array. In-degree counts incoming edges whose
           source vertices have not yet been processed.
        2. Scan every outgoing edge u -> v and increment v's in-degree.
           This counts all prerequisites before processing any vertex.
        3. Enqueue all vertices with in-degree zero in vertex-index order.
           These have no prerequisites and may appear next in the result.
           Isolated vertices are included because their in-degree is zero.
        4. Remove the oldest queued vertex with popleft() and append it to
           the output. Every predecessor has already been processed, so
           placing this vertex next respects all incoming edge constraints.
        5. For each outgoing neighbor, decrement its in-degree to account for
           the processed edge. If the count becomes zero, enqueue it. A
           neighbor with several predecessors waits until the last one is
           processed. Repeat steps 4 and 5 until the queue is empty.
        6. Return the output directly; no reversal is needed. A DAG always
           has a zero-in-degree vertex while unprocessed vertices remain,
           so all components are processed. A single vertex returns [0];
           with no edges, the result is all indices in ascending order.

    Time Complexity:
        O(V + E), where E is the total number of adjacency-list entries.
        Initialization and scanning for initial sources take O(V). Counting
        in-degrees scans E edges, and processing the queue scans those edges
        once more. Each vertex is enqueued and dequeued once. Deque append
        and popleft take O(1), and output-list append takes O(1) amortized.

    Space Complexity:
        O(V) auxiliary space, excluding the input and output. The in-degree
        array stores V counts and the queue holds at most V vertices. The
        returned list also uses O(V), so including output keeps the total
        O(V). No recursive call stack is used.

    Limitation:
        The function assumes a DAG and does not explicitly report cycles.
        For cyclic input, it returns only the vertices it can process,
        producing fewer than V entries rather than a full topological order.

    https://www.youtube.com/watch?v=73sneFXuTEg&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=22

    """
    # 1. Initialize the queue, output, and remaining incoming-edge counts.
    vertices: int = len(adj)
    queue: deque[int] = deque()
    sorted_vertices: list[int] = []
    in_degree: list[int] = [0] * vertices

    # 2. Count every incoming edge before starting the traversal.
    for vertex in range(vertices):
        for neighbor in adj[vertex]:
            in_degree[neighbor] += 1

    # 3. Start with all vertices that have no prerequisites.
    for vertex in range(vertices):
        if in_degree[vertex] == 0:
            queue.append(vertex)

    # 4. Process available vertices in FIFO order and record them immediately.
    while queue:
        vertex: int = queue.popleft()
        sorted_vertices.append(vertex)

        # 5. Remove outgoing edges and enqueue newly available neighbors.
        for neighbor in adj[vertex]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 6. The processing order is already a valid topological order for a DAG.
    return sorted_vertices


def solve() -> None:
    adj: list[list[int]] = [[], [], [3], [1], [0, 1], [0, 2]]
    expected: list[int] = [5, 4, 2, 3, 1, 0]
    result: list[int] = topological_sort_dfs(adj)

    # Accept any valid order, not only the example's ordering.
    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Single vertex with zero edges.
    adj: list[list[int]] = [[]]
    expected: list[int] = [0]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Multiple isolated vertices.
    adj: list[list[int]] = [[], [], [], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # One forward edge.
    adj: list[list[int]] = [[1], []]
    expected: list[int] = [0, 1]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # One reverse edge.
    adj: list[list[int]] = [[], [0]]
    expected: list[int] = [1, 0]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Practice example: forward chain.
    adj: list[list[int]] = [[1], [2], []]
    expected: list[int] = [0, 1, 2]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Reverse chain.
    adj: list[list[int]] = [[], [0], [1], [2]]
    expected: list[int] = [3, 2, 1, 0]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Example 2: several sources share one sink.
    adj: list[list[int]] = [[], [0], [0], [0]]
    expected: list[int] = [3, 2, 1, 0]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Example 1: multiple valid orders.
    adj: list[list[int]] = [[], [], [3], [1], [0, 1], [0, 2]]
    expected: list[int] = [5, 4, 2, 3, 1, 0]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Diamond with a shared descendant.
    adj: list[list[int]] = [[1, 2], [3], [3], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Unsorted neighbors and an already reached descendant.
    adj: list[list[int]] = [[2, 1], [2], []]
    expected: list[int] = [0, 1, 2]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Disconnected chains and an isolated vertex.
    adj: list[list[int]] = [[1], [], [3], [], []]
    expected: list[int] = [0, 1, 2, 3, 4]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Later source points to an earlier vertex.
    adj: list[list[int]] = [[], [0, 2], []]
    expected: list[int] = [1, 0, 2]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Only edge is at the beginning.
    adj: list[list[int]] = [[1], [], [], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Only edge is in the middle.
    adj: list[list[int]] = [[], [2], [], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Only edge is at the end.
    adj: list[list[int]] = [[], [], [3], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Chain with nonconsecutive labels.
    adj: list[list[int]] = [[3], [4], [0], [1], []]
    expected: list[int] = [2, 0, 3, 1, 4]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Dense DAG with transitive edges.
    adj: list[list[int]] = [[1, 2, 3, 4], [2, 3, 4], [3, 4], [4], []]
    expected: list[int] = [0, 1, 2, 3, 4]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Several sources and sinks.
    adj: list[list[int]] = [[3, 4], [3], [4], [], []]
    expected: list[int] = [0, 1, 2, 3, 4]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Maximum vertices with zero edges.
    adj: list[list[int]] = [[] for _ in range(10000)]
    expected: list[int] = list(range(10000))
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Maximum vertices with one source and many sinks.
    adj: list[list[int]] = [list(range(1, 10000))] + [[] for _ in range(9999)]
    expected: list[int] = list(range(10000))
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Maximum vertices with many sources and one sink.
    adj: list[list[int]] = [[]] + [[0] for _ in range(9999)]
    expected: list[int] = list(range(1, 10000)) + [0]
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # Maximum edges: two layers with every source connected to every sink.
    adj: list[list[int]] = [list(range(100, 200)) for _ in range(100)] + [
        [] for _ in range(100)
    ]
    expected: list[int] = list(range(200))
    result: list[int] = topological_sort_dfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: two sources unlock a shared neighbor, which unlocks the final vertex.
    adj: list[list[int]] = [[2], [2], [3], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj))), result
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Single isolated vertex.
    adj: list[list[int]] = [[]]
    expected: list[int] = [0]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Several isolated vertices.
    adj: list[list[int]] = [[], [], [], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: One forward edge.
    adj: list[list[int]] = [[1], []]
    expected: list[int] = [0, 1]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: One reverse edge.
    adj: list[list[int]] = [[], [0]]
    expected: list[int] = [1, 0]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Forward chain.
    adj: list[list[int]] = [[1], [2], [3], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Reverse chain.
    adj: list[list[int]] = [[], [0], [1], [2]]
    expected: list[int] = [3, 2, 1, 0]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Example 1 with multiple sources.
    adj: list[list[int]] = [[], [], [3], [1], [0, 1], [0, 2]]
    expected: list[int] = [5, 4, 2, 3, 1, 0]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Example 2 with one shared sink.
    adj: list[list[int]] = [[], [0], [0], [0]]
    expected: list[int] = [3, 2, 1, 0]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Diamond: wait for both incoming edges.
    adj: list[list[int]] = [[1, 2], [3], [3], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Unsorted neighbors and a shortcut.
    adj: list[list[int]] = [[2, 1], [2], []]
    expected: list[int] = [0, 1, 2]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: One source releases several sinks.
    adj: list[list[int]] = [[3, 1, 2], [], [], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Unequal path lengths converge before the final sink.
    adj: list[list[int]] = [[2], [3], [4], [5], [5], [6], []]
    expected: list[int] = [0, 1, 2, 3, 4, 5, 6]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Disconnected chains and isolated vertices.
    adj: list[list[int]] = [[], [2], [], [4], [], []]
    expected: list[int] = [0, 1, 2, 3, 4, 5]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Single edge at the beginning.
    adj: list[list[int]] = [[1], [], [], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Single edge in the middle.
    adj: list[list[int]] = [[], [2], [], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Single edge at the end.
    adj: list[list[int]] = [[], [], [3], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Chain with nonconsecutive vertex labels.
    adj: list[list[int]] = [[3], [4], [0], [1], []]
    expected: list[int] = [2, 0, 3, 1, 4]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Dense DAG with many prerequisite counts.
    adj: list[list[int]] = [[1, 2, 3, 4], [2, 3, 4], [3, 4], [4], []]
    expected: list[int] = [0, 1, 2, 3, 4]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Maximum vertices and zero edges.
    adj: list[list[int]] = [[] for _ in range(10000)]
    expected: list[int] = list(range(10000))
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Maximum vertices in a forward chain.
    adj: list[list[int]] = [[i + 1] for i in range(9999)] + [[]]
    expected: list[int] = list(range(10000))
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Maximum vertices in a reverse chain.
    adj: list[list[int]] = [[]] + [[i - 1] for i in range(1, 10000)]
    expected: list[int] = list(range(9999, -1, -1))
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Maximum vertices with a wide queue after one source.
    adj: list[list[int]] = [list(range(1, 10000))] + [[] for _ in range(9999)]
    expected: list[int] = list(range(10000))
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Maximum vertices with a sink waiting for all sources.
    adj: list[list[int]] = [[]] + [[0] for _ in range(9999)]
    expected: list[int] = list(range(1, 10000)) + [0]
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Maximum edges between two layers.
    adj: list[list[int]] = [list(range(100, 200)) for _ in range(100)] + [
        [] for _ in range(100)
    ]
    expected: list[int] = list(range(200))
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")

    # BFS: Maximum vertices and edges with a chain and shortcut.
    adj: list[list[int]] = [[1, 2]] + [[i + 1] for i in range(1, 9999)] + [[]]
    expected: list[int] = list(range(10000))
    result: list[int] = topological_sort_bfs(adj)

    assert isinstance(result, list)
    assert len(result) == len(adj) and set(result) == set(range(len(adj)))
    positions: dict[int, int] = {vertex: index for index, vertex in enumerate(result)}
    assert all(
        positions[vertex] < positions[neighbor]
        for vertex, neighbors in enumerate(adj)
        for neighbor in neighbors
    )
    print(f"Expected (one valid order): {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
