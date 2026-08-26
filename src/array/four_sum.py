"""4 Sum

Given an integer array ``nums`` and an integer ``target``, return all
quadruplets ``[nums[a], nums[b], nums[c], nums[d]]`` such that:

- ``a``, ``b``, ``c``, and ``d`` are distinct valid indices of ``nums``.
- ``nums[a] + nums[b] + nums[c] + nums[d] == target``.

The solution must not contain duplicate quadruplets. One element may be part
of multiple quadruplets. The output and the values within each quadruplet may
be returned in any order.

Example 1:
    Input: nums = [1, -2, 3, 5, 7, 9], target = 7
    Output: [[-2, 1, 3, 5]]

    Explanation: The values at indices 1, 0, 2, and 3 add up to 7:
    -2 + 1 + 3 + 5 = 7.

Example 2:
    Input: nums = [7, -7, 1, 2, 14, 3], target = 9
    Output: []

    Explanation: No quadruplet adds up to 9.

Constraints:
    - 1 <= nums.length <= 200
    - -10^4 <= nums[i] <= 10^4
    - -10^4 <= target <= 10^4
"""


def four_sum_brute_force(nums: list[int], target: int) -> list[list[int]]:
    """Return all unique quadruplets whose values add up to ``target``.

    Approach: Brute-Force Enumeration
        Enumerate every possible combination of four distinct indices. Store
        matching value combinations in a set of sorted tuples so duplicate
        quadruplets produced by different index combinations are removed.

        1. Store the input size and create an empty set for unique matching
           quadruplets.
        2. Use four nested loops to choose indices in strictly increasing order:

               first_index < second_index < third_index < fourth_index

           This guarantees that all four indices are distinct and that each
           index combination is visited only once. Each loop stops early when
           too few elements remain to complete a quadruplet.
        3. Collect the four selected values in a list.
        4. Calculate the sum of those four values.
        5. When the sum equals ``target``, sort the four values, convert them to
           a tuple, and add the tuple to the set. Sorting gives equivalent value
           combinations the same representation, and the set removes repeats.
        6. Convert every stored tuple into a list for the required return type.
        7. Sort the outer result list to make the output deterministic. The
           problem allows any order, but deterministic ordering simplifies
           testing and comparison.
        8. Return all unique matching quadruplets.

    Parameters:
        nums: The integer array from which four distinct indices are selected.
        target: The required sum of each returned quadruplet.

    Returns:
        A new list containing every unique matching quadruplet. Each quadruplet
        and the outer result list are sorted in ascending order.

    Mutation:
        The input list is not modified. Sorting is performed only on newly
        created quadruplets and the new result list.

    Time Complexity:
        O(n^4 + q log q), where ``n`` is the length of ``nums`` and ``q`` is
        the number of unique matching quadruplets. The four nested loops examine
        O(n^4) index combinations. Sorting four values is O(1) because the size
        is fixed. Sorting the final ``q`` quadruplets costs O(q log q). This
        brute-force approach can be slow near the maximum input size of 200.

    Space Complexity:
        O(q) additional space for the set of unique tuple quadruplets. The
        returned nested list also uses O(q) space because each quadruplet has a
        fixed size of four.

    Assumptions:
        Values and ``target`` satisfy the problem constraints. If fewer than
        four values are provided, the function returns an empty list.

        https://www.youtube.com/watch?v=eD95WRfh81c&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=21
    """
    # 1. Store the input size and initialize the unique-result set.
    size: int = len(nums)
    result_set: set[tuple[int, int, int, int]] = set()

    # 2. Choose every strictly increasing combination of four distinct indices.
    for first_index in range(size - 3):
        for second_index in range(first_index + 1, size - 2):
            for third_index in range(second_index + 1, size - 1):
                for fourth_index in range(third_index + 1, size):
                    # 3. Collect the four selected values.
                    four_sum_list: list[int] = [
                        nums[first_index],
                        nums[second_index],
                        nums[third_index],
                        nums[fourth_index],
                    ]

                    # 4. Calculate the selected values' sum.
                    four_sum: int = sum(four_sum_list)

                    # 5. Store a canonical sorted tuple when the sum matches.
                    if four_sum == target:
                        result_set.add(tuple(sorted(four_sum_list)))

    # 6. Convert the unique tuple quadruplets into nested lists.
    result: list[list[int]] = [list(quadruplet) for quadruplet in result_set]

    # 7. Sort the outer list to produce deterministic output.
    result.sort()

    # 8. Return all unique matching quadruplets.
    return result


def four_sum_time_optimized(nums: list[int], target: int) -> list[list[int]]:
    """Return all unique quadruplets whose values add up to ``target``.

    Approach: Three Loops with Hash-Set Complement Lookup
        Fix the first two indices, then traverse possible third indices while a
        set remembers values visited earlier in that same traversal. Calculate
        the fourth value required to reach ``target`` and look it up in the set
        in expected O(1) time. This replaces the brute-force fourth loop.

        1. Store the input size and create a set for unique result quadruplets.
        2. Choose each possible first index while leaving room for three later
           indices.
        3. Choose each possible second index, then create a fresh
           ``seen_third_values`` set for that exact first/second pair. Resetting
           the set here prevents values from other index pairs from being
           incorrectly reused.
        4. Traverse each possible third index after the second index.
        5. Add the three selected values and calculate the fourth value needed
           to reach ``target``.
        6. If that required value is already in ``seen_third_values``, it came
           from an earlier third-loop index. Therefore all four selected indices
           are distinct. Sort the four values into a canonical tuple and add it
           to ``result_set`` so duplicate value quadruplets are removed.
        7. Add the current third value to the seen set after the lookup. It can
           then serve as the fourth value for a later third-loop position, but
           it cannot match itself during the current iteration.
        8. Convert the ``q`` unique tuples into lists and sort the outer list.
           Conversion costs O(q), and sorting costs O(q log q). The problem
           allows any order, but sorting produces deterministic output.
        9. Return all unique matching quadruplets.

    Parameters:
        nums: The integer array from which four distinct indices are selected.
        target: The required sum of every returned quadruplet.

    Returns:
        A new list containing all unique matching quadruplets. Each quadruplet
        and the outer result list are sorted in ascending order.

    Mutation:
        The input list is not modified. Only newly created quadruplets and the
        new result list are sorted.

    Time Complexity:
        O(n^3 + q log q), where ``n`` is the length of ``nums`` and ``q`` is
        the number of unique matching quadruplets. The three nested loops
        examine O(n^3) index combinations, and hash-set operations take O(1)
        expected time. Sorting four values is O(1) because their count is fixed.
        Converting the final set costs O(q), and sorting its ``q`` quadruplets
        costs O(q log q).

    Space Complexity:
        O(n + q) additional space. ``seen_third_values`` can store O(n) values
        for one first/second pair, and ``result_set`` stores ``q`` unique
        quadruplets. The returned nested list also uses O(q) output space.

    Assumptions:
        Values and ``target`` satisfy the stated constraints. When fewer than
        four values are provided, the loops do not execute and the function
        returns an empty list.
    """
    # 1. Store the input size and initialize the unique-result set.
    size: int = len(nums)
    result_set: set[tuple[int, int, int, int]] = set()

    # 2. Choose each possible first index.
    for first_index in range(size - 3):
        # 3. Choose the second index and reset the per-pair seen set.
        for second_index in range(first_index + 1, size - 2):
            seen_third_values: set[int] = set()

            # 4. Traverse every possible third index after the second.
            for third_index in range(second_index + 1, size):
                # 5. Calculate the fourth value required to reach the target.
                three_sum: int = (
                    nums[first_index] + nums[second_index] + nums[third_index]
                )
                fourth_num: int = target - three_sum

                # 6. Store a canonical quadruplet when the complement was seen.
                if fourth_num in seen_third_values:
                    four_sum_tuple: tuple[int, int, int, int] = tuple(
                        sorted(
                            [
                                nums[first_index],
                                nums[second_index],
                                nums[third_index],
                                fourth_num,
                            ],
                        )
                    )
                    result_set.add(four_sum_tuple)

                # 7. Record this third value for later third-loop positions.
                seen_third_values.add(nums[third_index])

    # 8. Convert unique tuples to lists and sort the q results deterministically.
    result: list[list[int]] = sorted([list(quadruplet) for quadruplet in result_set])

    # 9. Return all unique matching quadruplets.
    return result


def four_sum_optimized(nums: list[int], target: int) -> list[list[int]]:
    """Return every unique quadruplet whose values add up to ``target``.

    Approach — Sorting and Two Pointers:
    1. Sort ``nums`` so duplicate values are adjacent and pointer movement can
       be based on whether the current sum is too small or too large.
    2. Fix the first value of a quadruplet. Skip it when it is the same as the
       previous first value so the same quadruplet is not produced again.
    3. Fix the second value after the first value and similarly skip duplicate
       second values used with the current first value.
    4. Place two pointers after the second value: one at the beginning of the
       remaining range and one at the end.
    5. Calculate the sum of the four selected values. When it equals the
       target, save the quadruplet and move both pointers inward.
    6. After a match, move past repeated values at both pointers. If the sum is
       too small, move only the left pointer right; if it is too large, move
       only the right pointer left.
    7. Return the unique quadruplets. Because the array is sorted and indices
       always move forward, every returned quadruplet is in ascending order.

    Args:
        nums: Integers from which four distinct indices must be selected.
        target: Required sum of the four selected values.

    Returns:
        A list containing each unique matching quadruplet. Returns an empty
        list when fewer than four values exist or no quadruplet matches.

    Mutation:
        Sorts ``nums`` in place, so the caller's list is modified.

    Assumptions:
        A value may be used more than once only when it occurs at multiple
        distinct indices. Python integers avoid fixed-width overflow.

    Time Complexity:
        O(n^3), where n is the number of values. Sorting costs O(n log n), and
        the two fixed-index loops combined with the linear two-pointer scan
        cost O(n^3), which dominates the sorting cost.

    Space Complexity:
        O(n + q), where q is the total number of integers stored in the output.
        Python's in-place Timsort can use O(n) temporary memory, while the
        returned quadruplets use O(q). Apart from sorting and the output, the
        algorithm uses O(1) additional space.
    """
    # 1. Prepare the output and sort the input for duplicate handling and
    # directional two-pointer movement.
    size: int = len(nums)
    result: list[list[int]] = []
    nums.sort()

    # 2. Fix the first value and skip repeated first values.
    for first_index in range(size - 3):
        if first_index > 0 and nums[first_index] == nums[first_index - 1]:
            continue

        # 3. Fix the second value and skip its duplicates for this first value.
        for second_index in range(first_index + 1, size - 2):
            if (
                second_index > first_index + 1
                and nums[second_index] == nums[second_index - 1]
            ):
                continue

            # 4. Scan the remaining range using inward-moving pointers.
            third_index: int = second_index + 1
            fourth_index: int = size - 1

            while third_index < fourth_index:
                # 5. Calculate the sum represented by the four current indices.
                four_sum: int = (
                    nums[first_index]
                    + nums[second_index]
                    + nums[third_index]
                    + nums[fourth_index]
                )

                if four_sum == target:
                    # 5. Save a match, then move both pointers inward.
                    result.append(
                        [
                            nums[first_index],
                            nums[second_index],
                            nums[third_index],
                            nums[fourth_index],
                        ]
                    )

                    third_index += 1
                    fourth_index -= 1

                    # 6. Skip duplicate third and fourth values after a match.
                    while (
                        third_index < fourth_index
                        and nums[third_index] == nums[third_index - 1]
                    ):
                        third_index += 1
                    while (
                        third_index < fourth_index
                        and nums[fourth_index] == nums[fourth_index + 1]
                    ):
                        fourth_index -= 1
                elif four_sum < target:
                    # 6. Increase a sum that is smaller than the target.
                    third_index += 1
                else:
                    # 6. Decrease a sum that is larger than the target.
                    fourth_index -= 1

    # 7. Return all unique matching quadruplets.
    return result


def solve() -> None:
    nums: list[int] = [1, -2, 3, 5, 7, 9]
    target: int = 7

    expected: list[list[int]] = [[-2, 1, 3, 5]]
    result: list[list[int]] = four_sum_brute_force(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 0, -1, 0, -2, 2]
    target = 0

    expected = [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
    result = sorted(four_sum_brute_force(nums, target))
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 2, 2, 2]
    target = 8

    expected = [[2, 2, 2, 2]]
    result = four_sum_brute_force(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7, -7, 1, 2, 14, 3]
    target = 9

    expected = []
    result = four_sum_brute_force(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]
    target = 1

    expected = []
    result = four_sum_brute_force(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    target = 6

    expected = []
    result = four_sum_brute_force(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 0, 0]
    target = 0

    expected = [[0, 0, 0, 0]]
    result = four_sum_brute_force(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -10_000, 10_000, 10_000]
    target = 0

    expected = [[-10_000, -10_000, 10_000, 10_000]]
    result = four_sum_brute_force(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, 0, 10_000, 10_000]
    target = 10_000

    expected = [[-10_000, 0, 10_000, 10_000]]
    result = four_sum_brute_force(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -10_000, 0, 10_000]
    target = -10_000

    expected = [[-10_000, -10_000, 0, 10_000]]
    result = four_sum_brute_force(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, -2, 3, 5, 7, 9]
    target = 7

    expected = [[-2, 1, 3, 5]]
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 0, -1, 0, -2, 2]
    target = 0

    expected = [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 2, 2, 2]
    target = 8

    expected = [[2, 2, 2, 2]]
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7, -7, 1, 2, 14, 3]
    target = 9

    expected = []
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]
    target = 1

    expected = []
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    target = 6

    expected = []
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 0, 0]
    target = 0

    expected = [[0, 0, 0, 0]]
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -10_000, 10_000, 10_000]
    target = 0

    expected = [[-10_000, -10_000, 10_000, 10_000]]
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, 0, 10_000, 10_000]
    target = 10_000

    expected = [[-10_000, 0, 10_000, 10_000]]
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -10_000, 0, 10_000]
    target = -10_000

    expected = [[-10_000, -10_000, 0, 10_000]]
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0] * 200
    target = 0

    expected = [[0, 0, 0, 0]]
    result = four_sum_time_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 0, -1, 0, -2, 2]
    target = 0

    expected = [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 2, 2, 2]
    target = 8

    expected = [[2, 2, 2, 2]]
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4]
    target = 100

    expected = []
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]
    target = 1

    expected = []
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    target = 6

    expected = []
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -10_000, 10_000, 10_000]
    target = 0

    expected = [[-10_000, -10_000, 10_000, 10_000]]
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-5, -4, -3, -2, -1]
    target = -14

    expected = [[-5, -4, -3, -2]]
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 0, 0, 0]
    target = 0

    expected = [[0, 0, 0, 0]]
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-3, -2, -1, 0, 0, 1, 2, 3]
    target = 0

    expected = [
        [-3, -2, 2, 3],
        [-3, -1, 1, 3],
        [-3, 0, 0, 3],
        [-3, 0, 1, 2],
        [-2, -1, 0, 3],
        [-2, -1, 1, 2],
        [-2, 0, 0, 2],
        [-1, 0, 0, 1],
    ]
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0] * 200
    target = 0

    expected = [[0, 0, 0, 0]]
    result = four_sum_optimized(nums, target)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
