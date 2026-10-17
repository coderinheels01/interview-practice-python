"""381. Number of islands II

Given n rows and m columns, start with a matrix containing only water (0).
An array of k operations specifies cells to turn into land (1). Each
operation [row, col] changes the cell at that position to land.

After each operation, return the number of islands currently in the matrix.
An island is a group of land cells connected horizontally or vertically:
up, down, left, or right. Diagonal connections do not join islands.

Adding land at a position that is already land leaves the matrix unchanged,
but you must still include the current island count for that operation.
Return a list of k counts. Coordinates are zero-based.

Example 1:
    Input: n = 4, m = 5, k = 4,
           A = [[1, 1], [0, 1], [3, 3], [3, 4]]
    Output: [1, 1, 2, 2]
    Explanation:
        Add (1, 1): one island.
        Add (0, 1): it joins (1, 1), so there is still one island.
        Add (3, 3): it forms a separate island, giving two islands.
        Add (3, 4): it joins (3, 3), so there are still two islands.

Example 2:
    Input: n = 4, m = 5, k = 12,
           A = [[0, 0], [0, 0], [1, 1], [1, 0], [0, 1], [0, 3],
                [1, 3], [0, 4], [3, 2], [2, 2], [1, 2], [0, 2]]
    Output: [1, 1, 2, 1, 1, 2, 2, 2, 3, 3, 1, 1]
    Explanation: The repeated addition at (0, 0) does not change the count.
    Later additions can connect previously separate islands. In particular,
    adding (1, 2) connects three islands into one.

Practice question:
    Input: n = 2, m = 2, k = 4,
           A = [[0, 0], [0, 1], [1, 0], [1, 1]]
    Choices:
        [1, 1, 1, 2]
        [1, 1, 2, 1]
        [1, 2, 2, 2]
        [1, 1, 1, 1]

Constraints:
    - 1 <= n, m <= 1000
    - 1 <= k <= 10**4
    - 0 <= A[i][0] < n
    - 0 <= A[i][1] < m

The function receives A as operations; k = len(operations).

https://www.youtube.com/watch?v=Rn6B-Q4SNyA&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=51
"""

from dataclasses import dataclass, field


@dataclass
class DisjointSet:
    vertices: int
    parents: list[int] = field(init=False)
    ranks: list[int] = field(init=False)

    def __post_init__(self) -> None:
        # Step 1: Allocate DSU entries for every cell, including water cells.
        self.parents = list(range(self.vertices))
        self.ranks = [0] * self.vertices

    def find_parent(self, node: int) -> int:
        # Step 4: Find the root and compress the visited parent chain.
        if self.parents[node] == node:
            return node
        self.parents[node] = self.find_parent(node=self.parents[node])

        return self.parents[node]

    def union_by_rank(self, node1: int, node2: int) -> bool:
        # Step 4: Compare roots so we merge whole islands, not individual cells.
        root1: int = self.find_parent(node=node1)
        root2: int = self.find_parent(node=node2)

        # Neighbors already in the same island must not reduce the count again.
        if root1 == root2:
            return False

        # Attach the lower-rank root; equal ranks increase the winning root's rank.
        if self.ranks[root1] == self.ranks[root2]:
            self.parents[root2] = root1
            self.ranks[root1] += 1
        elif self.ranks[root1] > self.ranks[root2]:
            self.parents[root2] = root1
        else:
            self.parents[root1] = root2

        return True


def number_of_islands_ii(n: int, m: int, operations: list[list[int]]) -> list[int]:
    """Return the island count after each land addition to an empty grid.

    Args:
        n: Number of rows in the initially all-water grid.
        m: Number of columns in the grid.
        operations: Valid zero-based [row, col] positions to turn into land.
            Repeated positions are allowed. Inputs are assumed to satisfy
            the problem's constraints.

    Returns:
        One island count per operation, in input order. Only horizontal and
        vertical land connections count. Repeated additions leave the count
        unchanged but still produce an output entry.

    The input operations and their nested lists are not modified. The grid
    is represented by a local set of land IDs rather than a 2D matrix.

    Approach:
        Disjoint Set Union (Union-Find) with union by rank and path compression.

        1. Initialize an empty land set, a zero island count, and an output
           list. Allocate parent and rank arrays for all n * m cells.
           These arrays include water cells, but water cells are never counted
           as islands or merged until they become land.
        2. Map each operation's coordinates to node = row * m + col. Using
           the column count m as the stride gives every cell a unique ID.
           If the ID is already in visited, append the unchanged count and
           skip the rest of the operation.
        3. Add the new ID to visited and increase the island count by one.
           Initially treat the new cell as an isolated island.
        4. Examine its four neighbors. Check both coordinates are in bounds
           before checking membership or attempting a union. A computed ID
           alone cannot establish validity: an out-of-bounds column could
           otherwise appear to wrap into another row.
           For each valid land neighbor, union the two roots. Path compression
           shortens future lookups. Union by rank attaches the lower-rank
           root under the higher-rank root; equal ranks increase the winning
           root's rank by one. Decrease the island count only when union
           returns True, meaning two previously distinct islands merged.
           If multiple neighbors already belong to the same island, later
           unions return False and do not reduce the count again.
        5. Append the count after processing all neighbors. Return all counts
           after every operation has been processed.

        For example, adding a cell between two separate islands first adds
        one island, then performs two successful unions: 2 + 1 - 2 = 1.
        Touching four cells of the same island performs only one successful
        union, so the total remains unchanged.

    Time Complexity:
        Let G = n * m, K = len(operations), and L be the number of distinct
        added cells, with L <= min(K, G).
        O(G + K + L * alpha(G)) amortized, or the simpler upper bound
        O(G + K * alpha(G)), assuming expected O(1) set operations.
        Initializing the DSU arrays costs O(G). Every operation checks the
        land set and appends a result. Only new cells examine four neighbors,
        giving at most 4L union calls. Union by rank and path compression
        give O(alpha(G)) amortized per union across the sequence, where alpha
        is the extremely slowly growing inverse Ackermann function.
        Repeated additions take expected O(1) each and skip all unions.

    Space Complexity:
        O(G + K) including the returned list. The parent and rank arrays
        each contain G entries, visited stores L IDs, and the output has
        K entries. Directions use constant space. Recursive root lookup
        uses at most O(log G) stack space with union by rank, dominated by
        the arrays. Excluding output, auxiliary space is O(G).
        Using a set for visited does not make the entire implementation
        O(K) space: the DSU still allocates entries for every grid cell.
    """
    # Step 1: Track land separately from the DSU allocated for the entire grid.
    visited: set[int] = set()
    total_island_count: list[int] = []
    delta_list: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    current_islands: int = 0
    total_nodes: int = n * m

    ds = DisjointSet(vertices=total_nodes)

    for row, col in operations:
        # Step 2: Flatten coordinates and skip cells already added as land.
        node: int = (row * m) + col
        if node in visited:
            total_island_count.append(current_islands)
            continue

        # Step 3: A new land cell starts as one additional island.
        visited.add(node)
        current_islands += 1

        # Step 4: Merge with valid land neighbors, counting only successful unions.
        for row_delta, col_delta in delta_list:
            new_row = row + row_delta
            new_col = col + col_delta
            neighbor_node: int = (new_row * m) + new_col

            if (
                0 <= new_row < n
                and 0 <= new_col < m
                and neighbor_node in visited
                and ds.union_by_rank(node1=node, node2=neighbor_node)
            ):
                current_islands -= 1
        # Step 5: Record the count after this cell's connections are processed.
        total_island_count.append(current_islands)

    return total_island_count


def solve() -> None:
    # Original example.
    n: int = 4
    m: int = 5
    operations: list[list[int]] = [[1, 1], [0, 1], [3, 3], [3, 4]]
    expected: list[int] = [1, 1, 2, 2]
    result: list[int] = number_of_islands_ii(n, m, operations)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second supplied example with repeated land.
    n: int = 4
    m: int = 5
    operations: list[list[int]] = [
        [0, 0],
        [0, 0],
        [1, 1],
        [1, 0],
        [0, 1],
        [0, 3],
        [1, 3],
        [0, 4],
        [3, 2],
        [2, 2],
        [1, 2],
        [0, 2],
    ]
    expected: list[int] = [1, 1, 2, 1, 1, 2, 2, 2, 3, 3, 1, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum grid and operation count.
    n: int = 1
    m: int = 1
    operations: list[list[int]] = [[0, 0]]
    expected: list[int] = [1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated addition to the only cell.
    n: int = 1
    m: int = 1
    operations: list[list[int]] = [[0, 0], [0, 0], [0, 0]]
    expected: list[int] = [1, 1, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Fill a two by two grid; multiple neighbors in one component.
    n: int = 2
    m: int = 2
    operations: list[list[int]] = [[0, 0], [0, 1], [1, 0], [1, 1]]
    expected: list[int] = [1, 1, 1, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diagonal cells remain separate.
    n: int = 3
    m: int = 3
    operations: list[list[int]] = [[0, 0], [1, 1], [2, 2]]
    expected: list[int] = [1, 2, 3]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Horizontal bridge merges two islands.
    n: int = 1
    m: int = 3
    operations: list[list[int]] = [[0, 0], [0, 2], [0, 1]]
    expected: list[int] = [1, 2, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Vertical bridge merges two islands.
    n: int = 3
    m: int = 1
    operations: list[list[int]] = [[0, 0], [2, 0], [1, 0]]
    expected: list[int] = [1, 2, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Center connects four distinct islands.
    n: int = 3
    m: int = 3
    operations: list[list[int]] = [[0, 1], [1, 0], [1, 2], [2, 1], [1, 1]]
    expected: list[int] = [1, 2, 3, 4, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Center connects three distinct islands.
    n: int = 3
    m: int = 3
    operations: list[list[int]] = [[0, 1], [1, 0], [1, 2], [1, 1]]
    expected: list[int] = [1, 2, 3, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Center touches four neighbors already in the same island.
    n: int = 3
    m: int = 3
    operations: list[list[int]] = [
        [0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [2, 1],
        [2, 0],
        [1, 0],
        [1, 1],
    ]
    expected: list[int] = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated bridge after a merge.
    n: int = 1
    m: int = 3
    operations: list[list[int]] = [[0, 0], [0, 2], [0, 1], [0, 1]]
    expected: list[int] = [1, 2, 1, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate between distinct island additions.
    n: int = 3
    m: int = 3
    operations: list[list[int]] = [[0, 0], [0, 0], [2, 2], [2, 2], [1, 1]]
    expected: list[int] = [1, 1, 2, 2, 3]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide grid catches incorrect flattening stride.
    n: int = 2
    m: int = 5
    operations: list[list[int]] = [[0, 4], [1, 0], [1, 4], [1, 3], [1, 2], [1, 1]]
    expected: list[int] = [1, 2, 2, 2, 2, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tall grid catches incorrect flattening stride.
    n: int = 5
    m: int = 2
    operations: list[list[int]] = [[4, 0], [0, 1], [4, 1], [3, 1], [2, 1], [1, 1]]
    expected: list[int] = [1, 2, 2, 2, 2, 1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Row boundary must not wrap to the next row.
    n: int = 2
    m: int = 3
    operations: list[list[int]] = [[0, 2], [1, 0]]
    expected: list[int] = [1, 2]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Opposite borders must not wrap through negative indices.
    n: int = 3
    m: int = 3
    operations: list[list[int]] = [[2, 0], [0, 0], [0, 2], [2, 2]]
    expected: list[int] = [1, 2, 3, 4]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum dimensions with last valid coordinates.
    n: int = 1000
    m: int = 1000
    operations: list[list[int]] = [[999, 999]]
    expected: list[int] = [1]
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum width, single row.
    n: int = 1
    m: int = 1000
    operations: list[list[int]] = [[0, c] for c in range(1000)]
    expected: list[int] = [1] * 1000
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum height, single column.
    n: int = 1000
    m: int = 1
    operations: list[list[int]] = [[r, 0] for r in range(1000)]
    expected: list[int] = [1] * 1000
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum operations on minimum grid.
    n: int = 1
    m: int = 1
    operations: list[list[int]] = [[0, 0] for _ in range(10000)]
    expected: list[int] = [1] * 10000
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum dimensions and operations, connected strip.
    n: int = 1000
    m: int = 1000
    operations: list[list[int]] = [[r, c] for r in range(10) for c in range(1000)]
    expected: list[int] = [1] * 10000
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum operations forming separate islands.
    n: int = 200
    m: int = 200
    operations: list[list[int]] = [
        [r, c] for r in range(0, 200, 2) for c in range(0, 200, 2)
    ]
    expected: list[int] = list(range(1, 10001))
    result: list[int] = number_of_islands_ii(n, m, operations)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
