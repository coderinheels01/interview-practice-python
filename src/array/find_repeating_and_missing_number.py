"""Find the Repeating and Missing Number.

Given an integer array ``nums`` of size ``n`` containing values from ``1`` to
``n``, every value should appear exactly once except:

- One value, ``A``, appears twice.
- One value, ``B``, is missing.

Return ``[A, B]``, where the repeating value is at index 0 and the missing
value is at index 1.

Do not modify the original array.

Example 1:
    Input: nums = [3, 5, 4, 1, 1]
    Output: [1, 2]

    Explanation:
        1 appears twice, and 2 is missing.

Example 2:
    Input: nums = [1, 2, 3, 6, 7, 5, 7]
    Output: [7, 4]

    Explanation:
        7 appears twice, and 4 is missing.

Constraints:
    - n == len(nums)
    - 1 <= n <= 10^5
    - n - 2 values appear exactly once and are between 1 and n.
    - One value between 1 and n appears twice.
    - One value between 1 and n is missing.

    https://www.youtube.com/watch?v=2D0D8HE6uak&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=25
"""


def find_repeating_and_missing_number_brute_force(nums: list[int]) -> list[int]:
    """Return the repeating value followed by the missing value.

    Approach — Brute-Force Frequency Counting:
    1. Initialize a two-element result with sentinel values for the repeating
       and missing numbers.
    2. Consider every possible value from ``1`` through ``n`` as a candidate.
    3. For each candidate, scan the complete input and count how many times the
       candidate occurs.
    4. If its frequency is 2, store it as the repeating number. If its
       frequency is 0, store it as the missing number.
    5. Stop early once both required numbers have been found.
    6. Return ``[repeating_number, missing_number]``.

    Args:
        nums: An array of length ``n`` containing values from 1 through ``n``,
            with exactly one repeated value and one missing value.

    Returns:
        A two-element list containing the repeating value at index 0 and the
        missing value at index 1.

    Mutation:
        This function does not modify ``nums``.

    Assumptions:
        Exactly one value occurs twice, exactly one value is absent, and every
        input value is between 1 and ``len(nums)``.

    Time Complexity:
        O(n^2), where n is the length of ``nums``. There can be n candidate
        values, and determining each candidate's frequency can scan all n input
        values. The early exit can reduce work but does not change the worst
        case. This runtime is impractical for the maximum length of 10^5.

    Space Complexity:
        O(1) auxiliary space. The counters and fixed two-element result do not
        grow with the input size.
    """
    # 1. Initialize the input size and result sentinels.
    size: int = len(nums)
    result: list[int] = [-1] * 2

    # 2. Consider every allowed value as the repeating or missing candidate.
    for candidate_number in range(1, size + 1):
        # 3. Count this candidate's occurrences by scanning the complete input.
        frequency: int = 0
        for num in nums:
            if candidate_number == num:
                frequency += 1

        # 4. Record a repeated candidate or a missing candidate.
        if frequency == 2:
            result[0] = candidate_number
        elif frequency == 0:
            result[1] = candidate_number

        # 5. Stop once both answers have been discovered.
        if result[0] != -1 and result[1] != -1:
            break

    # 6. Return the repeating value followed by the missing value.
    return result


def find_repeating_and_missing_number_time_optimized(nums: list[int]) -> list[int]:
    """Return the repeating value followed by the missing value.

    Approach — Frequency Array:
    1. Create a frequency array of size ``n + 1`` so each valid value from 1
       through ``n`` can be used directly as an index. Index 0 is unused.
    2. Visit every value in ``nums`` and increase its frequency.
    3. Scan every valid value from 1 through ``n``.
    4. Store the value with frequency 2 at index 0 of the result because it is
       the repeating number.
    5. Store the value with frequency 0 at index 1 of the result because it is
       the missing number.
    6. Return ``[repeating_number, missing_number]``.

    Args:
        nums: An array of length ``n`` containing values from 1 through ``n``,
            with exactly one repeated value and one missing value.

    Returns:
        A two-element list containing the repeating value at index 0 and the
        missing value at index 1.

    Mutation:
        This function does not modify ``nums``.

    Assumptions:
        Exactly one value occurs twice, exactly one value is absent, and all
        input values are between 1 and ``len(nums)``.

    Time Complexity:
        O(n), where n is the length of ``nums``. One loop counts the n input
        values, and the second loop scans the n possible values.

    Space Complexity:
        O(n) auxiliary space for the frequency array of length ``n + 1``. The
        two-element result uses O(1) additional space.
    """

    # 1. Initialize the result and a frequency slot for every value from 1 to n.
    size: int = len(nums)
    result: list[int] = [-1] * 2
    frequency: list[int] = [0] * (size + 1)

    # 2. Count how many times each input value occurs.
    for num in nums:
        frequency[num] += 1

    # 3. Inspect every valid value from 1 through n.
    for num in range(1, len(frequency)):
        # 4. A frequency of 2 identifies the repeating value.
        if frequency[num] == 2:
            result[0] = num

        # 5. A frequency of 0 identifies the missing value.
        if frequency[num] == 0:
            result[1] = num

    # 6. Return the repeating value followed by the missing value.
    return result


def find_repeating_and_missing_number_optimized1(nums: list[int]) -> list[int]:
    """Return the repeating value followed by the missing value using algebra.

    Approach — Sum and Square-Sum Equations:
    1. Let ``M`` be the missing number and ``R`` be the repeating number.
       Calculate the actual array sum and the expected natural-number sum:

           expected_sum = n * (n + 1) / 2

       Because the array contains ``R`` instead of ``M``:

           expected_sum - actual_sum = M - R

    2. Calculate the actual square sum and the expected natural-number square
       sum:

           expected_square_sum = n * (n + 1) * (2n + 1) / 6

       Their difference produces a second equation:

           expected_square_sum - actual_square_sum = M^2 - R^2

    3. Apply the difference-of-squares identity:

           M^2 - R^2 = (M - R)(M + R)

       Dividing ``M^2 - R^2`` by the already known ``M - R`` gives ``M + R``.
    4. Solve the two equations:

           M - R = missing_minus_repeating
           M + R = missing_plus_repeating

       Adding them gives ``2M``, so:

           M = ((M - R) + (M + R)) / 2
           R = (M + R) - M

    5. Return ``[R, M]`` because the repeating number must come first.

    Args:
        nums: An array of length ``n`` containing values from 1 through ``n``,
            with exactly one repeated value and one missing value.

    Returns:
        A two-element list containing the repeating value at index 0 and the
        missing value at index 1.

    Mutation:
        This function does not modify ``nums``.

    Assumptions:
        Exactly one value occurs twice, exactly one value is absent, and every
        value is between 1 and ``len(nums)``. Thus ``M - R`` is nonzero.

    Time Complexity:
        O(n), where n is the length of ``nums``. Calculating the actual sum and
        square sum traverses the input; the remaining formulas take O(1) time.

    Space Complexity:
        O(1) auxiliary space. The square-sum generator produces one value at a
        time, and only a fixed number of integers are stored. Python integers
        avoid the fixed-width overflow risk of the square-sum formula.
    """
    # 1. Calculate the actual sum used to obtain M - R.
    array_length: int = len(nums)
    actual_sum: int = sum(nums)

    # 2. Calculate the actual square sum used to obtain M^2 - R^2.
    actual_square_sum: int = sum(number**2 for number in nums)

    # 1. Calculate the expected natural-number sum from 1 through n.
    expected_sum: int = array_length * (array_length + 1) // 2

    # 2. Calculate the expected natural-number square sum from 1 through n.
    expected_square_sum: int = (
        array_length * (array_length + 1) * (2 * array_length + 1) // 6
    )

    # 1. Subtract the actual sum from the expected sum to obtain M - R.
    missing_minus_repeating: int = expected_sum - actual_sum
    # 2. Subtract the square sums to obtain M^2 - R^2.
    missing_square_minus_repeating_square: int = expected_square_sum - actual_square_sum

    # 3. Use M^2 - R^2 = (M - R)(M + R) to calculate M + R.
    missing_plus_repeating: int = (
        missing_square_minus_repeating_square // missing_minus_repeating
    )

    # 4. Solve the two equations for the missing and repeating values.
    missing_number: int = (missing_minus_repeating + missing_plus_repeating) // 2
    repeating_number: int = missing_plus_repeating - missing_number

    # 5. Return the repeating number first and the missing number second.
    return [repeating_number, missing_number]


def find_repeating_and_missing_number_optimized2(nums: list[int]) -> list[int]:
    """Return the repeating value followed by the missing value using XOR.

    Approach — XOR Partitioning:
    1. XOR every array value with every expected value from 1 through ``n``.
       Values that appear once in both collections cancel because ``a ^ a = 0``.
       The remaining XOR is ``repeating_number ^ missing_number``.
    2. Find a bit that is set in the remaining XOR. The repeating and missing
       numbers differ at this bit, so it can separate them into two groups.
    3. Partition all values from ``nums`` by that bit and XOR each group.
    4. Partition all expected values from 1 through ``n`` using the same bit and
       XOR them into the corresponding groups. Equal values cancel within their
       groups, leaving the repeating and missing numbers as the two candidates.
    5. Count one candidate's occurrences in ``nums``. If it occurs twice, it is
       the repeating number; otherwise, the other candidate is repeating.
    6. Return the candidates in ``[repeating_number, missing_number]`` order.

    Args:
        nums: An array of length ``n`` containing values from 1 through ``n``,
            with exactly one repeated value and one missing value.

    Returns:
        A two-element list containing the repeating value at index 0 and the
        missing value at index 1.

    Mutation:
        This function does not modify ``nums``.

    Assumptions:
        Exactly one value occurs twice, exactly one value is absent, and every
        value is between 1 and ``len(nums)``. The repeating and missing numbers
        differ, so their XOR always has at least one set bit.

    Time Complexity:
        O(n), where n is the length of ``nums``. The function makes three
        linear passes over the input or the range 1 through n. Finding a set
        bit takes O(log n), which is dominated by the linear work.

    Space Complexity:
        O(1) auxiliary space. Only XOR accumulators, indices, a bit position,
        and a counter are stored.
    """

    # 1. XOR the actual and expected values, leaving repeating XOR missing.
    size: int = len(nums)
    xor_value: int = 0

    for index in range(size):
        xor_value ^= nums[index]
        xor_value ^= index + 1

    # 2. Find a bit where the repeating and missing candidates differ.
    bit_shift_number: int = 0

    while True:
        if (xor_value & (1 << bit_shift_number)) != 0:
            break
        bit_shift_number += 1

    # 3. Initialize groups for values with the selected bit unset or set.
    zero_group: int = 0
    one_group: int = 0

    # 3. Partition and XOR every value from the input array.
    for num in nums:
        if (num & (1 << bit_shift_number)) != 0:
            one_group ^= num
        else:
            zero_group ^= num

    # 4. Partition and XOR every expected value from 1 through n.
    for index in range(1, size + 1):
        if (index & (1 << bit_shift_number)) != 0:
            one_group ^= index
        else:
            zero_group ^= index

    # 5. Determine whether zero_group is the repeating or missing candidate.
    count: int = 0

    for num in nums:
        if num == zero_group:
            count += 1

    # 6. Return the repeating candidate first and the missing candidate second.
    return [zero_group, one_group] if count == 2 else [one_group, zero_group]


def solve() -> None:
    nums: list[int] = [3, 5, 4, 1, 1]

    expected: list[int] = [1, 2]
    result: list[int] = find_repeating_and_missing_number_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [1, 2, 3, 6, 7, 5, 7]

    expected: list[int] = [7, 4]
    result: list[int] = find_repeating_and_missing_number_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 5, 7, 1, 8, 6, 4, 3, 2]

    expected = [6, 9]
    result = find_repeating_and_missing_number_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1]

    expected = [1, 2]
    result = find_repeating_and_missing_number_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2]

    expected = [2, 1]
    result = find_repeating_and_missing_number_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 3, 3, 4]

    expected = [3, 2]
    result = find_repeating_and_missing_number_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 2, 3]

    expected = [2, 4]
    result = find_repeating_and_missing_number_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, 2, 4, 1, 5]

    expected = [5, 3]
    result = find_repeating_and_missing_number_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(1, 100_001))
    nums[-1] = 99_999

    expected = [99_999, 100_000]
    result = find_repeating_and_missing_number_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [3, 5, 4, 1, 1]

    expected: list[int] = [1, 2]
    result: list[int] = find_repeating_and_missing_number_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [1, 2, 3, 6, 7, 5, 7]

    expected: list[int] = [7, 4]
    result: list[int] = find_repeating_and_missing_number_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 5, 7, 1, 8, 6, 4, 3, 2]

    expected = [6, 9]
    result = find_repeating_and_missing_number_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1]

    expected = [1, 2]
    result = find_repeating_and_missing_number_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2]

    expected = [2, 1]
    result = find_repeating_and_missing_number_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 3, 3, 4]

    expected = [3, 2]
    result = find_repeating_and_missing_number_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 2, 3]

    expected = [2, 4]
    result = find_repeating_and_missing_number_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, 2, 4, 1, 5]

    expected = [5, 3]
    result = find_repeating_and_missing_number_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [3, 5, 4, 1, 1]

    expected: list[int] = [1, 2]
    result: list[int] = find_repeating_and_missing_number_optimized1(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [1, 2, 3, 6, 7, 5, 7]

    expected: list[int] = [7, 4]
    result: list[int] = find_repeating_and_missing_number_optimized1(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 5, 7, 1, 8, 6, 4, 3, 2]

    expected = [6, 9]
    result = find_repeating_and_missing_number_optimized1(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1]

    expected = [1, 2]
    result = find_repeating_and_missing_number_optimized1(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2]

    expected = [2, 1]
    result = find_repeating_and_missing_number_optimized1(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 3, 3, 4]

    expected = [3, 2]
    result = find_repeating_and_missing_number_optimized1(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 2, 3]

    expected = [2, 4]
    result = find_repeating_and_missing_number_optimized1(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, 2, 4, 1, 5]

    expected = [5, 3]
    result = find_repeating_and_missing_number_optimized1(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(1, 100_001))
    nums[-1] = 99_999

    expected = [99_999, 100_000]
    result = find_repeating_and_missing_number_optimized1(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [3, 5, 4, 1, 1]

    expected: list[int] = [1, 2]
    result: list[int] = find_repeating_and_missing_number_optimized2(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [1, 2, 3, 6, 7, 5, 7]

    expected: list[int] = [7, 4]
    result: list[int] = find_repeating_and_missing_number_optimized2(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 5, 7, 1, 8, 6, 4, 3, 2]

    expected = [6, 9]
    result = find_repeating_and_missing_number_optimized2(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1]

    expected = [1, 2]
    result = find_repeating_and_missing_number_optimized2(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2]

    expected = [2, 1]
    result = find_repeating_and_missing_number_optimized2(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 3, 3, 4]

    expected = [3, 2]
    result = find_repeating_and_missing_number_optimized2(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 2, 3]

    expected = [2, 4]
    result = find_repeating_and_missing_number_optimized2(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, 2, 4, 1, 5]

    expected = [5, 3]
    result = find_repeating_and_missing_number_optimized2(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(1, 100_001))
    nums[-1] = 99_999

    expected = [99_999, 100_000]
    result = find_repeating_and_missing_number_optimized2(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
