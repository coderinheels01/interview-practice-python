r"""
================================================================================
                MINIMUM ABSOLUTE SUM AFTER ONE SIGN FLIP
================================================================================

PROBLEM:
--------
There is an array A consisting of N integers. You may choose AT MOST ONE
element to multiply by -1. Your goal is to make the sum of elements as
close to 0 as possible.

Return the minimum absolute value of the sum that can be obtained.

FUNCTION SIGNATURE:
-------------------
  int solution(vector<int> &A)

EXAMPLES:
---------
  Example 1: A = [1, 3, 2, 5]
    Original sum = 11
    Best flip: 5 → -5, new sum = 1
    Output: 1

  Example 2: A = [-4, 0, -3, -3]
    Original sum = -10
    Best flip: -4 → 4, new sum = -2
    Output: 2

  Example 3: A = [4, -3, 5, -7]
    Original sum = -1
    No flip improves it (any flip makes it worse or equal)
    Output: 1

  Example 4: A = [-15, 18, -1, -1, 10, -22]
    Original sum = -11
    Best flip: -1 → 1, new sum = -9
    Output: 9

CONSTRAINTS:
------------
  - 1 ≤ N ≤ 100,000
  - Each element of A is an integer within the range [-1,000, 1,000]

COMPLEXITY:
-----------
  Time:  O(N)
    - One pass to compute the total sum: O(N)
    - One pass to try flipping each element: O(N)
    - All other operations (abs, min, multiply) are O(1) per element
    - Total: O(N) + O(N) = O(N)

  Space: O(1)
    - Only a fixed number of variables are used (total, best, flipped_n,
      flipped_sum) regardless of input size
    - No extra data structures are allocated

ALGORITHM:
----------
The key insight: when you flip element n (multiply by -1), the sum changes by
exactly 2 * (-n), because you remove n and add -n:

  new_sum = total - n + (-n) = total - 2n

So the change is:  flipped_sum = total + (2 * flipped_n)
                              = total + (2 * (-n))
                              = total - 2n

Step 1: Compute the original total sum.
Step 2: Track the best (minimum absolute) result, starting with abs(total)
        in case no flip helps.
Step 3: For each element n, simulate flipping it:
          flipped_n   = n * -1
          flipped_sum = total + (2 * flipped_n)
        Update best if abs(flipped_sum) < best.
Step 4: Return best.

WALKTHROUGH — Example 1: A = [1, 3, 2, 5]
------------------------------------------
  total = 1 + 3 + 2 + 5 = 11
  best  = abs(11) = 11   ← baseline (no flip)

  Flip n=1:  flipped_n=-1,  flipped_sum = 11 + 2*(-1)  = 9   → best=9
  Flip n=3:  flipped_n=-3,  flipped_sum = 11 + 2*(-3)  = 5   → best=5
  Flip n=2:  flipped_n=-2,  flipped_sum = 11 + 2*(-2)  = 7   → best=5
  Flip n=5:  flipped_n=-5,  flipped_sum = 11 + 2*(-5)  = 1   → best=1

  Return 1 ✓

WALKTHROUGH — Example 2: A = [-4, 0, -3, -3]
---------------------------------------------
  total = -4 + 0 + -3 + -3 = -10
  best  = abs(-10) = 10

  Flip n=-4: flipped_n=4,  flipped_sum = -10 + 2*(4)  = -2  → best=2
  Flip n=0:  flipped_n=0,  flipped_sum = -10 + 2*(0)  = -10 → best=2
  Flip n=-3: flipped_n=3,  flipped_sum = -10 + 2*(3)  = -4  → best=2
  Flip n=-3: flipped_n=3,  flipped_sum = -10 + 2*(3)  = -4  → best=2

  Return 2 ✓

================================================================================
"""


def minimum_absolute_sum_after_one_sign_flip(input: list[int]) -> int | None:
    # Edge case: empty array has no sum to compute
    if not input:
        return None

    # Step 1: Compute the original sum of all elements
    total: int = sum(input)

    # Step 2: Baseline — the absolute sum if we flip nothing
    best: int = abs(total)

    # Step 3: Try flipping each element one at a time
    for index, n in enumerate(input):
        # Multiply the chosen element by -1
        flipped_n: int = n * -1

        # The new sum after flipping: remove n, add flipped_n
        # new_sum = total - n + flipped_n = total + 2 * flipped_n
        flipped_sum: int = total + (2 * flipped_n)

        # Keep track of the smallest absolute sum seen so far
        best = min(best, abs(flipped_sum))

    # Step 4: Return the minimum absolute sum achievable
    return best


# ==================== TEST CASES ====================
def run_tests():
    test_cases = [
        {
            "name": "Test 1: Basic positive array — flip largest",
            "input": [1, 3, 2, 5],
            "expected": 1,
        },
        {
            "name": "Test 2: All negatives — flip most negative",
            "input": [-4, 0, -3, -3],
            "expected": 2,
        },
        {
            "name": "Test 3: Mixed signs — no flip improves result",
            "input": [4, -3, 5, -7],
            "expected": 1,
        },
        {
            "name": "Test 4: Larger mixed array",
            "input": [-15, 18, -1, -1, 10, -22],
            "expected": 9,
        },
        {
            "name": "Test 5: Already zero sum — any flip makes it worse",
            "input": [3, -3],
            "expected": 0,
        },
        {
            "name": "Test 6: Empty list returns None",
            "input": [],
            "expected": None,
        },
        {
            "name": "Test 7: Single positive element — flip gives same abs",
            "input": [5],
            "expected": 5,
        },
        {
            "name": "Test 8: Single negative element — flip gives same abs",
            "input": [-7],
            "expected": 7,
        },
        {
            "name": "Test 9: Large values",
            "input": [100, -99],
            "expected": 1,
        },
        {
            "name": "Test 10: All same positive values",
            "input": [4, 4, 4],
            "expected": 4,
        },
        {
            "name": "Test 11: Flip reduces sum exactly to zero",
            "input": [10, -3, -3, -4],
            "expected": 0,
        },
        {
            "name": "Test 12: All positives — flip largest halves the gap",
            "input": [1, 2, 3],
            "expected": 0,
        },
    ]

    passed = 0
    failed = 0

    print("=" * 70)
    print("RUNNING MINIMUM ABSOLUTE SUM AFTER ONE SIGN FLIP TEST CASES")
    print("=" * 70)

    for test in test_cases:
        result = minimum_absolute_sum_after_one_sign_flip(test["input"])
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


def solve():
    run_tests()


solve()
