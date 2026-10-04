"""425. Find Eventual Safe States

Given a directed graph with V vertices labeled from 0 to V - 1, return all
safe nodes in ascending order.

The graph is represented by an adjacency list: adj[i] contains each vertex
to which vertex i has an outgoing edge. Derive V from len(adj) rather than
passing it separately.

A terminal node has no outgoing edges. A node is safe if every possible
path starting from it eventually reaches a terminal node. Terminal nodes
are also safe. A node is not safe if any path from it can continue forever
by following a cycle, even if another path reaches a terminal node.

Example 1:
    Input: V = 7, adj = [[1, 2], [2, 3], [5], [0], [5], [], []]
    Output: [2, 4, 5, 6]
    Explanation:
        - Node 0 can follow 0 -> 2 -> 5 to a terminal node, but it can also
          follow the cycle 0 -> 1 -> 3 -> 0 indefinitely. It is not safe.
        - Node 1 can reach terminal node 5 through node 2, but it can also
          follow the cycle 1 -> 3 -> 0 -> 1. It is not safe.
        - Node 2 leads only to terminal node 5, so it is safe.
        - Node 3 can reach terminal node 5 through 0 -> 2, but it can also
          follow the cycle 3 -> 0 -> 1 -> 3. It is not safe.
        - Node 4 leads only to terminal node 5, so it is safe.
        - Nodes 5 and 6 are terminal nodes and are therefore safe.

Example 2:
    Input: V = 4, adj = [[1], [2], [0, 3], []]
    Output: [3]
    Explanation: Node 3 is terminal and safe. Nodes 0, 1, and 2 can all
    follow the cycle 0 -> 1 -> 2 -> 0 indefinitely. Although they can also
    reach node 3, not every path terminates, so they are not safe.

Practice example:
    Input: V = 4, adj = [[1], [2], [0], []]
    Pick the correct output:
        A. []
        B. [1, 2]
        C. [0]
        D. [3]

Constraints:
    - V == len(adj).
    - 1 <= V <= 10**4.
    - 0 <= len(adj[i]) <= V.
    - 0 <= adj[i][j] <= V - 1.
    - Each neighbor list is sorted in strictly increasing order.
    - The graph may contain self-loops.
    - 1 <= number of edges <= 4 * 10**4.
"""

from collections import deque


def find_eventual_safe_states_dfs(adj: list[list[int]]) -> list[int]:
    """Return all eventually safe vertices in ascending order.

    Args:
        adj: Adjacency list for a directed graph with V vertices labeled
            0 through V - 1. Each neighbor v in adj[u] represents u -> v.
            Assumes valid indices, strictly increasing neighbor lists,
            1 <= V <= 10**4, and 1 <= E <= 4 * 10**4. Self-loops,
            disconnected components, and terminal vertices are allowed.

    Returns:
        The vertices from which every possible path eventually reaches a
        terminal vertex, in ascending order without duplicates. Terminal
        vertices are safe; reaching a cycle through even one branch makes
        a vertex unsafe. The input adjacency list is not modified.

    Approach:
        Use recursive Depth-First Search (DFS) with memoization of safety.
        1. Initialize visited flags, a set of confirmed safe vertices, and
           an output list. Here visited does not mean simply ever visited:
           True means either currently exploring or previously found unsafe.
           Successful calls clear their flag and cache the vertex as safe;
           unsuccessful calls leave their flag set.
        2. At the start of DFS, return True immediately for a cached safe
           vertex. This avoids re-exploring shared safe descendants.
        3. Otherwise, return False if the vertex is marked visited. It is
           either on the active recursion path, closing a directed cycle,
           or already known to lead to a cycle. Both make this path unsafe.
        4. Mark the vertex visited and recursively check its outgoing
           neighbors. If any neighbor returns False, return False immediately.
           The current vertex can reach the same cycle, so its flag remains
           set too. Propagating failure marks the unsuccessful path unsafe.
        5. Only after every neighbor succeeds, clear the current visited flag,
           add the vertex to safe_nodes, and return True. A terminal vertex
           has no neighbors, so its empty loop reaches this same success
           block automatically. Finding just one safe neighbor is not enough.
        6. Scan all vertex indices in ascending order. Skip vertices whose
           flags remain set because they are unsafe. For every other vertex,
           call DFS and append it only if the call succeeds. This includes
           cached safe descendants and disconnected components. Append only
           in this outer loop, so DFS discovery order cannot affect ordering.
        7. Return the result. Every index was considered once by the outer
           loop, so the output is ascending and unique without sorting.

    Time Complexity:
        O(V + E) expected time, assuming average O(1) set membership and
        insertion. Initialization and the outer scan take O(V). Each vertex's
        neighbors are explored at most once: later calls either return from
        the safe cache or reject a marked unsafe vertex. At most E edges are
        examined in total, and output construction takes O(V). No O(V log V)
        sorting step is needed. These bounds assume recursion completes.

    Space Complexity:
        O(V) auxiliary space. The visited array stores V flags, safe_nodes
        holds at most V vertices, and the recursive stack can grow to V calls
        along a path. The returned list also contains at most V vertices, so
        including output space keeps the total O(V).

    Limitation:
        A long directed path can exceed Python's recursion limit and raise
        RecursionError. This recursive implementation therefore cannot handle
        every permitted 10,000-vertex graph under the default recursion limit.
    """
    # 1. Track active/unsafe vertices, cached safe vertices, and ordered output.
    vertices: int = len(adj)
    visited: list[bool] = [False] * vertices
    safe_nodes: set[int] = set()
    result: list[int] = []

    def dfs(vertex: int) -> bool:
        # 2. Reuse a completed safety check without traversing again.
        if vertex in safe_nodes:
            return True

        # 3. Reject an active-path revisit or a previously confirmed unsafe node.
        if visited[vertex]:
            return False

        # 4. Explore every neighbor; one unsafe branch makes this vertex unsafe.
        visited[vertex] = True

        for neighbor in adj[vertex]:
            if not dfs(vertex=neighbor):
                return False

        # 5. All neighbors are safe (or absent); finish and cache this vertex.
        visited[vertex] = False
        safe_nodes.add(vertex)
        return True

    # 6. Append safe vertices only here to preserve ascending index order.
    for vertex in range(vertices):
        if not visited[vertex] and dfs(vertex=vertex):
            result.append(vertex)

    # 7. The result is already sorted and contains no duplicates.
    return result


def find_eventual_safe_states_bfs(adj: list[list[int]]) -> list[int]:
    """Return eventually safe vertices in ascending order without recursion.

    Args:
        adj: Adjacency list for a directed graph with V vertices labeled
            0 through V - 1. An entry v in adj[u] represents an edge u -> v.
            Assumes valid indices, strictly increasing neighbor lists,
            1 <= V <= 10**4, and 1 <= E <= 4 * 10**4. Self-loops,
            disconnected components, and terminal vertices are allowed.

    Returns:
        All vertices from which every possible path eventually reaches a
        terminal vertex, in ascending order. Terminal vertices are safe.
        A vertex that can reach a cycle is unsafe even if another path
        terminates. The input adjacency list is not modified.

    Approach:
        Use Kahn's algorithm on the reversed graph to propagate safety.
        1. Initialize a deque, an outgoing-edge count for every vertex, and
           a reverse adjacency list with one empty list per vertex.
        2. For every original edge u -> v, increment out_degree[u] and add u
           to reverse_adj[v]. The count belongs to u because the edge leaves
           u. These original outgoing counts are the reversed graph's
           in-degrees, allowing Kahn's algorithm to start at original sinks.
        3. Enqueue every vertex with zero outgoing edges. These terminal
           vertices are already known to be safe, including isolated nodes.
        4. Pop a safe vertex from the queue and visit its predecessors through
           reverse_adj. Decrease each predecessor's remaining outgoing count
           by one, accounting for its edge to this processed safe vertex.
        5. Enqueue a predecessor only when its remaining count reaches zero.
           All its outgoing destinations have then been processed as safe,
           so every path from it terminates. One safe destination is not
           enough if another destination remains unsafe. Repeat until the
           queue is empty. Cycles retain edges to one another, and vertices
           leading into them retain unresolved edges, so neither is released.
        6. Scan vertex indices in ascending order and collect those whose
           final outgoing counts are zero. Queue processing order need not
           be ascending, but this final scan gives sorted, unique output
           without calling sort(). If there are no terminal vertices, the
           queue starts empty and no vertex is safe.

        Why reverse adjacency is needed:
            Once a vertex is known to be safe, we must find who points to it,
            rather than where it points. For 0 -> 1 -> 2, vertex 2 is terminal
            and adj[2] is empty, so the original list cannot directly tell us
            that vertex 1 depends on it. reverse_adj[2] = [1] and
            reverse_adj[1] = [0] let safety propagate backward: process 2,
            release 1, then release 0. Reverse adjacency finds predecessors
            directly instead of repeatedly scanning all original edges.

            For adj = [[1], [2], [], [4], [3], [1, 3]], start with terminal
            node 2. Processing it releases 1. Processing 1 releases 0 and
            decreases node 5's count from 2 to 1. Node 5 still points to node
            3 in the cycle 3 -> 4 -> 3, so it never reaches zero. The queue
            processes 2, 1, 0; the final scan returns [0, 1, 2].

    Time Complexity:
        O(V + E). Initializing structures and finding terminal vertices take
        O(V). Building reverse adjacency and counting outgoing edges take
        O(V + E). Each safe vertex is queued at most once, and each reverse
        edge is examined at most once. Deque append and popleft take O(1).
        The final ascending scan takes O(V), with no sorting step.

    Space Complexity:
        O(V + E) auxiliary space. Reverse adjacency stores V lists and E
        predecessor entries. The outgoing counts and queue each use O(V).
        The returned list holds at most V vertices, so including output
        keeps the bound O(V + E). No recursive call stack is used.

    https://www.youtube.com/watch?v=2gtg3VsDGyc&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=26
    """
    # 1. Initialize the queue, outgoing counts, and predecessor lists.
    vertices: int = len(adj)
    queue: deque[int] = deque()
    out_degree: list[int] = [0] * vertices
    reverse_adj: list[list[int]] = [[] for _ in range(vertices)]

    # 2. Reverse every edge and count outgoing edges at its original source.
    for vertex in range(vertices):
        for neighbor in adj[vertex]:
            reverse_adj[neighbor].append(vertex)
            out_degree[vertex] += 1

    # 3. Terminal vertices have zero outgoing edges and are safe immediately.
    for vertex in range(vertices):
        if out_degree[vertex] == 0:
            queue.append(vertex)

    # 4. Propagate safety backward to the original predecessors.
    while queue:
        vertex: int = queue.popleft()

        for neighbor in reverse_adj[vertex]:
            out_degree[neighbor] -= 1
            # 5. Release a predecessor only after all its destinations are safe.
            if out_degree[neighbor] == 0:
                queue.append(neighbor)

    # 6. Collect safe indices in ascending order without sorting.
    return [vertex for vertex in range(vertices) if out_degree[vertex] == 0]


def solve() -> None:
    adj: list[list[int]] = [[1, 2], [2, 3], [5], [0], [5], [], []]
    expected: list[int] = [2, 4, 5, 6]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum graph: one self-loop.
    adj: list[list[int]] = [[0]]
    expected: list[int] = []
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum edge count: one edge to a terminal.
    adj: list[list[int]] = [[1], []]
    expected: list[int] = [0, 1]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reverse edge still returns ascending safe nodes.
    adj: list[list[int]] = [[], [0]]
    expected: list[int] = [0, 1]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-node cycle.
    adj: list[list[int]] = [[1], [0]]
    expected: list[int] = []
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Example 2: cycle with a terminal exit.
    adj: list[list[int]] = [[1], [2], [0, 3], []]
    expected: list[int] = [3]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: cycle and isolated terminal.
    adj: list[list[int]] = [[1], [2], [0], []]
    expected: list[int] = [3]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Safe branch checked before a cyclic branch.
    adj: list[list[int]] = [[1, 2], [], [2]]
    expected: list[int] = [1]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cyclic branch checked before a safe branch.
    adj: list[list[int]] = [[1, 2], [1], []]
    expected: list[int] = [2]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Self-loop with an outgoing edge to a terminal.
    adj: list[list[int]] = [[0, 1], []]
    expected: list[int] = [1]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Chain of predecessors leading into a cycle.
    adj: list[list[int]] = [[1], [2], [3], [2], []]
    expected: list[int] = [4]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diamond DAG shares a safe nonterminal descendant.
    adj: list[list[int]] = [[1, 2], [3], [3], [4], []]
    expected: list[int] = [0, 1, 2, 3, 4]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Separate sources share an unsafe descendant.
    adj: list[list[int]] = [[2], [2], [3], [2], []]
    expected: list[int] = [4]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Safe nodes before a disconnected cycle.
    adj: list[list[int]] = [[1], [], [3], [2]]
    expected: list[int] = [0, 1]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Safe nodes between disconnected cycles.
    adj: list[list[int]] = [[0], [2], [], [3]]
    expected: list[int] = [1, 2]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Safe nodes after a disconnected cycle.
    adj: list[list[int]] = [[1], [0], [3], []]
    expected: list[int] = [2, 3]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All vertices have self-loops.
    adj: list[list[int]] = [[0], [1], [2], [3]]
    expected: list[int] = []
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Branching safe DAG with several terminals.
    adj: list[list[int]] = [[1, 2], [3, 4], [4, 5], [], [], []]
    expected: list[int] = list(range(6))
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One unsafe branch makes all its predecessors unsafe.
    adj: list[list[int]] = [[1], [2, 3], [4], [3], []]
    expected: list[int] = [2, 4]
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and minimum edges.
    adj: list[list[int]] = [[0]] + [[] for _ in range(9999)]
    expected: list[int] = list(range(1, 10000))
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and edges with safe two-layer graph.
    adj: list[list[int]] = [list(range(100, 500)) for _ in range(100)] + [
        [] for _ in range(9900)
    ]
    expected: list[int] = list(range(10000))
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and edges with one unsafe destination per source.
    adj: list[list[int]] = (
        [list(range(100, 498)) + [9999]]
        + [list(range(100, 499)) + [9999] for _ in range(99)]
        + [[] for _ in range(9899)]
        + [[9999]]
    )
    expected: list[int] = list(range(100, 9999))
    result: list[int] = find_eventual_safe_states_dfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: a safe chain, a cycle, and a node with both safe and unsafe paths.
    adj: list[list[int]] = [[1], [2], [], [4], [3], [1, 3]]
    expected: list[int] = [0, 1, 2]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Minimum vertices and edges: self-loop.
    adj: list[list[int]] = [[0]]
    expected: list[int] = []
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: One edge to a terminal.
    adj: list[list[int]] = [[1], []]
    expected: list[int] = [0, 1]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Reverse edge gives ascending output.
    adj: list[list[int]] = [[], [0]]
    expected: list[int] = [0, 1]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Two-vertex cycle with no initial terminal.
    adj: list[list[int]] = [[1], [0]]
    expected: list[int] = []
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Original mixed graph.
    adj: list[list[int]] = [[1, 2], [2, 3], [5], [0], [5], [], []]
    expected: list[int] = [2, 4, 5, 6]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Cycle with an exit remains unsafe.
    adj: list[list[int]] = [[1], [2], [0, 3], []]
    expected: list[int] = [3]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Safe neighbor before unsafe neighbor.
    adj: list[list[int]] = [[1, 2], [], [2]]
    expected: list[int] = [1]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Unsafe neighbor before safe neighbor.
    adj: list[list[int]] = [[1, 2], [1], []]
    expected: list[int] = [2]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Self-loop plus terminal exit.
    adj: list[list[int]] = [[0, 1], []]
    expected: list[int] = [1]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Shared safe descendant and multiple predecessors.
    adj: list[list[int]] = [[2], [2], [3, 4], [], []]
    expected: list[int] = list(range(5))
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: One safe successor is insufficient to release a predecessor.
    adj: list[list[int]] = [[1], [2, 3], [], [3]]
    expected: list[int] = [2]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Safe nodes only at the beginning.
    adj: list[list[int]] = [[1], [], [3], [2]]
    expected: list[int] = [0, 1]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Safe nodes only in the middle.
    adj: list[list[int]] = [[0], [2], [], [3]]
    expected: list[int] = [1, 2]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Safe nodes only at the end.
    adj: list[list[int]] = [[1], [0], [3], []]
    expected: list[int] = [2, 3]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: All vertices point to themselves.
    adj: list[list[int]] = [[0], [1], [2], [3]]
    expected: list[int] = []
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Several outgoing edges all lead to safe nodes.
    adj: list[list[int]] = [[1, 2, 3], [2, 3], [3], []]
    expected: list[int] = [0, 1, 2, 3]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Several sources feed the same cycle.
    adj: list[list[int]] = [[3], [3], [3, 4], [3], []]
    expected: list[int] = [4]
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Maximum vertices and minimum edges.
    adj: list[list[int]] = [[9999]] + [[] for _ in range(9999)]
    expected: list[int] = list(range(10000))
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Maximum vertices with outgoing degree V at one node.
    adj: list[list[int]] = [list(range(10000))] + [[] for _ in range(9999)]
    expected: list[int] = list(range(1, 10000))
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Maximum edges and vertices with safe destinations.
    adj: list[list[int]] = [list(range(100, 500)) for _ in range(100)] + [
        [] for _ in range(9900)
    ]
    expected: list[int] = list(range(10000))
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Maximum edges with a self-loop destination and isolated safe nodes.
    adj: list[list[int]] = [list(range(200)) for _ in range(200)] + [
        [] for _ in range(9800)
    ]
    expected: list[int] = list(range(200, 10000))
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: Wide convergence to the final terminal.
    adj: list[list[int]] = [[9999] for _ in range(9999)] + [[]]
    expected: list[int] = list(range(10000))
    result: list[int] = find_eventual_safe_states_bfs(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
