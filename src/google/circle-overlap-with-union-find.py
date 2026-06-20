def check_overlap(circle1: tuple[int, int, int], circle2: tuple[int, int, int]) -> bool:
    x_distance: int = abs(circle1[0] - circle2[0])
    y_distance: int = abs(circle1[1] - circle2[1])
    distance: int = x_distance**2 + y_distance**2
    radius_sum: int = (circle1[2] + circle2[2]) ** 2
    return radius_sum > distance


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure for tracking connected components.

    Two operations:
    1. find(x) - Find which group/component x belongs to
    2. union(x, y) - Merge the groups of x and y
    """

    def __init__(self, n: int):
        # Each element is initially its own parent (its own group)
        self.parent: list[int] = list(range(n))
        # Rank helps optimize: attach smaller tree to larger tree
        self.rank: list[int] = [0] * n

    def find(self, x):
        """
        Find the root/representative of the group containing x.
        Uses path compression: update nodes to point directly to root.

        Example: If we have chain 3→2→1→0
        After find(3), it becomes 3→0 (path compression)
        """
        if self.parent[x] != x:
            # Recursively find root and compress path
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """
        Merge the groups of x and y into one group.

        Steps:
        1. Find root of x
        2. Find root of y
        3. If different roots, make one point to the other
        """
        root_x: int = self.find(x)
        root_y: int = self.find(y)

        if root_x == root_y:
            # Already in same group, nothing to do
            return

        # Union by rank: attach smaller tree to larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            # Same rank, pick one and increase its rank
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


def circles_belong_to_single_group(circles):
    """
    Use Union-Find to check if all circles form ONE connected group.
    """
    n: int = len(circles)
    uf: UnionFind = UnionFind(n)

    # Check all pairs
    for i in range(n):
        for j in range(i + 1, n):
            if check_overlap(circles[i], circles[j]):
                # Circles i and j overlap, merge their groups
                uf.union(i, j)

    # Check if all circles have the same root
    root: int = uf.find(0)
    for i in range(1, n):
        if uf.find(i) != root:
            return False

    return True


# ==================== TRACE THROUGH EXAMPLE ====================
"""
Example: [(0, 0, 2), (3, 0, 2), (6, 0, 2), (9, 0, 2)]

A overlaps B
B overlaps C
C overlaps D

Initial parent: [0, 1, 2, 3]
Initial rank:   [0, 0, 0, 0]

Step 1: Check A(0) vs B(1) - OVERLAP
  find(0) = 0, find(1) = 1
  union(0, 1): parent[1] = 0
  parent: [0, 0, 2, 3]
  rank:   [1, 0, 0, 0]

Step 2: Check A(0) vs C(2) - NO OVERLAP
  (no change)

Step 3: Check A(0) vs D(3) - NO OVERLAP
  (no change)

Step 4: Check B(1) vs C(2) - OVERLAP
  find(1): parent[1] = 0, so return 0
  find(2): parent[2] = 2, so return 2
  union(1, 2): 
    root_1 = 0, root_2 = 2
    rank[0] = 1, rank[2] = 0
    parent[2] = 0 (attach smaller to larger)
  parent: [0, 0, 0, 3]
  rank:   [1, 0, 0, 0]

Step 5: Check B(1) vs D(3) - NO OVERLAP
  (no change)

Step 6: Check C(2) vs D(3) - OVERLAP
  find(2): parent[2] = 0, so return 0
  find(3): parent[3] = 3, so return 3
  union(2, 3):
    root_2 = 0, root_3 = 3
    rank[0] = 1, rank[3] = 0
    parent[3] = 0 (attach smaller to larger)
  parent: [0, 0, 0, 0]
  rank:   [1, 0, 0, 0]

Final check:
  find(0) = 0
  find(1) = 0
  find(2) = 0
  find(3) = 0
  All have same root → return True ✓
"""


# Test it
def solve():

    from typing import Any

    test_cases: list[Any] = [
        {
            "name": "All circles in chain",
            "input": [(0, 0, 2), (3, 0, 2), (6, 0, 2), (9, 0, 2)],
            "expected": True,
        },
        {
            "name": "Two separate groups",
            "input": [(0, 0, 2), (1, 1, 2), (10, 10, 2), (11, 11, 2)],
            "expected": False,
        },
        {
            "name": "All circles overlap",
            "input": [(1, 2, 4), (3, 7, 5), (2, 2, 4)],
            "expected": True,
        },
    ]

    print("=" * 70)
    print("UNION-FIND SOLUTION TEST")
    print("=" * 70)

    for test in test_cases:
        result: bool = circles_belong_to_single_group(test["input"])
        status: str = "✓ PASS" if result == test["expected"] else "✗ FAIL"
        print(f"\n{status}: {test['name']}")
        print(f"  Expected: {test['expected']}, Got: {result}")


solve()
