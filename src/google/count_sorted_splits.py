r"""
================================================================================
                        COUNT SORTED SPLITS
================================================================================

PROBLEM:
--------
You are given an array A of N integers. You can split the array into two
non-empty parts — left and right. Sort the elements in each part independently
and then join them back together.

Your task is to find the number of ways to split the array into two parts such
that, after sorting both parts and joining them back, the resulting array is
sorted in non-decreasing order.

FUNCTION SIGNATURE:
-------------------
  int solution(vector<int> &A)

EXAMPLE:
--------
  A = [1, 3, 2, 4]

  Split 1: left=[1],       right=[3,2,4]
    sorted left=[1],       sorted right=[2,3,4]
    joined=[1,2,3,4]  → max(left)=1  ≤  min(right)=2  ✓  VALID

  Split 2: left=[1,3],     right=[2,4]
    sorted left=[1,3],     sorted right=[2,4]
    joined=[1,3,2,4]  → max(left)=3  >  min(right)=2  ✗  INVALID

  Split 3: left=[1,3,2],   right=[4]
    sorted left=[1,2,3],   sorted right=[4]
    joined=[1,2,3,4]  → max(left)=3  ≤  min(right)=4  ✓  VALID

  Valid splits: #1 and #3 → Answer = 2

KEY INSIGHT:
------------
After sorting both halves independently, the joined array is fully sorted if
and only if:

  max(left half) <= min(right half)

So for each split index i (1 ≤ i < N), we only need to check:
  - The maximum value in A[0..i-1]
  - The minimum value in A[i..N-1]

ALGORITHM:
----------
  Brute Force:
    Step 1: Try every valid split index i from 1 to N-1.
            (left = A[:i], right = A[i:])

    Step 2: For each split, sort both halves.
            The last element of sorted left  = max(left).
            The first element of sorted right = min(right).

    Step 3: If max(left) <= min(right), the joined result is fully sorted.
            Record this split index as valid.

    Step 4: Return the count of valid split indices.

  Prefix/Suffix: https://www.youtube.com/watch?v=xbYr9JOC2Lk
  
    Step 1: Build prefix_max where prefix_max[i] = max(A[0..i]).
            A single forward pass gives O(1) max(left) lookup for any split.

    Step 2: Build suffix_min where suffix_min[i] = min(A[i..N-1]).
            A single backward pass gives O(1) min(right) lookup for any split.

    Step 3: Try every valid split index i from 1 to N-1.
            A split at i is valid iff prefix_max[i-1] <= suffix_min[i].
            Record valid split indices.

    Step 4: Return the count of valid split indices.

COMPLEXITY:
-----------
  Brute Force — O(N² log N) time, O(N) space
    Time:  O(N² log N)
      - There are N-1 possible splits.
      - For each split, sorting left takes O(i log i) and right O((N-i) log(N-i)).
      - In the worst case this sums to O(N² log N) overall.

    Space: O(N)
      - sorted() creates a new list of up to N elements for each split.
      - The split_indexes result list holds at most N-1 entries.

  Prefix/Suffix — O(N) time, O(N) space
    Time:  O(N)
      - One forward pass to build prefix_max:  O(N).
      - One backward pass to build suffix_min: O(N).
      - One forward pass to check each split:  O(N).
      - Total: O(N).

    Space: O(N)
      - prefix_max and suffix_min each hold N values: O(N).
      - The split_indexes result list holds at most N-1 entries.

================================================================================
"""


def count_sorted_splits_brute_force(input: list[int]) -> list[int]:
    # Collect the valid split indexes (1-based split point, i.e. left = input[:i])
    split_indexes: list[int] = []

    # Step 1: Try every split index from 1 to N-1 so both halves are non-empty
    for index in range(1, len(input)):
        # Step 2: Sort each half independently
        left: list[int] = sorted(input[:index])
        right: list[int] = sorted(input[index:])

        n: int = len(left)

        # Guard: both halves must be non-empty (already guaranteed by the range,
        # but kept for clarity)
        if len(left) < 1 or len(right) < 1:
            continue

        # Step 3: The join is sorted iff the largest element in the left half
        # is <= the smallest element in the right half
        if left[n - 1] <= right[0]:
            split_indexes.append(index)

    # Step 4: Return all valid split indexes
    return split_indexes


def count_sorted_splits_prefix_suffix(input: list[int]) -> list[int]:
    # Collect the valid split indexes (1-based split point, i.e. left = input[:i])
    n: int = len(input)
    prefix_max: list[int] = [0] * n
    suffix_min: list[int] = [0] * n
    split_indexes: list[int] = []

    # Step 1: Build prefix_max where prefix_max[i] = max of input[0..i]
    # This lets us look up max(left half) in O(1) for any split index
    prefix_max[0] = input[0]
    for i in range(1, n):
        prefix_max[i] = max(prefix_max[i - 1], input[i])

    # Step 2: Build suffix_min where suffix_min[i] = min of input[i..n-1]
    # This lets us look up min(right half) in O(1) for any split index
    suffix_min[n - 1] = input[n - 1]
    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(suffix_min[i + 1], input[i])

    # Step 3: Try every split index from 1 to N-1 so both halves are non-empty.
    # The join is sorted iff the largest element in the left half
    # is <= the smallest element in the right half.
    # For a split at i: left = input[:i], right = input[i:]
    #   max(left) = prefix_max[i-1], min(right) = suffix_min[i]
    for i in range(1, n):
        if prefix_max[i - 1] <= suffix_min[i]:
            split_indexes.append(i)

    # Step 4: Return all valid split indexes
    return split_indexes


# ==================== TEST CASES ====================
TEST_CASES = [
    {
        "name": "Test 1: Example from problem — 2 valid splits",
        "input": [1, 3, 2, 4],
        "expected": 2,
    },
    {
        "name": "Test 2: Already sorted — every split is valid",
        "input": [1, 2, 3, 4],
        "expected": 3,
    },
    {
        "name": "Test 3: Reverse sorted — no split is valid",
        "input": [4, 3, 2, 1],
        "expected": 0,
    },
    {
        "name": "Test 4: Two elements, valid split",
        "input": [1, 2],
        "expected": 1,
    },
    {
        "name": "Test 5: Two elements, invalid split",
        "input": [2, 1],
        "expected": 0,
    },
    {
        "name": "Test 6: All equal elements — every split is valid",
        "input": [3, 3, 3, 3],
        "expected": 3,
    },
    {
        "name": "Test 7: One large element at the end",
        "input": [1, 2, 5, 3, 4, 6],
        "expected": 3,
    },
    {
        "name": "Test 8: Large jump in the middle blocks most splits",
        "input": [1, 2, 10, 3, 4],
        "expected": 2,
    },
    {
        "name": "Test 9: Duplicate values across the split boundary",
        "input": [1, 3, 3, 5],
        "expected": 3,
    },
    {
        "name": "Test 10: Single valid split in the middle",
        "input": [3, 1, 2, 4, 5],
        "expected": 2,
    },
]


def _run_tests(label: str, fn) -> tuple[int, int]:
    """Run TEST_CASES against the given function and return (passed, failed)."""
    passed = 0
    failed = 0

    print("=" * 70)
    print(f"RUNNING COUNT SORTED SPLITS TEST CASES — {label}")
    print("=" * 70)

    for test in TEST_CASES:
        result = len(fn(test["input"]))
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
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(TEST_CASES)} tests")
    print("=" * 70)

    return passed, failed


def run_tests():
    _run_tests("BRUTE FORCE", count_sorted_splits_brute_force)


def run_tests_prefix_suffix():
    _run_tests("PREFIX/SUFFIX", count_sorted_splits_prefix_suffix)


def solve():
    run_tests()
    print()
    run_tests_prefix_suffix()


solve()
