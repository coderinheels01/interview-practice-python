r"""
================================================================================
                    CIRCLE OVERLAP DETECTION ALGORITHM
================================================================================

PROBLEM:
--------
Determine if circles overlap (touch or intersect) with each other.

A circle is defined by:
  - Center point: (x, y)
  - Radius: r

SOLUTION FOR 2 CIRCLES:
-----------------------
Two circles overlap if the distance between their centers is LESS THAN
the sum of their radii.

Formula to find distance between two centers (x1, y1) and (x2, y2):
  distance = √((x2 - x1)² + (y2 - y1)²)

Then compare:
  IF distance < (radius1 + radius2):  circles overlap
  IF distance >= (radius1 + radius2): circles don't overlap

DIAGRAM 1: Two Circles Comparison
---------------------------------
                                    
  OVERLAPPING:              NON-OVERLAPPING:
  
  Circle A (r=50)           Circle C (r=50)
      ╭─────╮                  ╭─────╮
     ╱       ╲                ╱       ╲
    │    •    │  ↔ 60 units │    •    │ ↔ 120 units │    •    │
     ╲       ╱                ╲       ╱
      ╰─────╯                  ╰─────╯
    Circle B (r=40)         Circle D (r=40)
    
    Distance = 60            Distance = 120
    Sum = 50+40 = 90         Sum = 50+40 = 90
    60 < 90 ✓ OVERLAP        120 ≥ 90 ✗ NO OVERLAP

WHY THIS WORKS:
  Imagine a right triangle:
  - Horizontal side (x distance): x2 - x1
  - Vertical side (y distance): y2 - y1
  - Diagonal (actual distance): √((x2-x1)² + (y2-y1)²)
  
  The diagonal is the shortest path between the two centers.
  If this distance is less than the combined radii, the circles must overlap.

DIAGRAM 2: Distance Formula with Right Triangle
-----------------------------------------------

                y-axis
                  ↑
                  │         Center 2 (3, 7)
                  │              •
                  │              │╲
                  │              │ ╲ distance = √29 ≈ 5.4
                  │              │  ╲
                  │ y distance=5  │   ╲
                  │              │    ╲
                  │              │     ╲
                  │ Center 1•─────┴───── • (3, 2)
                  │ (1, 2)  x distance=2
                  │
                  └──────────────────→ x-axis
  
  Formula: distance = √((x₂ - x₁)² + (y₂ - y₁)²)
  Example: distance = √((3-1)² + (7-2)²) = √(4 + 25) = √29 ≈ 5.4

SOLUTION FOR 3+ CIRCLES:
------------------------
Check EVERY UNIQUE PAIR of circles using the same rule above.

DIAGRAM 3: Three Circles - All Pairs to Check
---------------------------------------------

              Circle 1
                 •
                / \
               /   \
              /     \         Pair 1: Circle 1 vs Circle 2
             /       \        Pair 2: Circle 1 vs Circle 3
        Circle 2 ---- Circle 3 Pair 3: Circle 2 vs Circle 3
              •       •

With 3 circles:
  - Check pair 1: Circle A vs Circle B
  - Check pair 2: Circle A vs Circle C
  - Check pair 3: Circle B vs Circle C

With 4 circles, you'd have 6 pairs to check.
With 5 circles, you'd have 10 pairs to check.

ALGORITHM EXPLANATION:
----------------------

Step 1: Create parent_indexes array
  parent_indexes = [0, 1, 2, ...]
  
  This tracks which "group" each circle belongs to.
  Initially, each circle is in its own group (group = its own index).
  
  Example with 3 circles:
    parent_indexes = [0, 1, 2]
    Circle 0 is in group 0
    Circle 1 is in group 1
    Circle 2 is in group 2

Step 2: Check all pairs and merge groups
  For each pair (i, j) where i < j:
    IF circles[i] and circles[j] overlap:
      parent_indexes[j] = parent_indexes[i]
      (Put circle j in the same group as circle i)
  
  Example with circles [(1,2,4), (3,7,5), (2,2,4)]:
    
    parent_indexes = [0, 1, 2]
    
    Check i=0, j=1: Circle 0 overlaps Circle 1?
      YES! → parent_indexes[1] = parent_indexes[0] = 0
      parent_indexes = [0, 0, 2]
    
    Check i=0, j=2: Circle 0 overlaps Circle 2?
      YES! → parent_indexes[2] = parent_indexes[0] = 0
      parent_indexes = [0, 0, 0]
    
    Check i=1, j=2: Circle 1 overlaps Circle 2?
      YES! → parent_indexes[2] = parent_indexes[1] = 0
      parent_indexes = [0, 0, 0]

Step 3: Check if all circles are in ONE group
  Convert parent_indexes to a set and check if size == 1
  
  parent_indexes = [0, 0, 0]
  set([0, 0, 0]) = {0}
  len({0}) == 1? YES → return True
  
  All circles belong to ONE circle group!

WHY THIS WORKS:
  When circles overlap, we put them in the same group.
  If Circle A overlaps B, and B overlaps C, then:
    - A and B are in same group (group A)
    - C joins group A through B
    - All three are now in the same group
  
  This automatically handles transitive connections!
  If all circles end up with the same group number,
  they all belong to ONE circle group.

EXAMPLE:
--------
circles = [(1,2,4), (3,7,5), (2,2,4)]

Circle 1: center=(1,2), radius=4
Circle 2: center=(3,7), radius=5
Circle 3: center=(2,2), radius=4

Pair 1-2: distance=√((3-1)²+(7-2)²)=√29≈5.4,  sum=4+5=9  → 5.4<9 → OVERLAP ✓
Pair 1-3: distance=√((2-1)²+(2-2)²)=√1=1,     sum=4+4=8  → 1<8   → OVERLAP ✓
Pair 2-3: distance=√((2-3)²+(2-7)²)=√26≈5.1, sum=5+4=9  → 5.1<9 → OVERLAP ✓



==== Example with trace through ===

circles = [
    (0, 0, 2),   # A
    (3, 0, 2),   # B
    (6, 0, 2),   # C
    (9, 0, 2)    # D
]

parent_indexes = [0, 1, 2, 3]

i=0, j=1: A(0,0,2) vs B(3,0,2)
  distance = √((3-0)² + 0²) = 3
  sum = 2 + 2 = 4
  3 < 4? YES → parent_indexes[1] = 0
  parent_indexes = [0, 0, 2, 3]

i=0, j=2: A(0,0,2) vs C(6,0,2)
  distance = √((6-0)² + 0²) = 6
  sum = 2 + 2 = 4
  6 < 4? NO
  parent_indexes = [0, 0, 2, 3]

i=0, j=3: A(0,0,2) vs D(9,0,2)
  distance = √((9-0)² + 0²) = 9
  sum = 2 + 2 = 4
  9 < 4? NO
  parent_indexes = [0, 0, 2, 3]

i=1, j=2: B(3,0,2) vs C(6,0,2)
  distance = √((6-3)² + 0²) = 3
  sum = 2 + 2 = 4
  3 < 4? YES → parent_indexes[2] = parent_indexes[1] = 0
  parent_indexes = [0, 0, 0, 3]

i=1, j=3: B(3,0,2) vs D(9,0,2)
  distance = √((9-3)² + 0²) = 6
  sum = 2 + 2 = 4
  6 < 4? NO
  parent_indexes = [0, 0, 0, 3]

i=2, j=3: C(6,0,2) vs D(9,0,2)
  distance = √((9-6)² + 0²) = 3
  sum = 2 + 2 = 4
  3 < 4? YES → parent_indexes[3] = parent_indexes[2] = 0
  parent_indexes = [0, 0, 0, 0]

Final check:
  set(parent_indexes) = {0}
  len({0}) == 1? YES → return True

Result: All three circles overlap! → return True
================================================================================
"""

import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from helpers import show_diagram

# ==================== DIAGRAM ====================
show_diagram("circle-diagram.png", caller_file=__file__)


def check_overlap(circle1: [int, int, int], circle2: [int, int, int]) -> bool:
    x_distance: float = abs(circle1[0] - circle2[0])
    y_distance: float = abs(circle1[1] - circle2[1])
    distance: float = math.sqrt(x_distance**2 + y_distance**2)
    radius_sum: float = circle1[2] + circle2[2]
    return radius_sum > distance


def all_circles_overlap(circles: list[tuple[int, int, int]]) -> bool:
    n: int = len(circles)
    parent_indexes = list(range(n))

    for i in range(n):
        for j in range(i + 1, n):
            if check_overlap(circles[i], circles[j]):
                parent_indexes[j] = parent_indexes[i]

    print(f"parent_indexes - {parent_indexes}")
    return len(set(parent_indexes)) == 1


# ==================== TEST CASES ====================
def run_tests():
    test_cases = [
        {
            "name": "Test 1: All circles overlap",
            "input": [(1, 2, 4), (3, 7, 5), (2, 2, 4)],
            "expected": True,
        },
        {
            "name": "Test 2: No circles overlap",
            "input": [(0, 0, 1), (10, 10, 1), (20, 20, 1)],
            "expected": False,
        },
        {
            "name": "Test 3: Two separate groups",
            "input": [(0, 0, 2), (1, 1, 2), (10, 10, 2), (11, 11, 2)],
            "expected": False,
        },
        {
            "name": "Test 4: Chain of overlaps (A-B-C)",
            "input": [(0, 0, 2), (2, 0, 2), (4, 0, 2)],
            "expected": True,
        },
        {
            "name": "Test 5: Three circles, only two overlap",
            "input": [(0, 0, 1), (1, 0, 1), (10, 10, 1)],
            "expected": False,
        },
        {
            "name": "Test 6: All circles at same location",
            "input": [(5, 5, 3), (5, 5, 3), (5, 5, 3)],
            "expected": True,
        },
        {
            "name": "Test 7: Circles touching at edge",
            "input": [(0, 0, 2), (4, 0, 2)],
            "expected": False,
        },
        {
            "name": "Test 8: Circles barely overlapping",
            "input": [(0, 0, 2), (3.9, 0, 2)],
            "expected": True,
        },
        {
            "name": "Test 9: Four circles in chain",
            "input": [(0, 0, 3), (2, 0, 3), (4, 0, 3), (6, 0, 3)],
            "expected": True,
        },
        {
            "name": "Test 10: Large circles",
            "input": [(0, 0, 100), (50, 50, 100), (100, 100, 100)],
            "expected": True,
        },
        {
            "name": "Test 10: Large circles",
            "input": [(0, 0, 2), (3, 0, 2), (6, 0, 2), (9, 0, 2)],
            "expected": True,
        },
    ]

    passed = 0
    failed = 0

    print("=" * 70)
    print("RUNNING CIRCLE OVERLAP TEST CASES")
    print("=" * 70)

    for test in test_cases:
        result = all_circles_overlap(test["input"])
        is_pass = result == test["expected"]

        status = "✓ PASS" if is_pass else "✗ FAIL"

        print(f"\n{status}: {test['name']}")
        print(f"  Input:    {test['input']}")
        print(f"  Expected: {test['expected']}")
        print(f"  Got:      {result}")

        if is_pass:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)


# Write your solution here
def solve():
    # Run the tests
    run_tests()


solve()
