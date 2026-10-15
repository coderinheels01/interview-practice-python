"""Number of Provinces

Given an undirected graph with V vertices, find the number of provinces.
Two vertices belong to the same province if there is a path between them.

A province is a group of directly or indirectly connected cities with no
connections to cities outside that group. An isolated city is one province.

The graph is provided as a square adjacency matrix, adj:
    - adj[u][v] == 1 indicates a direct connection between cities u and v.
    - adj[u][v] == 0 indicates no direct connection.
    - Connections are undirected, so the matrix is symmetric.
    - The diagonal entries are 1.
    - V = len(adj).

Return the number of provinces as an integer.

Example 1:
    Input: adj = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    Output: 2
    Explanation: Cities 0 and 2 form one province, and city 1 forms another.
    The screenshot labels these cities 1, 3, and 2, respectively.

Constraints:
    Numerical constraints are not shown in the supplied screenshot.

This separate starter is for Disjoint Set (Union-Find) practice.

https://www.youtube.com/watch?v=ZGr5nX-Gi6Y&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=48

"""

from dataclasses import dataclass, field


@dataclass
class DisjointSet:
    vertices: int
    ranks: list[int] = field(init=False)
    parents: list[int] = field(init=False)

    def __post_init__(self) -> None:
        # Step 1: Every city begins as its own root with rank zero.
        self.ranks = [0] * self.vertices
        self.parents = list(range(self.vertices))

    def _find_parent(self, node: int) -> int:
        # Step 3a: A node that points to itself is a root.
        if self.parents[node] == node:
            return node

        # Step 3a: Compress the traversed path to point directly to the root.
        self.parents[node] = self._find_parent(node=self.parents[node])
        return self.parents[node]

    def union_by_rank(self, node1: int, node2: int) -> None:

        # Step 3a: Find the representatives of both groups.
        root1: int = self._find_parent(node=node1)
        root2: int = self._find_parent(node=node2)

        # Step 3b: An edge inside one group does not create a new merge.
        if root1 == root2:
            return

        # Step 3c: Attach roots by rank; increase rank only on an equal-rank merge.
        if self.ranks[root1] == self.ranks[root2]:
            self.parents[root2] = root1
            self.ranks[root1] += 1
        elif self.ranks[root1] > self.ranks[root2]:
            self.parents[root2] = root1
        else:
            self.parents[root1] = root2

    def count_province(self) -> int:

        # Step 4: Collect vertices that point to themselves: one root per province.
        return len(
            [
                vertex
                for vertex in range(self.vertices)
                if self.parents[vertex] == vertex
            ]
        )


def number_of_provinces_disjoint_set(adj: list[list[int]]) -> int:
    """Return the number of connected provinces in an undirected graph.

    Args:
        adj: A square, symmetric adjacency matrix. A 1 represents a direct
            connection and a 0 represents no connection. Diagonal entries in
            the problem are 1, but this implementation ignores the diagonal.

    Returns:
        The number of connected components, including isolated cities.
        An empty matrix returns 0, although the screenshot does not specify
        whether empty input is allowed.

    The input matrix is not modified. Only the newly created DisjointSet's
    parent and rank arrays are modified. Input validity is assumed.

    Approach:
        Disjoint Set Union (Union-Find) with union by rank and path compression.

        1. Initialize V separate sets, one per city. Each city's parent is
           itself and its rank is zero. Rank is an upper bound on tree height;
           it is not the number of cities in the group.
        2. Scan the matrix. Skip entries where from_node >= to_node to ignore
           self-connections and process each undirected edge only once.
           The explicit skip preserves the readable full-matrix loop.
        3. For each remaining entry equal to 1, merge the connected groups:
           a. Find both roots. Path compression updates nodes visited during
              a find to point directly to their ultimate root.
           b. If the roots match, the cities already share a province.
           c. Otherwise, attach the smaller-rank root under the larger-rank
              root. For equal ranks, attach root2 under root1 and increase
              root1's rank by one. Attach roots, not arbitrary input nodes,
              so the entire groups are merged.
        4. Collect each vertex whose parent is itself, then return the length
           of that list. Each province has exactly one such root. Isolated
           cities are their own roots and are included automatically.
           No additional root lookups or path compression are needed here.

        Union changes only a group's root pointer, not every descendant's
        parent. For example, merging 3 -> 0 with 2 -> 1 can produce
        3 -> 0 -> 1 and 2 -> 1. City 3's direct parent is still 0, but its
        ultimate root is 1. Counting set(parents) would incorrectly count
        both 0 and 1. Instead, check parents[vertex] == vertex: only vertex 1
        satisfies this condition, so the province count is 1. Intermediate
        parent pointers do not affect which vertices are roots.

    Time Complexity:
        O(V^2 + E * alpha(V)), where V is the number of cities and E
        is the number of undirected edges between distinct cities.
        Initialization takes O(V). The nested loops visit V^2 positions,
        including positions skipped by continue. There are E union calls.
        With union by rank and path compression, these operations cost
        O(alpha(V)) each amortized across the sequence. The final province
        count scans V parent entries in O(V) time using constant-time equality
        checks; taking the resulting list's length is O(1).
        Alpha is the inverse Ackermann function, which grows extremely slowly.
        This is an amortized bound, not a constant-time guarantee for each
        individual lookup.

    Space Complexity:
        O(V) additional space. The parent and rank arrays each contain V
        entries. The final root list contains one entry per province, up to
        V entries, so the counting step itself uses O(V) space in the worst
        case. It builds a list rather than counting with a generator.
        Recursive root lookup uses at most O(log V) stack space because of
        union by rank; this is dominated by the O(V) arrays and root list.
        No edge list is stored. The existing O(V^2) input matrix is excluded
        from additional space.
    """
    # Step 1: Start with one separate group per city.
    vertices: int = len(adj)
    ds = DisjointSet(vertices=vertices)

    # Step 2: Consider each connection once, above the matrix diagonal.
    for from_node in range(vertices):
        for to_node in range(vertices):
            if from_node >= to_node:
                continue
            if adj[from_node][to_node] == 1:
                # Step 3: Merge the groups containing these connected cities.
                ds.union_by_rank(node1=from_node, node2=to_node)

    # Step 4: Count vertices that remain their own parents after all merges.
    return ds.count_province()


def solve() -> None:
    # Original example.
    adj: list[list[int]] = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ]
    expected: int = 2
    result: int = number_of_provinces_disjoint_set(adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single city.
    adj: list[list[int]] = [
        [1],
    ]
    expected: int = 1
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two isolated cities.
    adj: list[list[int]] = [
        [1, 0],
        [0, 1],
    ]
    expected: int = 2
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two connected cities.
    adj: list[list[int]] = [
        [1, 1],
        [1, 1],
    ]
    expected: int = 1
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All cities isolated.
    adj: list[list[int]] = [
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ]
    expected: int = 6
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All cities directly connected.
    adj: list[list[int]] = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Indirect connections in a chain.
    adj: list[list[int]] = [
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Star centered on the last city.
    adj: list[list[int]] = [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle with an isolated city.
    adj: list[list[int]] = [
        [1, 1, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
    ]
    expected: int = 2
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Separate pairs and an isolated city.
    adj: list[list[int]] = [
        [1, 1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1],
    ]
    expected: int = 4
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated first city.
    adj: list[list[int]] = [
        [1, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 1, 1],
    ]
    expected: int = 2
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated middle city.
    adj: list[list[int]] = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 1],
        [0, 0, 0, 1, 1],
    ]
    expected: int = 2
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Bridge joins two previously formed groups.
    adj: list[list[int]] = [
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Bridged group plus a separate pair.
    adj: list[list[int]] = [
        [1, 0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1, 1],
    ]
    expected: int = 2
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger isolated graph (200 is a stress size, not a supplied limit).
    adj: list[list[int]] = [
        [int(row == col) for col in range(200)] for row in range(200)
    ]
    expected: int = 200
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger complete graph.
    adj: list[list[int]] = [[1] * 200 for _ in range(200)]
    expected: int = 1
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger chain of indirect connections.
    adj: list[list[int]] = [
        [int(abs(row - col) <= 1) for col in range(200)] for row in range(200)
    ]
    expected: int = 1
    result: int = number_of_provinces_disjoint_set(adj)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
