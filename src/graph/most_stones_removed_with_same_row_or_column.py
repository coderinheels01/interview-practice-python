"""365. Most Stones Removed with Same Row or Column

There are n stones at integer coordinate points on a 2D plane, with at most
one stone per coordinate point.

A stone can be removed if it shares the same row or the same column as
another stone that has not been removed.

Given an array stones of length n, where stones[i] = [xi, yi] represents
the location of the ith stone, return the maximum possible number of stones
that can be removed.

Example 1:
    Input: n = 6,
           stones = [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]
    Output: 5
    Explanation: One possible removal order is:
        [0, 0], [1, 0], [0, 1], [2, 1], [1, 2].
    The stone at [2, 2] remains.

Example 2:
    Input: n = 6,
           stones = [[0, 0], [0, 2], [1, 3], [3, 1], [3, 2], [4, 3]]
    Output: 4
    Explanation: One possible removal order is:
        [0, 0], [0, 2], [1, 3], [3, 1].
    The stones at [3, 2] and [4, 3] remain.

Practice question:
    Input: n = 2, stones = [[0, 0], [0, 2]]
    Choices: 1, 3, 2, 4

Constraints:
    - 1 <= n <= 1000
    - n == len(stones)
    - 0 <= xi, yi <= 10^4
    - No two stones are at the same position.

https://www.youtube.com/watch?v=OwMNX8SPavM&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=54
"""

from dataclasses import dataclass, field


@dataclass
class DisjointSet:
    vertices: int
    parents: list[int] = field(init=False)
    ranks: list[int] = field(init=False)

    def __post_init__(self) -> None:
        self.parents = list(range(self.vertices))
        self.ranks = [0] * self.vertices

    def find_parent(self, node: int) -> int:
        if self.parents[node] == node:
            return node
        self.parents[node] = self.find_parent(node=self.parents[node])
        return self.parents[node]

    def union_by_rank(self, node1: int, node2: int) -> bool:
        root1: int = self.find_parent(node=node1)
        root2: int = self.find_parent(node=node2)

        if root1 == root2:
            return False

        if self.ranks[root1] == self.ranks[root2]:
            self.parents[root2] = root1
            self.ranks[root1] += 1

        elif self.ranks[root1] > self.ranks[root2]:
            self.parents[root2] = root1
        else:
            self.parents[root1] = root2

        return True


def most_stones_removed_with_same_row_or_column_disjoint_set(
    stones: list[list[int]],
) -> int:
    """Return the maximum removals using row and column nodes in a DSU.

    Args:
        stones: Unique [row, column] coordinates for n stones, where
            1 <= n <= 1000 and both coordinates are between 0 and 10000.
            n is the number of stones, not a grid dimension.

    Returns:
        The maximum number of stones removable while each removed stone
        shares a row or column with a stone still present. One stone remains
        per connected component. A single stone or all isolated stones give
        0; one connected group gives n - 1. The input is not modified.

    Approach:
        Disjoint Set Union (Union-Find) with union by rank and path compression.

        1. Find the maximum row and column coordinates. Represent whole rows
           and columns as DSU nodes; unlike the DFS version, a stone is a
           connection between two nodes rather than a node itself.
        2. Allocate V = max_row + max_col + 2 nodes. Row IDs range from 0 to
           max_row. Column IDs start at max_row + 1, so row and column IDs
           never overlap. There are max_row + 1 row slots and max_col + 1
           column slots. Their sizes ADD; this is not a 2D grid allocation.
        3. For every stone [row, col], union row with col + max_row + 1.
           The stone's presence is the reason to union these endpoints; no
           pairwise coordinate comparison is needed. Equal rows reuse the
           same row node, and equal columns reuse the same column node.
           Union by rank merges different roots; equal roots need no change.
           Path compression makes searched nodes point directly to their root.
           Record both endpoint IDs in used_nodes, a set of active nodes.
        4. After every union is complete, find the root of each used node and
           collect distinct roots in component_roots. Count only used nodes:
           unused row/column slots are isolated DSU nodes but contain no stones.
           Counting all allocated roots would incorrectly include these slots.
        5. Return n minus the number of roots. Each used row/column component
           corresponds to one group of stones connected by shared rows or
           columns. In a group of k stones, k - 1 can be removed: in the graph
           whose nodes are stones, choose a spanning tree and remove leaves
           toward a final root. Each removal has a remaining neighbor. The
           final stone cannot be removed, so one must remain per component.

        Visual example:
            stones = [[0, 0], [0, 2], [2, 2]]

                       Column
                       0   1   2
                Row 0  A   .   B
                Row 1  .   .   .
                Row 2  .   .   C

            max_row = 2, max_col = 2, column offset = 3, V = 6.

            Row nodes:     R0=0  R1=1  R2=2
            Column nodes:  C0=3  C1=4  C2=5

            Stone A -> union(0, 3)
            Stone B -> union(0, 5)
            Stone C -> union(2, 5)

            C0 --- R0 --- C2 --- R2       R1       C1
                A      B      C         unused   unused

        A, B, C label connections, not DSU nodes. The repeated node 0 joins
        A and B through their shared row; repeated node 5 joins B and C through
        their shared column. used_nodes is {0, 2, 3, 5}. All four used nodes
        have one root, so the answer is 3 - 1 = 2. Unused IDs 1 and 4 are ignored.

        The largest possible column ID is max_row + max_col + 1; a list needs
        one more entry than its largest index. For [[0, 0], [0, 2]], V is
        0 + 2 + 2 = 4, covering R0=0, C0=1, C1=2, C2=3. Multiplying maxima
        would give only 0 * 2 + 2 = 2 entries, too few for column node 3.

    Time Complexity:
        O(V + n * α(V)), assuming average O(1) set operations, where
        n = len(stones) and V = max_row + max_col + 2.

        1. Find maximum coordinates: scan n stones -> O(n).
        2. Initialize parents and ranks: each has V entries -> O(V).
        3. Process n stones: one union and two set insertions each. With union
           by rank and path compression, DSU operations cost O(α(V)) amortized,
           giving O(n * α(V)) across these operations.
        4. There are at most 2n used nodes. Find each root and insert it into
           a set -> O(n * α(V)). Root-set length and the subtraction are O(1).

        α is the inverse Ackermann function, an extremely slow-growing function
        that acts like a tiny factor for practical inputs. Amortized means
        averaged across a sequence of operations, not that every individual
        lookup has constant cost.

        These phases are sequential, so add their costs:
            O(n) + O(V) + O(n * α(V)) + O(n * α(V))
            = O(V + n * α(V)).
        This is practically near O(V + n), not simply O(n): even one stone at
        [10000, 10000] causes initialization of V = 20002 nodes.

    Space Complexity:
        O(V + n) additional space, excluding the input list. More tightly,
        this is O(V), since used-node and root counts cannot exceed V.

        - parents: V integer entries -> O(V).
        - ranks: another V integer entries -> O(V).
          In the 3-stone visual example, there are 6 + 6 = 12 array entries.
          The arrays include unused rows and columns; this is why storage is
          tied to coordinate maxima rather than just the number of stones.
        - used_nodes: at most min(2n, V) IDs. Each stone contributes at most
          two IDs, and shared rows or columns reuse existing set entries.
        - component_roots: at most n roots, also bounded by used-node count.
        - Recursive find_parent calls: O(log V) stack space at most because
          union by rank bounds tree height; path compression shortens paths.
          Calls finish before later lookups, so stack space is not multiplied
          by the total number of lookups.
        - Loop variables and maximum coordinates: O(1).

        Add peak storage: O(V + V + n + n + log V + 1) = O(V + n).
        Bounding the sets by V instead gives the tighter O(V) bound. Space
        measures memory live at once, not allocations accumulated over time.

    Interview Summary:
        I treat rows and columns as separate DSU nodes, with each stone joining
        its two endpoints. I count roots only among used nodes and return n
        minus that count. Time is O(V + n * α(V)); extra space is O(V), where
        V is the sum of the row and column coordinate ranges.
    """
    # Step 1: Determine the coordinate ranges for row and column nodes.
    max_row: int = 0
    max_col: int = 0

    for row, col in stones:
        max_row = max(max_row, row)
        max_col = max(max_col, col)

    # Step 2: Allocate separate row and column ID ranges, including zero.
    ds = DisjointSet(vertices=(max_row + max_col) + 2)

    used_nodes: set[int] = set()

    # Step 3: Each stone joins its row and column; remember both active IDs.
    for row_index, col_index in stones:
        row_node = row_index
        col_node = max_row + col_index + 1
        ds.union_by_rank(node1=row_node, node2=col_node)
        used_nodes.add(row_node)
        used_nodes.add(col_node)

    # Step 4: Count distinct roots only among nodes that contain stones.
    component_roots: set[int] = set()
    for node in used_nodes:
        stone_parent = ds.find_parent(node=node)
        component_roots.add(stone_parent)

    # Step 5: Leave one stone per connected component.
    return len(stones) - len(component_roots)


def most_stones_removed_with_same_row_or_column_dfs(stones: list[list[int]]) -> int:
    """Return the maximum number of stones removable by the shared-line rule.

    Args:
        stones: Unique [row, column] coordinates for n stones, where
            1 <= n <= 1000 and coordinates are between 0 and 10000 inclusive.
            n counts stones, not rows or columns. No grid dimensions are needed.

    Returns:
        The maximum removals, leaving one stone per connected component.
        A single stone or entirely isolated stones return 0. The input list
        and its coordinates are not modified; only local structures change.

    Approach:
        Depth-First Search (DFS) with an explicit stack and row/column maps.

        1. Use each stone's list index as its node ID. Build dictionaries from
           each row and column to the IDs of stones on it. Stones sharing a
           row or column connect even if they are separated by empty positions.
        2. Keep one visited set for the entire graph. Loop over all stone IDs.
           Skip visited stones. Each unvisited stone starts a new component:
           count it once and create a fresh stack containing that stone.
        3. Pop a stone. If already visited, skip it; otherwise mark it visited
           and read its coordinates. Marking on popping allows duplicate stack
           entries, but each stone's connections are explored only once.
        4. Retrieve and remove the row list using pop(row, []), then extend the
           stack with its IDs. Do the same for the column. The [] is an empty
           list returned if the entry was already removed. Removing an entry
           is safe: all its stones are now scheduled, and each still explores
           its other connections when processed. Repeat until the stack empties.
        5. Continue the outer loop for disconnected components. Return
           n - components_count. A component with k stones permits k - 1
           removals: choose a spanning tree and remove leaves toward its root.
           Each removed leaf has a remaining neighbor sharing a row or column.
           The last stone cannot be removed: no other component shares its
           row or column. Thus one stone remains per component.

        Visual example (letters stand for stone IDs):
            A = [0, 0], B = [0, 1], C = [1, 1], D = [5, 5]

            A --- B       D
                  |
                  C

            row map: {0: [A, B], 1: [C], 5: [D]}
            col map: {0: [A], 1: [B, C], 5: [D]}

        Starting at A discovers B through row 0, then C through column 1.
        The outer loop skips B and C, already visited. D starts a second
        component. The answer is 4 stones - 2 components = 2 removals.

        A and B are different stones sharing the same row. The visited guard
        prevents reprocessing a stone; pop prevents re-expanding its row list.
        A retrieves [A, B] and removes row 0. B later gets [] for that row,
        but still explores its column to discover C. Being added to the stack
        means scheduled, not yet visited in this implementation. Do not mark
        on pushing while retaining the skip-if-visited guard after popping:
        that combination would skip every scheduled stone's exploration.

    Time Complexity:
        O(n) expected time, where n is the number of stones. Dictionary and
        set operations are assumed to take O(1) time on average.

        1. Build the maps: visit n stones and append each ID twice, once to
           its row list and once to its column list. This costs O(n).
        2. The outer loop checks all n stone IDs, costing O(n).
        3. Across all DFS traversals, each stone is explored once. Each row
           and column list is removed on its first expansion. Their combined
           length is 2n, so only 2n IDs are copied into stacks by extend.
           Those entries, plus one starting entry per component, are each
           popped once. The total DFS work is therefore O(n).

        For 4 stones, there are 4 row-list entries and 4 column-list entries:
        only 8 entries to copy, even if all stones share a row. Extending by
        k items costs O(k), not O(1); the sum of all expanded lengths is 2n.
        Nested loops do not automatically mean O(n²): the searches share
        visited and the maps rather than repeat a full search for each stone.
        Add the phases: O(n) + O(n) + O(n) = O(n).

    Space Complexity:
        O(n) additional space, excluding the input stones list.

        - Row map: at most n keys and n total stone-ID entries -> O(n).
        - Column map: at most n keys and n total stone-ID entries -> O(n).
          For 4 stones, these maps store 4 + 4 = 8 IDs. A coordinate of 10000
          does not require an array of 10001 entries: the maps store used keys.
        - visited: up to n IDs across all components -> O(n).
        - stack: O(n). Duplicates are possible, but only 2n entries come from
          list expansions over the entire run, plus component starting IDs.
        - A popped dictionary list can temporarily remain alive during extend:
          at most O(n) entries, which does not change the overall bound.
        - Empty [] fallback lists and other local variables use O(1) space.
          The temporary empty lists are not accumulated across lookups.
        - DFS is iterative, so there is no recursive call stack.

        Space measures peak live storage, not the sum of allocations over time.
        Add the storage: O(n + n + n + n + n + 1) = O(n).

    Interview Summary:
        I group stone IDs by row and column, then use DFS to count connected
        components. Expanding each row and column list once gives O(n) expected
        time and O(n) additional space. I return n minus the component count,
        because one stone must remain in each connected component.
    """

    # Step 1: Group stone IDs by their row and column.
    row_adjacency_list: dict[int, list[int]] = {}
    col_adjacency_list: dict[int, list[int]] = {}

    for stone, (row, col) in enumerate(stones):
        row_adjacency_list.setdefault(row, []).append(stone)
        col_adjacency_list.setdefault(col, []).append(stone)

    # Step 2: Keep visited across all components.
    visited: set[int] = set()

    components_count: int = 0

    for stone in range(len(stones)):
        if stone in visited:
            continue

        # Step 2: Count a new component and start its DFS.
        stack: list[int] = [stone]
        components_count += 1

        while stack:
            # Step 3: Mark on popping; skip duplicate entries already explored.
            current_stone: int = stack.pop()
            if current_stone in visited:
                continue
            row, col = stones[current_stone]
            visited.add(current_stone)

            # Step 4: Expand each row and column once; missing entries give [].
            stack.extend(row_adjacency_list.pop(row, []))
            stack.extend(col_adjacency_list.pop(col, []))

    # Step 5: Leave exactly one stone in each connected component.
    return len(stones) - components_count


def solve() -> None:
    stones: list[list[int]] = [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]
    expected: int = 5
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second problem example: two connected components.
    stones: list[list[int]] = [[0, 0], [0, 2], [1, 3], [3, 1], [3, 2], [4, 3]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum input size and minimum coordinates.
    stones: list[list[int]] = [[0, 0]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One stone at maximum coordinates.
    stones: list[list[int]] = [[10000, 10000]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stones sharing a row across the coordinate range.
    stones: list[list[int]] = [[0, 0], [0, 10000]]
    expected: int = 1
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stones sharing a column across the coordinate range.
    stones: list[list[int]] = [[0, 10000], [10000, 10000]]
    expected: int = 1
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stones with no shared row or column.
    stones: list[list[int]] = [[0, 0], [10000, 10000]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal row and column numbers across different stones do not connect them.
    stones: list[list[int]] = [[0, 1], [1, 0]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All stones isolated.
    stones: list[list[int]] = [[0, 0], [1, 1], [2, 2], [10000, 10000]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An alternating row-column chain connects indirectly.
    stones: list[list[int]] = [[0, 0], [0, 2], [3, 2], [3, 5], [8, 5]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A rectangle cycle has several paths to already visited stones.
    stones: list[list[int]] = [[0, 0], [0, 10000], [10000, 0], [10000, 10000]]
    expected: int = 3
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A branching component centered on one stone.
    stones: list[list[int]] = [[5, 5], [5, 0], [5, 10000], [0, 5], [10000, 5]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unequal component sizes and one isolated stone.
    stones: list[list[int]] = [[0, 0], [0, 1], [1, 1], [5, 5], [6, 5], [9, 9]]
    expected: int = 3
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An isolated first stone followed by a connected component.
    stones: list[list[int]] = [[9, 9], [0, 0], [0, 1], [1, 1]]
    expected: int = 2
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An isolated stone in the middle of the input.
    stones: list[list[int]] = [[0, 0], [9, 9], [0, 1], [1, 1]]
    expected: int = 2
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An isolated final stone after a connected component.
    stones: list[list[int]] = [[0, 0], [0, 1], [1, 1], [9, 9]]
    expected: int = 2
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A final bridge joins two earlier groups.
    stones: list[list[int]] = [[0, 0], [0, 1], [2, 2], [3, 2], [0, 2]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # The same bridge appears first instead.
    stones: list[list[int]] = [[0, 2], [3, 2], [0, 1], [2, 2], [0, 0]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected components interleaved in input order.
    stones: list[list[int]] = [[0, 0], [5, 5], [0, 1], [6, 5], [1, 1], [6, 7]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: all stones in one row.
    stones: list[list[int]] = [[10000, col] for col in range(1000)]
    expected: int = 999
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: all stones in one column.
    stones: list[list[int]] = [[row, 10000] for row in range(1000)]
    expected: int = 999
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: every stone is isolated.
    stones: list[list[int]] = [[value, value] for value in range(1000)]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: 500 separate connected pairs.
    stones: list[list[int]] = [
        [pair, 2 * pair + offset] for pair in range(500) for offset in range(2)
    ]
    expected: int = 500
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: a dense connected rectangle.
    stones: list[list[int]] = [[row, col] for row in range(25) for col in range(40)]
    expected: int = 999
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: a long alternating chain.
    stones: list[list[int]] = [
        [step, step + offset] for step in range(500) for offset in range(2)
    ]
    expected: int = 999
    result: int = most_stones_removed_with_same_row_or_column_dfs(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disjoint-set solution: first problem example.
    stones: list[list[int]] = [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]
    expected: int = 5
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Additional disjoint-set tests.
    # Second problem example: two connected components.
    stones: list[list[int]] = [[0, 0], [0, 2], [1, 3], [3, 1], [3, 2], [4, 3]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum input size and minimum coordinates.
    stones: list[list[int]] = [[0, 0]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One stone at maximum coordinates.
    stones: list[list[int]] = [[10000, 10000]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stones sharing a row across the coordinate range.
    stones: list[list[int]] = [[0, 0], [0, 10000]]
    expected: int = 1
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stones sharing a column across the coordinate range.
    stones: list[list[int]] = [[0, 10000], [10000, 10000]]
    expected: int = 1
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stones with no shared row or column.
    stones: list[list[int]] = [[0, 0], [10000, 10000]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal row and column numbers across different stones do not connect them.
    stones: list[list[int]] = [[0, 1], [1, 0]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All stones isolated.
    stones: list[list[int]] = [[0, 0], [1, 1], [2, 2], [10000, 10000]]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An alternating row-column chain connects indirectly.
    stones: list[list[int]] = [[0, 0], [0, 2], [3, 2], [3, 5], [8, 5]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A rectangle cycle has several paths to already visited stones.
    stones: list[list[int]] = [[0, 0], [0, 10000], [10000, 0], [10000, 10000]]
    expected: int = 3
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A branching component centered on one stone.
    stones: list[list[int]] = [[5, 5], [5, 0], [5, 10000], [0, 5], [10000, 5]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unequal component sizes and one isolated stone.
    stones: list[list[int]] = [[0, 0], [0, 1], [1, 1], [5, 5], [6, 5], [9, 9]]
    expected: int = 3
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An isolated first stone followed by a connected component.
    stones: list[list[int]] = [[9, 9], [0, 0], [0, 1], [1, 1]]
    expected: int = 2
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An isolated stone in the middle of the input.
    stones: list[list[int]] = [[0, 0], [9, 9], [0, 1], [1, 1]]
    expected: int = 2
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An isolated final stone after a connected component.
    stones: list[list[int]] = [[0, 0], [0, 1], [1, 1], [9, 9]]
    expected: int = 2
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A final bridge joins two earlier groups.
    stones: list[list[int]] = [[0, 0], [0, 1], [2, 2], [3, 2], [0, 2]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # The same bridge appears first instead.
    stones: list[list[int]] = [[0, 2], [3, 2], [0, 1], [2, 2], [0, 0]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected components interleaved in input order.
    stones: list[list[int]] = [[0, 0], [5, 5], [0, 1], [6, 5], [1, 1], [6, 7]]
    expected: int = 4
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: all stones in one row.
    stones: list[list[int]] = [[10000, col] for col in range(1000)]
    expected: int = 999
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: all stones in one column.
    stones: list[list[int]] = [[row, 10000] for row in range(1000)]
    expected: int = 999
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: every stone is isolated.
    stones: list[list[int]] = [[value, value] for value in range(1000)]
    expected: int = 0
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: 500 separate connected pairs.
    stones: list[list[int]] = [
        [pair, 2 * pair + offset] for pair in range(500) for offset in range(2)
    ]
    expected: int = 500
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: a dense connected rectangle.
    stones: list[list[int]] = [[row, col] for row in range(25) for col in range(40)]
    expected: int = 999
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stone count: a long alternating chain.
    stones: list[list[int]] = [
        [step, step + offset] for step in range(500) for offset in range(2)
    ]
    expected: int = 999
    result: int = most_stones_removed_with_same_row_or_column_disjoint_set(stones)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
