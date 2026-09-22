"""60. Permutation Sequence

The set [1, 2, 3, ..., n] contains a total of n! unique permutations.

By listing and labeling all of the permutations in order, we get the following
sequence for n = 3:
    1. "123"
    2. "132"
    3. "213"
    4. "231"
    5. "312"
    6. "321"

Given n and k, return the kth permutation sequence as a string.
The position k is one-based: k = 1 selects the first permutation.

Example 1:
    Input: n = 3, k = 3
    Output: "213"

Example 2:
    Input: n = 4, k = 9
    Output: "2314"

Example 3:
    Input: n = 3, k = 1
    Output: "123"

Constraints:
    Numeric constraints are not shown in the provided screenshot.
"""

import math


def permutation_sequence(n: int, k: int) -> str:
    """Return the kth lexicographic permutation of the numbers 1 through n.

    Args:
        n: Number of distinct digits, with 1 <= n <= 9.
        k: One-based position in sorted permutation order, with 1 <= k <= n!.

    Returns:
        A string containing each digit from 1 through n exactly once.
        Inputs are assumed valid and are not modified. All working lists
        are created locally; the function does not generate every permutation.

    Approach:
        Factorial Number System (factoradic) permutation unranking.
        1. Create a sorted list of available numbers and an empty result list.
           Convert k to a zero-based rank by subtracting one, so rank zero
           selects the first permutation.
        2. Calculate n! once. With m numbers remaining, there are m! possible
           orders, grouped into m buckets according to their first number.
           Each bucket contains m! / m = (m - 1)! orders of the other numbers.
        3. While more than one number remains, divide the current permutation
           count by the number of available numbers to get rows_per_bucket.
           Divide the zero-based rank by this bucket size to find bucket_index.
        4. Remove the number at bucket_index and append it to kth_permutation.
           Removing it prevents reuse and preserves the order of the others.
        5. Take the rank modulo rows_per_bucket to find the rank within the
           selected bucket. Set permutation to rows_per_bucket: this is the
           permutation count for the remaining numbers. Repeat from step 3.
        6. Append the last remaining number, then convert the integers to
           strings and join them into the answer. For n = 1, the loop is
           skipped and this step returns "1".

        Walkthrough: n = 4, k = 9
            Start: nums = [1, 2, 3, 4], new_k = 8, permutation = 24.
            - 24 / 4 = 6 orders per bucket. 8 // 6 = 1 selects 2.
              Remaining nums = [1, 3, 4], new_k = 8 % 6 = 2.
            - 6 / 3 = 2 orders per bucket. 2 // 2 = 1 selects 3.
              Remaining nums = [1, 4], new_k = 2 % 2 = 0.
            - 2 / 2 = 1 order per bucket. 0 // 1 = 0 selects 1.
              Remaining nums = [4], new_k = 0.
            Append 4 and join [2, 3, 1, 4] to return "2314".

    Time Complexity:
        O(n**2), using constant-cost arithmetic for the small integers allowed
        by the constraints. There are n - 1 loop iterations. Removing a number
        with pop(bucket_index) can shift every later number, taking O(n) time
        per iteration in the worst case. These shifts total O(n**2).

        For example, when k = 1, each selection removes the first number:
            [1, 2, 3, 4] -> remove 1 -> shift 3 elements
            [2, 3, 4]    -> remove 2 -> shift 2 elements
            [3, 4]       -> remove 3 -> shift 1 element

        For n numbers, the total shifts in this worst case are:
            (n - 1) + (n - 2) + ... + 1
            = n * (n - 1) / 2
            = (n**2 - n) / 2
        Ignoring constant factors and the lower-order term gives O(n**2).
        Although there is only one loop, pop() does additional work inside it.

        Factorial is computed once and reused through division. Creating nums
        and converting/joining the n single-digit numbers take O(n) time.

    Space Complexity:
        O(n), including the output string.
        1. nums and kth_permutation use O(n) space. During the loop, each
           number removed from nums is added to kth_permutation, so together
           they hold n numbers. For n = 4, k = 9:
               nums            kth_permutation
               [1, 2, 3, 4]    []                 -> 4 numbers total
               [1, 3, 4]       [2]                -> 4 numbers total
               [1, 4]          [2, 3]             -> 4 numbers total
               [4]             [2, 3, 1]          -> 4 numbers total
           Appending the final number leaves an extra reference in nums,
           making n + 1 references in total. This is still O(n). Any spare
           capacity allocated by the lists also fits within O(n) space.
        2. Converting the numbers to strings and joining them uses O(n) space.
           Each number is a single digit under the constraints, so the output
           has n characters. For example, "2314" has four characters. The
           temporary digit strings used by join also fit within O(n) space.
        3. The remaining scalar variables use O(1) space under the problem's
           small numeric constraints. There is no recursion stack.

        Total: O(n) + O(n) + O(1) = O(n).
        The function stores one permutation, not all n! permutations.
    """
    # 1. Prepare sorted choices and convert k to a zero-based rank.
    nums: list[int] = list(range(1, n + 1))
    kth_permutation: list[str] = []
    new_k: int = k - 1

    # 2. Compute the initial permutation count once.
    permutation: int = math.factorial(n)

    while len(nums) > 1:
        # 3. Determine the bucket size and which bucket contains the rank.
        numbers_of_buckets: int = len(nums)
        rows_per_bucket: int = permutation // numbers_of_buckets
        bucket_index: int = new_k // rows_per_bucket
        # 4. Select the next number and remove it from the available choices.
        kth_permutation.append(str(nums.pop(bucket_index)))
        # 5. Continue with the rank and permutation count inside this bucket.
        new_k = new_k % rows_per_bucket
        permutation = rows_per_bucket

    # 6. Append the only remaining number and build the answer string.
    kth_permutation.append(str(nums[0]))

    return "".join(kth_permutation)


def solve() -> None:
    n: int = 3
    k: int = 3
    expected: str = "213"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 1, k = 1
    n: int = 1
    k: int = 1
    expected: str = "1"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 2, k = 1
    n: int = 2
    k: int = 1
    expected: str = "12"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 2, k = 2
    n: int = 2
    k: int = 2
    expected: str = "21"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 3, k = 1
    n: int = 3
    k: int = 1
    expected: str = "123"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 3, k = 2
    n: int = 3
    k: int = 2
    expected: str = "132"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 3, k = 3
    n: int = 3
    k: int = 3
    expected: str = "213"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 3, k = 4
    n: int = 3
    k: int = 4
    expected: str = "231"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 3, k = 5
    n: int = 3
    k: int = 5
    expected: str = "312"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 3, k = 6
    n: int = 3
    k: int = 6
    expected: str = "321"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 4, k = 9
    n: int = 4
    k: int = 9
    expected: str = "2314"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 4, k = 6
    n: int = 4
    k: int = 6
    expected: str = "1432"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 4, k = 7
    n: int = 4
    k: int = 7
    expected: str = "2134"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 4, k = 12
    n: int = 4
    k: int = 12
    expected: str = "2431"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 4, k = 13
    n: int = 4
    k: int = 13
    expected: str = "3124"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 4, k = 24
    n: int = 4
    k: int = 24
    expected: str = "4321"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 5, k = 42
    n: int = 5
    k: int = 42
    expected: str = "24531"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 6, k = 360
    n: int = 6
    k: int = 360
    expected: str = "365421"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 9, k = 1
    n: int = 9
    k: int = 1
    expected: str = "123456789"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 9, k = 40320
    n: int = 9
    k: int = 40320
    expected: str = "198765432"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 9, k = 40321
    n: int = 9
    k: int = 40321
    expected: str = "213456789"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 9, k = 181440
    n: int = 9
    k: int = 181440
    expected: str = "549876321"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # n = 9, k = 362880
    n: int = 9
    k: int = 362880
    expected: str = "987654321"
    result: str = permutation_sequence(n, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
