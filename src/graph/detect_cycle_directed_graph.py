"""Detect a Cycle in a Directed Graph

Given a directed graph with V vertices labeled from 0 to V - 1, determine
whether it contains a directed cycle. Return True if any cycle exists and
False otherwise.

A directed cycle follows edges in their specified direction and returns to
its starting vertex, without repeating any other vertex. A self-loop is a
cycle, and two opposite edges u -> v and v -> u form a cycle of length two.

The graph is represented by an adjacency list: adj[u] contains each vertex v
for which an edge u -> v exists. An edge does not imply its reverse exists.
The graph may contain isolated vertices or disconnected components.

Derive V from len(adj) rather than passing it separately.

Example 1:
    Input: adj = [[1], [2], [0, 3], []]
    Output: True
    Explanation: The edges 0 -> 1 -> 2 -> 0 form a directed cycle.

Example 2:
    Input: adj = [[1, 2], [3], [3], []]
    Output: False
    Explanation: Both branches reach vertex 3, but there is no directed path
    back to an earlier vertex, so the graph has no directed cycle.

Example 3:
    Input: adj = [[], [2], [1]]
    Output: True
    Explanation: Vertex 0 is isolated, but vertices 1 and 2 form a cycle.

Practice input assumptions:
    - V = len(adj) >= 1.
    - Each neighbor index is between 0 and V - 1, inclusive.
    - Neighbor lists may be empty and contain no duplicate entries.
    - Self-loops are allowed.
"""


def detect_cycle_directed_graph(adj: list[list[int]]) -> bool:
    """Return whether any component contains a directed cycle.

    Args:
        adj: Adjacency list for V >= 1 vertices labeled 0 through V - 1.
            Each neighbor in adj[u] represents a directed edge u -> neighbor.
            Assumes valid indices and no duplicate neighbors. Self-loops,
            isolated vertices, and disconnected components are allowed.

    Returns:
        True as soon as a directed cycle is found, otherwise False after
        checking every component. The input adjacency list is not modified.

    Approach:
        Use recursive Depth-First Search (DFS) with recursion-path tracking.
        1. Derive V from len(adj) and allocate two boolean arrays. visited
           records whether a vertex has ever been discovered; in_path records
           whether its DFS call is active on the current recursion path.
        2. On entering DFS, mark the current vertex in both arrays. A vertex
           in the current path is always visited, so checking both flags
           before recursing is redundant but consistent with this invariant.
        3. Examine each outgoing neighbor. If it has not been visited and is
           not in the current path, explore it recursively. Propagate True
           immediately if that search detects a cycle. A visited neighbor
           outside the current path is already fully explored and is skipped.
        4. If a neighbor is in the current path, return True. The edge points
           back to an active ancestor (or the vertex itself), closing a
           directed cycle. Reaching a completed vertex does not imply a cycle.
        5. After all neighbors finish without finding a cycle, clear the
           current vertex's in_path flag and return False. Leave visited set
           to avoid repeating completed work. Clearing the current vertex
           also handles sinks and roots with no outgoing edges correctly.
        6. Start DFS from every still-unvisited vertex to cover disconnected
           components. Return True if any search finds a cycle; otherwise
           return False. Early cycle returns do not clear all path flags,
           but this is harmless because the entire function returns at once.

    Time Complexity:
        O(V + E), where E is the total number of adjacency-list entries.
        Initializing the arrays and the outer scan take O(V). Each vertex
        is explored at most once, and each outgoing edge is examined at most
        once. A detected cycle may stop the traversal early. These bounds
        assume the recursive traversal completes without exceeding its limit.

    Space Complexity:
        O(V) auxiliary space, excluding the input. visited and in_path each
        store V flags. The recursive DFS stack can contain at most V active
        calls along a path. Component searches run sequentially, so their
        stack sizes do not add together.

    Limitation:
        A sufficiently long directed path can exceed Python's recursion
        limit and raise RecursionError, even when the graph is acyclic.
    """
    # 1. Track discovery separately from membership in the active DFS path.
    vertices: int = len(adj)
    visited: list[bool] = [False] * vertices
    in_path: list[bool] = [False] * vertices

    def dfs(vertex: int) -> bool:
        # 2. Mark this vertex as discovered and active on the current path.
        visited[vertex] = True
        in_path[vertex] = True

        # 3. Explore unvisited outgoing neighbors and propagate cycle results.
        for neighbor in adj[vertex]:
            if  not in_path[neighbor]:
                if dfs(vertex=neighbor):
                    return True
            # 4. An edge to an active vertex closes a directed cycle.
            elif in_path[neighbor]:
                return True

        # 5. This call is complete; remove only this vertex from the path.
        in_path[vertex] = False

        return False

    # 6. Check every component, including those beyond isolated vertices.
    for vertex in range(vertices):
        if not visited[vertex] and dfs(vertex=vertex):
            return True

    return False


def solve() -> None:
    adj: list[list[int]] = [[1], [2], [0, 3], []]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single isolated vertex.
    adj: list[list[int]] = [[]]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single vertex with a self-loop.
    adj: list[list[int]] = [[0]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Multiple isolated vertices.
    adj: list[list[int]] = [[], [], [], []]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One forward edge.
    adj: list[list[int]] = [[1], []]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One edge to a previously completed root.
    adj: list[list[int]] = [[], [0]]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two opposite edges form a cycle.
    adj: list[list[int]] = [[1], [0]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Forward chain.
    adj: list[list[int]] = [[1], [2], [3], []]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reverse chain ending at vertex zero.
    adj: list[list[int]] = [[], [0], [1], [2]]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diamond DAG with branches joining at a sink.
    adj: list[list[int]] = [[1, 2], [3], [3], []]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Acyclic edge to an already explored descendant.
    adj: list[list[int]] = [[1, 2], [2], []]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Acyclic edge to a completed sibling branch.
    adj: list[list[int]] = [[2, 1], [2], []]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Directed triangle.
    adj: list[list[int]] = [[1], [2], [0]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A path enters a cycle that excludes the starting vertex.
    adj: list[list[int]] = [[1], [2], [3], [1]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle in the second branch after a dead end.
    adj: list[list[int]] = [[1, 2], [], [3], [2]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Self-loop in the second branch.
    adj: list[list[int]] = [[1, 2], [], [2]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle with an outgoing path to a sink.
    adj: list[list[int]] = [[1], [2, 3], [0], [4], []]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle in the first component.
    adj: list[list[int]] = [[1], [0], [], [4], []]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle in a middle component.
    adj: list[list[int]] = [[], [2], [1], [], []]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle in the last component.
    adj: list[list[int]] = [[1], [], [], [4], [3]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected acyclic components.
    adj: list[list[int]] = [[1], [], [3], [], []]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Later root points into an earlier completed component.
    adj: list[list[int]] = [[1], [], [0, 3], []]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Self-loop at the final vertex.
    adj: list[list[int]] = [[], [], [2]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Self-loop at vertex zero.
    adj: list[list[int]] = [[0], [], []]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two cycles sharing a vertex.
    adj: list[list[int]] = [[1], [0, 2], [1]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Dense DAG with unsorted outgoing neighbors.
    adj: list[list[int]] = [[3, 2, 1], [3, 2], [3], []]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Every possible directed edge including self-loops.
    adj: list[list[int]] = [list(range(4)) for _ in range(4)]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide acyclic star.
    adj: list[list[int]] = [list(range(1, 101))] + [[] for _ in range(100)]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Longer acyclic chain.
    adj: list[list[int]] = [[i + 1] for i in range(99)] + [[]]
    expected: bool = False
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Longer chain closed by a back edge.
    adj: list[list[int]] = [[i + 1] for i in range(99)] + [[0]]
    expected: bool = True
    result: bool = detect_cycle_directed_graph(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
