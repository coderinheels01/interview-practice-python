"""284. Making a large island

Given an n x n binary matrix grid, you may change at most one 0 to 1.
Return the size of the largest island in the grid after this operation.

An island is a group of connected 1s. Cells are connected if they share
a side: up, down, left, or right. Diagonal cells are not directly connected.
The size of an island is the number of cells it contains.

Changing a cell is optional. If the grid already contains only 1s, return
the size of that existing island.

Example 1:
    Input: grid = [[1, 0], [0, 1]]
    Output: 3
    Explanation: Change either 0 to 1 to connect the two existing land cells.
    The resulting island has size 3.

Example 2:
    Input: grid = [[1, 1], [1, 1]]
    Output: 4
    Explanation: The largest island already has size 4. No change is needed.

Example 3 (all water):
    Input: grid = [[0, 0], [0, 0]]
    Output: 1
    Explanation: Changing one 0 to 1 creates an island with just one cell.
    Only one cell can be changed, so the largest possible island has size 1.

Example 4 (single cell):
    Input: grid = [[0]]
    Output: 1
    Explanation: Change the only cell to land. If the input were [[1]], the
    answer would also be 1, with no change needed.

Example 5 (joining four separate islands):
    Input: grid = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ]
    Output: 5
    Explanation: The four land cells are initially separate because diagonal
    connections do not count. Changing the center cell (1, 1) to land joins
    all four islands: 1 + 1 + 1 + 1 + the new cell = 5.

Example 6 (several neighbors belong to the same island):
    Input: grid = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    Output: 9
    Explanation: All eight land cells already form one island. Changing the
    center to land gives size 8 + 1 = 9. Although the center touches land on
    four sides, those neighbors belong to the same island, counted only once.

Example 7 (joining two larger islands):
    Input: grid = [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
    ]
    Output: 7
    Explanation: The left and right columns are separate islands of size 3.
    Changing any cell in the middle column joins them: 3 + 1 + 3 = 7.

Example 8 (choosing where to flip matters):
    Input: grid = [
        [1, 1, 0],
        [1, 0, 0],
        [0, 0, 1],
    ]
    Output: 4
    Explanation: The top-left island has size 3. Changing (1, 1) to land
    grows it to size 4. The bottom-right cell stays separate because it is
    only diagonal to (1, 1). Changing (1, 2) instead grows the bottom-right
    island to size 2 and leaves the largest island at size 3.

Practice question:
    Input: grid = [[1, 1], [1, 0]]
    Choices: 3, 4, 2, 1

Constraints:
    - 1 <= n <= 500
    - grid has n rows and n columns.
    - 0 <= grid[i][j] <= 1

https://www.youtube.com/watch?v=lgiz0Oup6gM&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=52
"""

from dataclasses import dataclass, field


@dataclass
class DisjointSet:
    vertices: int
    parents: list[int] = field(init=False)
    size: list[int] = field(init=False)

    def __post_init__(self) -> None:
        self.parents = list(range(self.vertices))
        self.size = [1] * self.vertices

    def find_parent(self, node: int) -> int:
        if self.parents[node] == node:
            return node

        self.parents[node] = self.find_parent(node=self.parents[node])

        return self.parents[node]

    def union_by_size(self, node1: int, node2: int) -> int:
        root1: int = self.find_parent(node=node1)
        root2: int = self.find_parent(node=node2)

        if root1 == root2:
            return 0

        if self.size[root1] >= self.size[root2]:
            self.parents[root2] = root1
            self.size[root1] += self.size[root2]
            return self.size[root1]
        else:
            self.parents[root1] = root2
            self.size[root2] += self.size[root1]
            return self.size[root2]


def making_a_large_island(grid: list[list[int]]) -> int:
    """Return the largest island possible after changing at most one 0 to 1.

    Args:
        grid: A nonempty n x n binary grid, where 1 <= n <= 500. Land cells
            connect through shared sides, not diagonally.

    Returns:
        The maximum number of connected land cells after an optional flip.
        All water returns 1; all land returns n². Either single-cell input
        returns 1. The input grid is not modified: flips are hypothetical.

    Approach:
        Disjoint Set Union (Union-Find) with union by size and path compression.

        1. Create one DSU node per cell, using row_index * col + col_index
           as its ID. A root identifies a connected component, and size[root]
           records its size. Start the answer at 1 because a nonempty grid
           either has land already or allows one water cell to become land.
        2. First pass: visit every land cell and union it with land above and
           to its left. Each adjacent land pair is checked once: the right
           cell checks left, and the lower cell checks up. Different pairs
           can already share a root; union_by_size safely returns 0 then.
           Otherwise, attach the smaller component to the larger one and
           update the largest island size. Path compression makes visited
           nodes point directly to their root during root lookups.
        3. Finish all unions, then make a second pass over the grid. For each
           zero, imagine flipping it to land and start its candidate size at
           1 for that new land cell. No actual grid change or union is needed.
        4. Check all four neighbors of that zero. For each land neighbor, find
           its root and add size[root] only if that root is not in seen_roots.
           This counts each neighboring island once, even if it touches the
           zero on several sides. For example, in [[1, 1], [1, 0]], both land
           neighbors of the zero share one root: the candidate is 1 + 3 = 4,
           not 1 + 3 + 3. Create a fresh set for each zero.
        5. Keep the largest candidate and return the answer. For all-land
           grids, there are no candidates, so the first pass supplies the
           answer. For all-water grids, each candidate stays at 1.

    Time Complexity:
        O(n² * α(n²)), effectively near O(n²) in practice.

        Here n is the number of rows and columns, so there are n² cells.
        For example, a 3 x 3 grid has 9 cells, not 3.

        - Initialization: parents and size each contain n² entries, so
          creating them takes O(n²) time.
        - First pass: visit n² cells and check at most 2 neighbors per cell.
          Two is fixed regardless of grid size. Each union does root lookups;
          with union by size and path compression, DSU operations cost
          O(α(n²)) amortized, giving O(n² * α(n²)) for this pass.
        - Second pass: visit n² cells and check at most 4 neighbors per zero.
          Root lookups give O(n² * α(n²)) for this pass too. The set contains
          at most 4 roots, so its operations add only constant work here.

        α is the inverse Ackermann function, which grows extremely slowly
        and is a tiny factor for practical inputs. Amortized means averaged
        over a sequence of operations; an individual lookup may take longer.
        The exact bound keeps α rather than treating every lookup as O(1).

        Sequential phases add:
            O(n²) + O(n² * α(n²)) + O(n² * α(n²))
            = O(n² * α(n²)).
        Two full scans do not make O(n⁴): neither scan runs inside each cell
        iteration of the other scan.

    Space Complexity:
        O(n²) additional space, excluding the input grid.

        - parents: n² entries, one per cell, including water -> O(n²).
        - size: another n² entries -> O(n²).
          For a 3 x 3 grid, these arrays have 9 + 9 = 18 entries.
        - seen_roots: at most 4 entries because a zero has only 4 direct
          neighbors. Shared islands contribute fewer distinct roots. A fresh
          set is used for each zero; sets are not retained across cells, so
          peak storage is O(1), not O(n²). O(4) simplifies to O(1).
        - Direction lists and other local variables: fixed-size -> O(1).
        - Recursive find_parent calls: O(log(n²)) stack space at most for
          n > 1, because union by size bounds the tree height. Path compression
          can shorten it further. A single-cell grid uses constant stack space.

        Add the storage and keep the dominant term:
            O(n² + n² + 1 + log(n²)) = O(n²).
        Repeatedly creating a small temporary set is different from keeping
        all those sets in memory at once; space measures peak live storage.

    Interview Summary:
        I scan n² cells twice, checking a constant number of neighbors each
        time. Union-Find gives O(n² * α(n²)) time, practically near O(n²).
        The two DSU arrays dominate the O(n²) additional space.
    """
    # Step 1: Define neighbors and allocate a DSU node for every grid cell.
    row: int = len(grid)
    col: int = len(grid[0])
    delta_count_island_size: list[tuple[int, int]] = [(-1, 0), (0, -1)]
    delta_flipped_cell: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    ds = DisjointSet(vertices=row * col)
    largest_island_size: int = 1

    # Step 2: Build all existing islands, checking each adjacent pair once.
    for row_index in range(row):
        for col_index in range(col):
            if grid[row_index][col_index] == 1:
                node: int = (row_index * col) + col_index

                for row_delta, col_delta in delta_count_island_size:
                    new_row: int = row_index + row_delta
                    new_col: int = col_index + col_delta
                    neighbor_node: int = (new_row * col) + new_col

                    if (
                        0 <= new_row < row
                        and 0 <= new_col < col
                        and grid[new_row][new_col] == 1
                    ):
                        largest_island_size = max(
                            largest_island_size,
                            ds.union_by_size(node1=node, node2=neighbor_node),
                        )

    # Step 3: With island sizes complete, evaluate each hypothetical flip.
    for row_index in range(row):
        for col_index in range(col):
            if grid[row_index][col_index] == 0:
                # Start fresh for this zero; count the flipped cell itself.
                seen_roots: set[int] = set()
                current_island_size: int = 1
                # Step 4: Add each distinct neighboring island exactly once.
                for row_delta, col_delta in delta_flipped_cell:
                    new_row: int = row_index + row_delta
                    new_col: int = col_index + col_delta
                    neighbor_node: int = (new_row * col) + new_col
                    if (
                        0 <= new_row < row
                        and 0 <= new_col < col
                        and grid[new_row][new_col] == 1
                    ):
                        neighbor_root: int = ds.find_parent(node=neighbor_node)
                        if neighbor_root not in seen_roots:
                            seen_roots.add(neighbor_root)
                            neighbor_island_size: int = ds.size[neighbor_root]
                            current_island_size += neighbor_island_size

                # Step 5: Keep the best candidate across all possible flips.
                largest_island_size = max(largest_island_size, current_island_size)

    # Step 5: This also preserves the first-pass answer when there are no zeros.
    return largest_island_size


def solve() -> None:
    # Original example.
    grid: list[list[int]] = [[1, 0], [0, 1]]
    expected: int = 3
    result: int = making_a_large_island(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single water cell.
    grid: list[list[int]] = [[0]]
    expected: int = 1
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single land cell.
    grid: list[list[int]] = [[1]]
    expected: int = 1
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All water.
    grid: list[list[int]] = [[0, 0], [0, 0]]
    expected: int = 1
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All land from example two.
    grid: list[list[int]] = [[1, 1], [1, 1]]
    expected: int = 4
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One missing corner touches the same island twice.
    grid: list[list[int]] = [[1, 1], [1, 0]]
    expected: int = 4
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One land cell.
    grid: list[list[int]] = [[1, 0], [0, 0]]
    expected: int = 2
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Opposite diagonal.
    grid: list[list[int]] = [[0, 1], [1, 0]]
    expected: int = 3
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Center joins four distinct islands.
    grid: list[list[int]] = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    expected: int = 5
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Center joins three distinct islands.
    grid: list[list[int]] = [[0, 1, 0], [1, 0, 1], [0, 0, 0]]
    expected: int = 4
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Center touches one island on four sides.
    grid: list[list[int]] = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    expected: int = 9
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Join two columns of size three.
    grid: list[list[int]] = [[1, 0, 1], [1, 0, 1], [1, 0, 1]]
    expected: int = 7
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Join two rows of size three.
    grid: list[list[int]] = [[1, 1, 1], [0, 0, 0], [1, 1, 1]]
    expected: int = 7
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best flip cannot join distant islands.
    grid: list[list[int]] = [[1, 1, 0], [1, 0, 0], [0, 0, 1]]
    expected: int = 4
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Land only in final row.
    grid: list[list[int]] = [[0, 0, 0], [0, 0, 0], [1, 1, 1]]
    expected: int = 4
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Land only in first row.
    grid: list[list[int]] = [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
    expected: int = 4
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Four isolated corners do not wrap across boundaries.
    grid: list[list[int]] = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    expected: int = 3
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unequal neighboring island sizes.
    grid: list[list[int]] = [[1, 0, 1], [1, 0, 0], [1, 0, 0]]
    expected: int = 5
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid all water.
    grid: list[list[int]] = [[0] * 500 for _ in range(500)]
    expected: int = 1
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid all land.
    grid: list[list[int]] = [[1] * 500 for _ in range(500)]
    expected: int = 250000
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid with one missing center.
    grid: list[list[int]] = [
        [int((r, c) != (250, 250)) for c in range(500)] for r in range(500)
    ]
    expected: int = 250000
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid with isolated checkerboard land.
    grid: list[list[int]] = [[(r + c) % 2 for c in range(500)] for r in range(500)]
    expected: int = 5
    result: int = making_a_large_island(grid)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
