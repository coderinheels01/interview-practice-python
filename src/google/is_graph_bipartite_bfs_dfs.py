# Reference: https://www.youtube.com/watch?v=mev55LTubBY

"""
Is Graph Bipartite? (LeetCode #785)

There is an undirected graph with n nodes, labeled 0 to n - 1. You're given
a 2D array graph, where graph[u] is a list of every node adjacent to node u.

The graph is bipartite if you can split its nodes into two independent sets
A and B, such that every edge in the graph connects a node in A to a node
in B (never two nodes in the same set).

Return true if the graph is bipartite, or false otherwise.

Example 1:
  graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
  Output: false
  There's a triangle formed by nodes 0, 1, 2 — an odd cycle, which can
  never be 2-colored without a conflict.

Example 2:
  graph = [[1,3],[0,2],[1,3],[0,2]]
  Output: true
  This is a 4-node cycle — splits cleanly into {0, 2} and {1, 3}.

Notes:
  - The graph has no self-edges (graph[u] never contains u) and no
    duplicate edges.
  - The graph is undirected: if v is in graph[u], then u is in graph[v].
  - The graph may not be fully connected — you may need to check multiple
    components separately.
"""

from collections import deque


def is_graph_bipartite_bfs(graph: list[list[int]]) -> bool:
    """
    Checks whether the graph is bipartite using BFS 2-coloring.

    A graph is bipartite if its nodes can be divided into two groups such
    that every edge connects a node from one group to a node in the other —
    never two nodes in the same group.  This is equivalent to asking: can
    we color every node with one of two colors so that no two adjacent nodes
    share the same color?

    Approach — BFS 2-coloring:
      - Use a group_map array to track which color (1 or -1) each node has
        been assigned.  0 means unvisited.
      - Iterate over every node to handle disconnected components.  Skip
        nodes already colored from a previous BFS.
      - For each unvisited node, start a BFS.  Assign it color 1, then for
        each neighbor alternate the color (current * -1).
      - If a neighbor has already been colored the SAME color as the current
        node, a conflict exists → the graph is not bipartite → return False.
      - If all components are colored without conflict → return True.

    Args:
        graph: Adjacency list where graph[u] lists every neighbor of node u.

    Returns:
        True if the graph is bipartite; False otherwise.

    Time Complexity:  O(V + E)
        - V = number of nodes (len(graph)), E = total number of edges.
        - Each node is enqueued at most once; each edge (u, v) is examined
          once from u's side and once from v's side.

    Space Complexity: O(V)
        - group_map array of size V to store each node's color.
        - BFS queue holds at most V nodes at once.
    """
    n: int = len(graph)
    # group_map[i] = 0 → unvisited, 1 → group A, -1 → group B
    group_map: list[int] = [0] * n

    # Step 1: Iterate over every node to cover disconnected components.
    for node in range(n):
        # Skip nodes already colored by a previous BFS traversal
        if group_map[node] != 0:
            continue

        # Step 2: Start a BFS from this unvisited node.
        queue: deque[int] = deque([node])

        while queue:
            print(f"inside queue and size is {len(queue)} and queue is {queue}")
            current: int = queue.popleft()

            # Step 3: Assign color 1 to the source node if it hasn't been
            # colored yet (this handles the very first node in the component).
            if group_map[current] == 0:
                group_map[current] = 1

            # Step 4: Examine every neighbor of the current node.
            for neighbor in graph[current]:
                if group_map[neighbor] == 0:
                    # Neighbor is unvisited — assign the opposite color and
                    # enqueue it for further exploration.
                    group_map[neighbor] = group_map[current] * -1
                    queue.append(neighbor)
                    print(
                        f"first time coloring neighbor {neighbor} and current {current} group_map {group_map}"
                    )
                elif group_map[neighbor] == group_map[current]:
                    # Step 5: Neighbor already has the same color as current
                    # → conflict detected → graph is NOT bipartite.
                    print(
                        f"detected same color neighbor {neighbor} current {current} group_map {group_map}"
                    )
                    return False
                # If neighbor has the opposite color, no conflict — continue.

    # Step 6: All components colored successfully → graph IS bipartite.
    return True


def is_graph_bipartite_dfs(graph: list[list[int]]) -> bool:
    """
    Checks whether the graph is bipartite using iterative DFS 2-coloring.

    Uses the same 2-coloring idea as the BFS version, but explores the graph
    depth-first via an explicit stack instead of a queue.  The logic is
    otherwise identical: assign alternating colors (1 / -1) as we traverse,
    and return False the moment we find two adjacent nodes with the same color.

    Approach — iterative DFS 2-coloring:
      - Maintain a color array (0 = unvisited, 1 = group A, -1 = group B).
      - Iterate over every node to handle disconnected components; skip any
        node already colored from a previous DFS.
      - For each unvisited node, push it onto a stack and start DFS.
        * Pop the top node; if it has no color yet, assign color 1 (source).
        * For each neighbor:
            - Same color as current → conflict → return False immediately.
            - Unvisited → assign the opposite color and push onto the stack.
            - Already the opposite color → no conflict, skip.
      - If every component is colored without conflict → return True.

    Key difference from BFS:
      Because DFS uses a stack (LIFO), neighbors are visited in reverse
      insertion order and we go deep before going wide.  The correctness
      guarantee is the same: each edge is examined and the 2-coloring
      invariant is enforced the moment a neighbor is first colored.

    Args:
        graph: Adjacency list where graph[u] lists every neighbor of node u.

    Returns:
        True if the graph is bipartite; False otherwise.

    Time Complexity:  O(V + E)
        - V = number of nodes (len(graph)), E = total number of edges.
        - Each node is pushed onto the stack at most once; each edge (u, v)
          is examined once from u's side and once from v's side.

    Space Complexity: O(V)
        - color array of size V to track each node's assigned color.
        - The explicit stack holds at most V nodes in the worst case
          (e.g., a path graph where every node is stacked before any is
          popped).
    """
    n: int = len(graph)

    # color[i] = 0 → unvisited, 1 → group A, -1 → group B
    color: list[int] = [0] * n

    # Step 1: Iterate over every node to cover disconnected components.
    for node in range(n):
        # Skip nodes already colored by a previous DFS traversal.
        if color[node] != 0:
            continue

        # Step 2: Start an iterative DFS from this unvisited node.
        # Using deque as a stack (append / pop from the right end).
        stack: deque[int] = deque([node])

        while stack:
            current: int = stack.pop()

            # Step 3: Assign color 1 to the current node if it hasn't been
            # colored yet (handles the source node of each component).
            if color[current] == 0:
                color[current] = 1

            # Step 4: Examine every neighbor of the current node.
            for neighbor in graph[current]:
                if color[neighbor] == color[current]:
                    # Step 5: Neighbor shares the same color as current
                    # → conflict detected → graph is NOT bipartite.
                    return False
                elif color[neighbor] == 0:
                    # Neighbor is unvisited → assign the opposite color and
                    # push onto the stack to continue DFS from there.
                    color[neighbor] = color[current] * -1
                    stack.append(neighbor)
                # If neighbor already has the opposite color, no conflict —
                # this edge has been validated; continue to the next neighbor.

    # Step 6: All components colored successfully → graph IS bipartite.
    return True


def solve():
    graph: list[list[int]] = [[1, 3], [0, 2], [1, 3], [0, 2]]
    # print(f"is graph {graph} bipartite? {is_graph_bipartite_bfs(graph=graph)}")
    print(f"is graph {graph} bipartite? {is_graph_bipartite_dfs(graph=graph)}")
    graph: list[list[int]] = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]
    # print(f"is graph {graph} bipartite? {is_graph_bipartite_bfs(graph=graph)}")
    print(f"is graph {graph} bipartite? {is_graph_bipartite_dfs(graph=graph)}")


solve()
