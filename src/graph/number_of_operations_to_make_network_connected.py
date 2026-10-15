"""391. Number of operations to make network connected

Given an undirected graph with n vertices and m edges, find the minimum
number of operations required to make the graph connected.

Vertices are numbered from 0 to n - 1. The graph is represented by an array
edges, where edges[i] = [a, b] indicates an edge between vertices a and b.
In one operation, an existing edge can be removed from anywhere and added
between any two vertices.

Return the minimum number of operations needed to connect all vertices.
If it is impossible to make the graph connected, return -1.

Example 1:
    Input: n = 4, edges = [[0, 1], [0, 2], [1, 2]]
    Output: 1
    Explanation: Remove edge (1, 2) and add edge (2, 3). This connects the
    two components in one operation.

Example 2:
    Input: n = 9,
           edges = [[0, 1], [0, 2], [0, 3], [1, 2], [2, 3],
                    [4, 5], [5, 6], [7, 8]]
    Output: 2
    Explanation: Initially there are three components: {0, 1, 2, 3},
    {4, 5, 6}, and {7, 8}. Remove edge (0, 2) and add edge (3, 4).
    Then remove edge (0, 3) and add edge (6, 8). All vertices are now
    connected after two operations.

Practice question:
    Input: n = 4, edges = [[0, 1]]
    Choices: 0, 3, 4, -1

Constraints:
    - 1 <= n <= 10**4
    - 1 <= len(edges) <= 10**4
    - len(edges[i]) == 2

https://www.youtube.com/watch?v=FYrl7iz9_ZU&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=49

"""

from dataclasses import dataclass, field


@dataclass
class DisjointedSet:
    vertices: int
    parents: list[int] = field(init=False)
    ranks: list[int] = field(init=False)

    def __post_init__(self) -> None:
        # Step 2: Initially every vertex is a separate component with rank zero.
        self.parents = list(range(self.vertices))
        self.ranks = [0] * self.vertices

    def _find_parent(self, node: int) -> int:
        # Step 3a: Stop at the root, which points to itself.
        if self.parents[node] == node:
            return node

        # Step 3a: Compress the visited path so future root lookups are shorter.
        self.parents[node] = self._find_parent(node=self.parents[node])
        return self.parents[node]

    def union_by_rank(self, node1: int, node2: int) -> bool:
        # Step 3a: Find the roots representing the endpoints' components.
        root1: int = self._find_parent(node=node1)
        root2: int = self._find_parent(node=node2)

        # Step 3b: A connection within one component is a reusable extra edge.
        if root1 == root2:
            return False

        # Step 3c: Merge roots by rank; only equal ranks increase the new root's rank.
        if self.ranks[root1] == self.ranks[root2]:
            self.ranks[root1] += 1
            self.parents[root2] = root1
        elif self.ranks[root1] > self.ranks[root2]:
            self.parents[root2] = root1
        else:
            self.parents[root1] = root2

        return True

    def count_groups(self) -> int:
        # Step 4: Each component has exactly one vertex whose parent is itself.
        return sum(self.parents[vertex] == vertex for vertex in range(self.vertices))


def number_of_operations_to_make_network_connected(
    n: int, edges: list[list[int]]
) -> int:
    """Return the minimum edge relocations needed to connect the network.

    Args:
        n: Number of vertices, labeled 0 through n - 1.
        edges: Undirected connections, each represented by two vertex labels.
            Inputs are assumed to satisfy the problem's constraints and have
            valid vertex labels.

    Returns:
        The minimum number of operations, or -1 if connection is impossible.
        A connected network requires zero operations. One operation relocates
        an existing edge; it does not increase the total number of edges.

    Neither edges nor its nested lists are modified. The Disjoint Set is local
    to this call, and only its parent and rank arrays are modified.

    Approach:
        Disjoint Set Union (Union-Find) with union by rank and path compression.

        1. If there are fewer than n - 1 edges, return -1 immediately. Any
           connected graph on n vertices needs at least n - 1 edges, and
           relocating edges cannot increase their number.
        2. Initialize one component per vertex and an extra-edge counter of
           zero. Each vertex starts as its own parent with rank zero.
        3. Process every edge using union_by_rank:
           a. Find both endpoints' roots using path compression.
           b. If the roots are equal, union returns False. The endpoints are
              already connected by previously accepted edges, so this edge
              is redundant and can be relocated. Increase extra_edges.
           c. Otherwise, attach the lower-rank root under the higher-rank
              root and return True. For equal ranks, attach root2 under
              root1 and increase root1's rank. Accepted edges form a forest
              that preserves connectivity within each original component;
              all rejected edges can therefore be removed together safely.
        4. Count components by checking parents[vertex] == vertex. Each
           component has one root. Intermediate parent pointers need not
           be compressed for this check. The generator supplies booleans
           to sum: True contributes 1 and False contributes 0, with no list.
        5. Connecting C separate components needs C - 1 new connections:
           each connection can reduce the component count by at most one,
           and linking the components in a chain achieves that bound.
           If extra_edges >= C - 1, relocate that many extra edges and return
           C - 1. Otherwise return -1. This function returns the count only;
           it does not actually remove or insert edges.

        For example, a triangle plus an isolated vertex has two components
        and one extra edge. Relocating a triangle edge to the isolated vertex
        connects the network in one operation.

        After processing m edges, exactly n - C unions succeeded, so
        extra_edges = m - (n - C). Thus m >= n - 1 already guarantees enough
        extra edges. The final comparison explicitly expresses the reuse
        condition, although its -1 branch cannot be reached after the early
        edge-count check for valid input.

    Time Complexity:
        O(n + m * alpha(n)) amortized, where m = len(edges).
        Initializing the arrays takes O(n). Each of m union calls performs
        two root lookups and constant additional work. Union by rank with
        path compression gives O(alpha(n)) amortized per operation across
        the sequence, where alpha is the very slowly growing inverse
        Ackermann function. An individual lookup is not guaranteed to take
        constant time. Counting roots takes O(n), and the final comparison
        takes O(1). If the initial edge-count check fails, time is O(1).

    Space Complexity:
        O(n) additional space for the parent and rank arrays. Recursive root
        lookup uses at most O(log n) stack space with union by rank. The
        generator used to count roots takes O(1) additional space and does
        not build a list. The existing input edges are excluded. If the
        early check returns -1, additional space is O(1).
    """
    # Step 1: Reject networks with too few edges to connect every vertex.
    if len(edges) < n - 1:
        return -1

    # Step 2: Initialize separate components and the reusable-edge counter.
    extra_edges: int = 0
    ds = DisjointedSet(vertices=n)

    # Step 3: Merge components, counting edges that do not require a merge.
    for from_node, to_node in edges:
        if not ds.union_by_rank(node1=from_node, node2=to_node):
            extra_edges += 1

    # Step 4: Count the roots remaining after all edges have been processed.
    groups: int = ds.count_groups()

    # Step 5: Each of groups - 1 connections requires one reusable edge.
    return groups - 1 if extra_edges >= groups - 1 else -1


def solve() -> None:
    # Original example.
    n: int = 4
    edges: list[list[int]] = [[0, 1], [0, 2], [1, 2]]
    expected: int = 1
    result: int = number_of_operations_to_make_network_connected(n, edges)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second supplied example.
    n: int = 9
    edges: list[list[int]] = [
        [0, 1],
        [0, 2],
        [0, 3],
        [1, 2],
        [2, 3],
        [4, 5],
        [5, 6],
        [7, 8],
    ]
    expected: int = 2
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One edge cannot connect four cities.
    n: int = 4
    edges: list[list[int]] = [[0, 1]]
    expected: int = -1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest network with a distinct-endpoint edge.
    n: int = 2
    edges: list[list[int]] = [[0, 1]]
    expected: int = 0
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Already connected tree.
    n: int = 5
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 3], [3, 4]]
    expected: int = 0
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Already connected cycle.
    n: int = 4
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 3], [3, 0]]
    expected: int = 0
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Complete graph has surplus edges but needs no moves.
    n: int = 5
    edges: list[list[int]] = [[u, v] for u in range(5) for v in range(u + 1, 5)]
    expected: int = 0
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exactly enough extra edges.
    n: int = 4
    edges: list[list[int]] = [[0, 1], [0, 2], [1, 2]]
    expected: int = 1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # More extra edges than needed.
    n: int = 5
    edges: list[list[int]] = [[u, v] for u in range(4) for v in range(u + 1, 4)]
    expected: int = 1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One extra edge short of the requirement.
    n: int = 5
    edges: list[list[int]] = [[0, 1], [0, 2], [1, 2]]
    expected: int = -1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Separate trees with no extra edges.
    n: int = 6
    edges: list[list[int]] = [[0, 1], [1, 2], [3, 4], [4, 5]]
    expected: int = -1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Extra edges spread across components.
    n: int = 7
    edges: list[list[int]] = [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3]]
    expected: int = 2
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated first vertex.
    n: int = 4
    edges: list[list[int]] = [[1, 2], [2, 3], [3, 1]]
    expected: int = 1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated middle vertex.
    n: int = 4
    edges: list[list[int]] = [[0, 2], [2, 3], [3, 0]]
    expected: int = 1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reversed endpoints and shuffled connections.
    n: int = 4
    edges: list[list[int]] = [[2, 1], [0, 2], [1, 0]]
    expected: int = 1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Bridge merges previously built groups.
    n: int = 4
    edges: list[list[int]] = [[0, 3], [1, 2], [2, 3]]
    expected: int = 0
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum n and edge count; self-loops are not excluded by supplied constraints.
    n: int = 1
    edges: list[list[int]] = [[0, 0]]
    expected: int = 0
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum n with minimum edge count.
    n: int = 10000
    edges: list[list[int]] = [[0, 9999]]
    expected: int = -1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum n with exactly n minus one edges.
    n: int = 10000
    edges: list[list[int]] = [[i, i + 1] for i in range(9999)]
    expected: int = 0
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum n and edge count, already connected.
    n: int = 10000
    edges: list[list[int]] = [[i, i + 1] for i in range(9999)] + [[0, 9999]]
    expected: int = 0
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum edge count with one isolated city.
    n: int = 10000
    edges: list[list[int]] = [[i, i + 1] for i in range(9998)] + [[0, 2], [0, 3]]
    expected: int = 1
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum edge count with two isolated cities.
    n: int = 10000
    edges: list[list[int]] = [[i, i + 1] for i in range(9997)] + [
        [0, 2],
        [0, 3],
        [0, 4],
    ]
    expected: int = 2
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reverse chain followed by a cycle-closing edge.
    n: int = 10000
    edges: list[list[int]] = [[i, i - 1] for i in range(1, 10000)] + [[0, 9999]]
    expected: int = 0
    result: int = number_of_operations_to_make_network_connected(n, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
