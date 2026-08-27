"""Count Subarrays with Given XOR K.

Given an array of integers ``nums`` and an integer ``k``, return the total
number of subarrays whose XOR equals ``k``.

A subarray is a contiguous, non-empty section of an array.

Example 1:
    Input: nums = [4, 2, 2, 6, 4], k = 6
    Output: 4

    Explanation:
        The subarrays whose XOR equals 6 are:
        [4, 2], [4, 2, 2, 6, 4], [2, 2, 6], and [6].

Example 2:
    Input: nums = [5, 6, 7, 8, 9], k = 5
    Output: 2

    Explanation:
        The subarrays whose XOR equals 5 are [5] and [5, 6, 7, 8, 9].

Constraints:
    - 1 <= nums.length <= 10^5
    - 1 <= nums[i] <= 10^9
    - 1 <= k <= 10^9

https://www.youtube.com/watch?v=eZr-6p0B7ME&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=22

"""


def count_subarrays_with_given_xor_k_brute_force(nums: list[int], k: int) -> int:
    """Count contiguous, non-empty subarrays whose XOR equals ``k``.

    Approach — Brute-Force Subarray Enumeration:
    1. Initialize a counter for the number of matching subarrays.
    2. Choose every possible starting index for a subarray.
    3. For each starting index, choose every possible ending index at or after
       it. Together, these two indices describe one contiguous subarray.
    4. Reset the XOR to zero and visit every element between the selected start
       and end indices, combining the values with the XOR operator.
    5. If the completed subarray XOR equals ``k``, increase the match counter.
    6. Return the total number of matching subarrays.

    Args:
        nums: The integers from which contiguous subarrays are formed.
        k: The XOR value each counted subarray must produce.

    Returns:
        The number of contiguous, non-empty subarrays whose XOR equals ``k``.

    Mutation:
        This function does not modify ``nums``.

    Assumptions:
        The input follows the problem constraints: ``nums`` is non-empty, and
        its elements and ``k`` are positive integers.

    Time Complexity:
        O(n^3), where n is the length of ``nums``. The first two loops generate
        O(n^2) start-and-end index pairs, and the third loop can traverse O(n)
        elements to recalculate each subarray's XOR from scratch. This cubic
        runtime is not practical for the maximum constraint of 10^5 elements.

    Space Complexity:
        O(1) auxiliary space. The function uses only index, XOR, size, and
        counter variables regardless of the input size.
    """
    # 1. Store the input size and initialize the number of matches.
    size: int = len(nums)
    count: int = 0

    # 2. Choose every possible starting index.
    for first_index in range(size):
        # 3. Choose every possible ending index for the current start.
        for second_index in range(first_index, size):
            # 4. Recalculate this subarray's XOR from its start through its end.
            xor_value: int = 0
            for third_index in range(first_index, second_index + 1):
                xor_value ^= nums[third_index]

            # 5. Count the subarray when its XOR matches k.
            if xor_value == k:
                count += 1

    # 6. Return the total number of matching subarrays.
    return count


def count_subarrays_with_given_xor_k_time_optimized(nums: list[int], k: int) -> int:
    """Count contiguous, non-empty subarrays whose XOR equals ``k``.

    Approach — Incremental XOR Subarray Enumeration:
    1. Initialize a counter for the number of matching subarrays.
    2. Choose every possible starting index and reset the running XOR to zero
       for the new group of subarrays beginning at that index.
    3. Move the ending index from the starting index to the end of the array.
    4. Extend the current subarray by XORing the new ending value into the
       running XOR. This reuses the previous result instead of traversing the
       entire subarray again.
    5. Increase the counter whenever the running XOR equals ``k``.
    6. Return the total number of matching subarrays.

    Args:
        nums: The integers from which contiguous subarrays are formed.
        k: The XOR value each counted subarray must produce.

    Returns:
        The number of contiguous, non-empty subarrays whose XOR equals ``k``.

    Mutation:
        This function does not modify ``nums``.

    Assumptions:
        The input follows the problem constraints: ``nums`` is non-empty, and
        its elements and ``k`` are positive integers.

    Time Complexity:
        O(n^2), where n is the length of ``nums``. The outer loop chooses each
        starting index, and the inner loop visits every possible ending index
        for that start. Updating the running XOR takes O(1) time. Although this
        improves upon the O(n^3) brute-force version, quadratic time is still
        impractical for the maximum constraint of 10^5 elements.

    Space Complexity:
        O(1) auxiliary space. Only the size, counter, indices, and running XOR
        are stored, regardless of the input length.
    """
    # 1. Store the input size and initialize the number of matches.
    size: int = len(nums)
    count: int = 0

    # 2. Choose each starting index and reset its running XOR.
    for first_index in range(size):
        xor_value: int = 0

        # 3. Extend the ending index through the rest of the array.
        for second_index in range(first_index, size):
            # 4. Include the new ending value in the current subarray's XOR.
            xor_value ^= nums[second_index]

            # 5. Count the current subarray when its XOR matches k.
            if xor_value == k:
                count += 1

    # 6. Return the total number of matching subarrays.
    return count


def count_subarrays_with_given_xor_k_optimized(nums: list[int], k: int) -> int:
    """Count contiguous, non-empty subarrays whose XOR equals ``k``.

    Approach — Prefix XOR with a Frequency Map:
    1. Create a frequency map of prefix XOR values. Initialize XOR 0 with a
       frequency of 1 to represent the empty prefix before the array begins.
       This makes it possible to count matching subarrays that start at index 0.
    2. Visit each number once and include it in the current prefix XOR.
    3. Calculate the previous prefix XOR required to form a subarray with XOR
       ``k`` using ``required_prefix_xor = current_prefix_xor ^ k``. This comes
       from the identity ``current_prefix_xor ^ previous_prefix_xor = k``.
    4. Add the required prefix XOR's recorded frequency to the answer because
       every occurrence represents a different matching subarray ending at the
       current position.
    5. Record the current prefix XOR in the frequency map so later positions
       can use it as the beginning boundary of a subarray.
    6. Return the total number of matching subarrays.

    Args:
        nums: The integers from which contiguous subarrays are formed.
        k: The XOR value each counted subarray must produce.

    Returns:
        The number of contiguous, non-empty subarrays whose XOR equals ``k``.

    Mutation:
        This function does not modify ``nums``.

    Assumptions:
        The input follows the problem constraints: ``nums`` is non-empty, and
        its elements and ``k`` are positive integers.

    Time Complexity:
        O(n) expected time, where n is the length of ``nums``. The function
        traverses the array once, and each dictionary lookup and update takes
        O(1) expected time.

    Space Complexity:
        O(n) auxiliary space. In the worst case, every prefix produces a
        different XOR value that must be stored in the frequency map.
    """
    # 1. Record the empty prefix XOR once and initialize the answer and running
    # prefix XOR.
    prev_subarray_xors: dict[int, int] = {0: 1}
    count: int = 0
    current_xor_value: int = 0

    # 2. Visit each number and extend the current prefix XOR.
    for num in nums:
        current_xor_value ^= num

        # 3. Find the earlier prefix XOR needed to produce XOR k.
        prev_subarray_xor: int = current_xor_value ^ k

        # 4. Count every occurrence of that required earlier prefix.
        if prev_subarray_xor in prev_subarray_xors:
            count += prev_subarray_xors.get(prev_subarray_xor, 0)

        # 5. Record this prefix XOR for subarrays ending at later positions.
        prev_subarray_xors[current_xor_value] = (
            prev_subarray_xors.get(current_xor_value, 0) + 1
        )

    # 6. Return the total number of matching subarrays.
    return count


def solve() -> None:
    nums: list[int] = [4, 2, 2, 6, 4]
    k: int = 6

    expected: int = 4
    result: int = count_subarrays_with_given_xor_k_brute_force(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [5, 6, 7, 8, 9]
    k: int = 5

    expected: int = 2
    result: int = count_subarrays_with_given_xor_k_brute_force(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, 2, 9]
    k = 7

    expected = 1
    result = count_subarrays_with_given_xor_k_brute_force(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]
    k = 1

    expected = 1
    result = count_subarrays_with_given_xor_k_brute_force(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]
    k = 2

    expected = 0
    result = count_subarrays_with_given_xor_k_brute_force(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [4, 4, 4, 4]
    k = 4

    expected = 6
    result = count_subarrays_with_given_xor_k_brute_force(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 4]
    k = 8

    expected = 0
    result = count_subarrays_with_given_xor_k_brute_force(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 1, 6]
    k = 6

    expected = 2
    result = count_subarrays_with_given_xor_k_brute_force(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1_000_000_000]
    k = 1_000_000_000

    expected = 1
    result: int = count_subarrays_with_given_xor_k_brute_force(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [4, 2, 2, 6, 4]
    k: int = 6

    expected: int = 4
    result: int = count_subarrays_with_given_xor_k_time_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [5, 6, 7, 8, 9]
    k: int = 5

    expected: int = 2
    result: int = count_subarrays_with_given_xor_k_time_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, 2, 9]
    k = 7

    expected = 1
    result = count_subarrays_with_given_xor_k_time_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]
    k = 1

    expected = 1
    result = count_subarrays_with_given_xor_k_time_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]
    k = 2

    expected = 0
    result = count_subarrays_with_given_xor_k_time_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1, 1]
    k = 1

    expected = 9
    result = count_subarrays_with_given_xor_k_time_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 4]
    k = 8

    expected = 0
    result = count_subarrays_with_given_xor_k_time_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 1, 6]
    k = 6

    expected = 2
    result = count_subarrays_with_given_xor_k_time_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1_000_000_000]
    k = 1_000_000_000

    expected = 1
    result = count_subarrays_with_given_xor_k_time_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [4, 2, 2, 6, 4]
    k: int = 6

    expected: int = 4
    result: int = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [5, 6, 7, 8, 9]
    k: int = 5

    expected: int = 2
    result: int = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, 2, 9]
    k = 7

    expected = 1
    result = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]
    k = 1

    expected = 1
    result = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]
    k = 2

    expected = 0
    result = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1, 1]
    k = 1

    expected = 9
    result = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 4]
    k = 8

    expected = 0
    result = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 1, 6]
    k = 6

    expected = 2
    result = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1_000_000_000]
    k = 1_000_000_000

    expected = 1
    result = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1] * 100_000
    k = 1

    expected = 2_500_050_000
    result = count_subarrays_with_given_xor_k_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
