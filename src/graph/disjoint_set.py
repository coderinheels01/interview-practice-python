"""810. Disjoint Set

Design a disjoint set (also called union-find) data structure supporting:

    DisjointSet(n): Initialize n elements, numbered 0 through n - 1,
        each initially in its own set.
    unionByRank(u, v): Merge the sets containing u and v using the rank
        heuristic. Return None.
    unionBySize(u, v): Merge the sets containing u and v using the size
        heuristic. Return None.
    find(u, v): Return True if u and v are in the same set, otherwise False.

The operation outputs below use Python's None, True, and False in place of
the question's null, true, and false. The None for construction is an output
placeholder; constructing DisjointSet returns an instance.

Example 1:
    Input:
        operations = ["DisjointSet", "unionByRank", "unionBySize", "find", "find"]
        arguments = [[5], [0, 1], [2, 3], [0, 1], [0, 3]]
    Output: [None, None, None, True, False]
    Explanation:
        ds = DisjointSet(5) initializes five separate sets.
        ds.unionByRank(0, 1) merges the sets containing 0 and 1 using rank.
        ds.unionBySize(2, 3) merges the sets containing 2 and 3 using size.
        ds.find(0, 1) returns True because both elements share a set.
        ds.find(0, 3) returns False because they are in different sets.

Example 2:
    Input:
        operations = ["DisjointSet", "unionBySize", "unionBySize", "find", "find"]
        arguments = [[3], [0, 1], [1, 2], [0, 2], [0, 1]]
    Output: [None, None, None, True, True]
    Explanation:
        ds = DisjointSet(3) initializes three separate sets.
        ds.unionBySize(0, 1) merges the sets containing 0 and 1 using size.
        ds.unionBySize(1, 2) merges the sets containing 1 and 2 using size.
        ds.find(0, 2) and ds.find(0, 1) both return True.

Now Your Turn:
    Input:
        operations = ["DisjointSet", "unionByRank", "unionBySize",
                      "unionByRank", "find", "find"]
        arguments = [[5], [0, 1], [3, 4], [1, 2], [0, 2], [1, 3]]
    Pick the correct output:
        A. [None, None, None, None, False, False]
        B. [None, None, None, None, True, True]
        C. [None, None, None, None, True, False]
        D. [None, None, None, None, False, True]

Constraints:
    - 1 <= n <= 10**4.
    - 0 <= u, v < n.
    - At most 5 * 10**4 calls total to unionByRank, unionBySize, and find.

https://www.youtube.com/watch?v=aBxjDBC4M1U&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=47

"""

from dataclasses import dataclass, field


@dataclass
class DisjointSet:
    """Maintain sets using parent links and root metadata.

    Approach:
        Disjoint Set Union (Union-Find) with path compression, union by rank,
        and union by size.

        Rank maintenance when mixing union strategies:
            Attaching root B under root A means setting parents[B] = A.
            The general rank update is:

                rank[A] = max(rank[A], rank[B] + 1)

            The original branches under A retain their height bound rank[A].
            Branches in B's tree gain one edge above their root, giving the
            bound rank[B] + 1. The merged tree must account for both.

            Union by rank chooses a parent whose rank is at least the child's
            rank. If the ranks differ, max(3, 2 + 1) = 3 leaves the parent
            rank unchanged. If they are equal, max(2, 2 + 1) = 3 increases it
            by one. Thus the usual equal-rank increment is a shortcut for
            the same general formula, not a different rule for attachment.

            Union by size chooses the parent by number of elements instead.
            A larger set can have a lower rank, so use the general formula
            in both attachment branches. For parent rank 1 and child rank 2,
            the new bound is max(1, 2 + 1) = 3. Assigning this maximum does
            not always increase rank; it can leave the existing value intact.

            Size always adds on a successful merge, regardless of strategy.
            Only roots hold authoritative sizes. Path compression shortens
            parent chains without reducing rank, so rank is a height upper
            bound rather than necessarily the current height. Maintaining
            both metadata arrays allows later operations to use either
            heuristic. A structure using only one heuristic need not keep
            the other heuristic's metadata.

        Implementation note:
            unionByRank currently mixes root1/root2 with the original node1/
            node2 after root lookup. All rank comparisons, parent attachments,
            and size updates in that method must use roots for the reasoning
            above to hold. This documentation does not change that code.

    Time Complexity:
        Initialization: O(n), where n = vertices, to create the parents,
        rank, and size arrays.

        Root lookup: O(h) for a call traversing h parent links. Path
        compression makes the traversed nodes point directly to the root,
        reducing the work of later lookups. Each public find or union makes
        two root lookups and otherwise performs O(1) work, so its cost is
        O(h + 1), taking h as the larger of the two traversed depths.

        Standard union-find with path compression and consistent union by
        rank OR union by size has O(alpha(n)) amortized time per operation,
        where alpha is the extremely slow-growing inverse Ackermann
        function. Amortized means averaged over a sequence of operations,
        not a constant-time guarantee for every individual lookup.

        That standard bound is not asserted for the current buggy rank
        method or for arbitrary mixing solely because rank remains a height
        upper bound. A conservative bound while parent links form a valid
        forest is O(n) per operation, since a chain has at most n - 1 links.

    Space Complexity:
        O(n) persistent space for three arrays of n entries. Recursive
        _findParent calls additionally use O(h + 1) temporary stack space,
        where h is the traversed depth. For standard consistently balanced
        union-find h is O(log n); for a general valid parent forest it can
        be O(n). Total space including the arrays remains O(n). Deep chains
        can exceed Python's recursion limit before that theoretical bound.
    """

    vertices: int
    parents: list[int] = field(init=False)
    rank: list[int] = field(init=False)
    size: list[int] = field(init=False)

    def __post_init__(self) -> None:
        self.parents = list(range(self.vertices))
        self.rank = [0] * self.vertices
        self.size = [1] * self.vertices

    def _findParent(self, node: int) -> int:
        if self.parents[node] == node:
            return node
        self.parents[node] = self._findParent(self.parents[node])

        return self.parents[node]

    def unionByRank(self, node1: int, node2: int) -> None:
        root1 = self._findParent(node=node1)
        root2 = self._findParent(node=node2)

        if root1 == root2:
            return
        if self.rank[root1] == self.rank[node2]:
            self.parents[node2] = root1
            self.rank[root1] += 1
            self.size[root1] += self.size[node2]
        elif self.rank[root1] > self.rank[node2]:
            self.parents[node2] = node1
            self.size[root1] += self.size[node2]
        else:
            self.parents[root1] = node2
            self.size[node2] += self.size[root1]

    def unionBySize(self, node1: int, node2: int) -> None:
        root1 = self._findParent(node=node1)
        root2 = self._findParent(node=node2)

        if root1 == root2:
            return

        if self.size[root1] >= self.size[root2]:
            self.parents[root2] = root1
            self.rank[root1] = max(self.rank[root1], self.rank[root2] + 1)
            self.size[root1] += self.size[root2]

        else:
            self.parents[root1] = root2
            self.rank[root2] = max(self.rank[root2], self.rank[root1] + 1)
            self.size[root2] += self.size[root1]

    def find(self, node1: int, node2: int) -> bool:
        node1_parent: int = self._findParent(node=node1)
        node2_parent: int = self._findParent(node=node2)

        return node1_parent == node2_parent


def solve() -> None:
    ds: DisjointSet = DisjointSet(5)
    expected: list[bool | None] = [None, None, None, True, False]
    result: list[bool | None] = [
        None,
        ds.unionByRank(0, 1),
        ds.unionBySize(2, 3),
        ds.find(0, 1),
        ds.find(0, 3),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single element, self-unions and self-query.
    ds = DisjointSet(1)
    expected = [None, None, True]
    result = [
        ds.unionByRank(0, 0),
        ds.unionBySize(0, 0),
        ds.find(0, 0),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Initially distinct elements and symmetric connectivity checks.
    ds = DisjointSet(3)
    expected = [False, False, True]
    result = [
        ds.find(0, 2),
        ds.find(2, 0),
        ds.find(1, 1),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example.
    ds = DisjointSet(3)
    expected = [None, None, True, True]
    result = [
        ds.unionBySize(0, 1),
        ds.unionBySize(1, 2),
        ds.find(0, 2),
        ds.find(0, 1),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example with mixed heuristics.
    ds = DisjointSet(5)
    expected = [None, None, None, True, False]
    result = [
        ds.unionByRank(0, 1),
        ds.unionBySize(3, 4),
        ds.unionByRank(1, 2),
        ds.find(0, 2),
        ds.find(1, 3),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Rank union must merge entire sets using non-root endpoints.
    ds = DisjointSet(4)
    expected = [None, None, None, True, True]
    result = [
        ds.unionByRank(0, 1),
        ds.unionByRank(2, 3),
        ds.unionByRank(1, 3),
        ds.find(0, 2),
        ds.find(2, 3),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Size union must merge entire sets using non-root endpoints.
    ds = DisjointSet(4)
    expected = [None, None, None, True, True]
    result = [
        ds.unionBySize(0, 1),
        ds.unionBySize(2, 3),
        ds.unionBySize(1, 3),
        ds.find(0, 2),
        ds.find(2, 3),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated and reversed rank unions leave the same set connected.
    ds = DisjointSet(3)
    expected = [None, None, None, True, False]
    result = [
        ds.unionByRank(0, 1),
        ds.unionByRank(1, 0),
        ds.unionByRank(0, 1),
        ds.find(0, 1),
        ds.find(0, 2),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated and reversed size unions must not create parent cycles.
    ds = DisjointSet(3)
    expected = [None, None, True, False]
    result = [
        ds.unionBySize(0, 1),
        ds.unionBySize(1, 0),
        ds.find(0, 1),
        ds.find(0, 2),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed unions preserve membership of both preexisting sets.
    ds = DisjointSet(5)
    expected = [None, None, None, True, False]
    result = [
        ds.unionByRank(0, 1),
        ds.unionBySize(2, 3),
        ds.unionBySize(1, 3),
        ds.find(0, 2),
        ds.find(0, 4),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Redundant union must not increase rank.
    ds = DisjointSet(2)
    expected = [None, None, 1]
    result = [
        ds.unionByRank(0, 1),
        ds.unionByRank(0, 1),
        ds.rank[ds._findParent(0)],
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Each singleton has size one.
    ds = DisjointSet(3)
    expected = [1, 1]
    result = [
        ds.size[ds._findParent(0)],
        ds.size[ds._findParent(2)],
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Size counts distinct members despite repeated unions.
    ds = DisjointSet(3)
    expected = [None, None, None, 3]
    result = [
        ds.unionBySize(0, 1),
        ds.unionBySize(0, 1),
        ds.unionBySize(0, 2),
        ds.size[ds._findParent(0)],
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Rank merges keep sizes accurate for later size-based merges.
    ds = DisjointSet(4)
    expected = [None, None, None, 4]
    result = [
        ds.unionByRank(0, 1),
        ds.unionBySize(2, 3),
        ds.unionBySize(0, 2),
        ds.size[ds._findParent(3)],
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Size heuristic attaches a smaller set to the larger root.
    ds = DisjointSet(4)
    expected = [None, None, None, True, True]
    result = [
        ds.unionBySize(0, 1),
        ds.unionBySize(0, 2),
        ds.unionBySize(3, 0),
        ds._findParent(0) == ds._findParent(3),
        ds.parents[3] == 0,
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum element index is valid and starts disconnected.
    ds = DisjointSet(10000)
    expected = [False, None, True, False]
    result = [
        ds.find(0, 9999),
        ds.unionByRank(0, 9999),
        ds.find(0, 9999),
        ds.find(5000, 9999),
    ]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum elements and exactly 50000 public operations using unionByRank.
    ds = DisjointSet(10000)
    for node in range(1, 10000):
        ds.unionByRank(node, node - 1)
    expected = True
    result = all([ds.find(0, 9999) for _ in range(40001)])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum elements and exactly 50000 public operations using unionBySize.
    ds = DisjointSet(10000)
    for node in range(1, 10000):
        ds.unionBySize(node, node - 1)
    expected = True
    result = all([ds.find(0, 9999) for _ in range(40001)])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
