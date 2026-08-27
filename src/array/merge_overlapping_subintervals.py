"""Merge Overlapping Subintervals.

Given an array of intervals where ``intervals[i] = [start_i, end_i]``, merge
all overlapping intervals.

Return an array of non-overlapping intervals that covers every interval in the
input. The intervals may be returned in any order.

Example 1:
    Input: intervals = [[1, 5], [3, 6], [8, 10], [15, 18]]
    Output: [[1, 6], [8, 10], [15, 18]]

    Explanation:
        Intervals [1, 5] and [3, 6] overlap, so they are merged into [1, 6].

Example 2:
    Input: intervals = [[5, 7], [1, 3], [4, 6], [8, 10]]
    Output: [[1, 3], [4, 7], [8, 10]]

    Explanation:
        Intervals [4, 6] and [5, 7] overlap, so they are merged into [4, 7].

Constraints:
    - 1 <= intervals.length <= 10^5
    - 0 <= start_i <= end_i <= 10^5
"""


def merge_overlapping_subintervals_brute_force(
    intervals: list[list[int]],
) -> list[list[int]]:
    """Merge overlapping intervals into non-overlapping intervals.

    Approach — Sort and Scan:
    1. Define a helper that combines two overlapping intervals by taking the
       smaller start and the larger end.
    2. Define helpers that determine whether two sorted intervals overlap and
       whether the current merged interval completely contains another one.
    3. Sort the intervals by their start values and initialize the result and
       current merged interval.
    4. Visit each interval as a possible beginning of a merged group. Skip it
       if it is already completely contained in the previously merged group.
    5. Starting with an interval that was not skipped, scan the following
       intervals. Merge each overlapping interval into ``current_interval``
       and stop when the next interval begins after the current interval ends.
    6. Append the completed merged interval to the result.
    7. Return all completed non-overlapping intervals.

    Args:
        intervals: A non-empty list of ``[start, end]`` pairs where each start
            is less than or equal to its corresponding end.

    Returns:
        A list of merged, non-overlapping intervals in ascending start order.

    Mutation:
        Sorts the outer ``intervals`` list in place. An unmerged interval added
        to the result may be the same inner list object as one in the input;
        merged intervals are newly created lists.

    Assumptions:
        Every interval contains exactly two integers and follows the problem's
        bounds. Intervals that touch at an endpoint are considered overlapping.

    Time Complexity:
        O(n log n), where n is the number of intervals. Sorting costs
        O(n log n). After sorting, the scan is O(n): the first interval of each
        overlapping group scans that group, and the outer loop skips the group
        members already contained in its merged interval.

    Space Complexity:
        O(n) including the returned intervals. Python's in-place Timsort may
        also use O(n) temporary memory. Aside from the output and sorting, the
        function uses O(1) additional variables at a time.

    https://www.youtube.com/watch?v=IexN60k62jo&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=23
    """

    # 1. Combine two overlapping intervals into their full covered range.
    def merge_intervals(
        first_interval: list[int], second_interval: list[int]
    ) -> list[int]:
        return [
            min(
                first_interval[0],
                second_interval[0],
            ),
            max(first_interval[1], second_interval[1]),
        ]

    # 2. Check for an overlap, including intervals that touch at an endpoint.
    def is_overlap(first_interval: list[int], second_interval: list[int]) -> bool:
        return first_interval[1] >= second_interval[0]

    # 2. Check whether the first interval completely contains the second.
    def is_total_overlap(first_interval: list[int], second_interval: list[int]) -> bool:
        return (
            first_interval[0] <= second_interval[0]
            and first_interval[1] >= second_interval[1]
        )

    # 3. Initialize the scan and sort intervals by start and then end value.
    result: list[list[int]] = []
    size: int = len(intervals)
    current_interval: list[int] = []
    intervals.sort()

    # 4. Consider every interval as the possible start of a merged group.
    for first_index in range(size):
        # 4. Skip intervals already covered by the previously merged group.
        if current_interval and is_total_overlap(
            current_interval, intervals[first_index]
        ):
            continue

        # 5. Start a new group and merge all following overlapping intervals.
        current_interval = intervals[first_index]
        for second_index in range(first_index + 1, size):
            if is_overlap(current_interval, intervals[second_index]):
                current_interval = merge_intervals(
                    current_interval, intervals[second_index]
                )
            else:
                break

        # 6. Store the completed interval for this overlapping group.
        result.append(current_interval)

    # 7. Return the sorted, non-overlapping merged intervals.
    return result


def merge_overlapping_subintervals_optimized(
    intervals: list[list[int]],
) -> list[list[int]]:
    """Merge overlapping intervals into non-overlapping intervals.

    Approach — Sort and Sweep:
    1. Sort the intervals so earlier starting positions are processed first,
       then initialize an empty result.
    2. Define helpers for detecting overlap and extending the ending position
       of the most recently merged interval.
    3. Scan every sorted interval from the beginning.
    4. Append the current interval when the result is empty or when it does not
       overlap the last result interval. This begins a new non-overlapping group.
    5. Otherwise, merge the current interval into the last result interval by
       keeping the larger ending position. This also handles intervals that are
       completely contained in the last result interval.
    6. Return the merged intervals in ascending start order.

    Args:
        intervals: A non-empty list of ``[start, end]`` pairs where each start
            is less than or equal to its corresponding end.

    Returns:
        A list of merged, non-overlapping intervals in ascending start order.

    Mutation:
        Sorts the outer ``intervals`` list in place. It also modifies inner
        interval lists when extending an interval's end. The returned result
        shares its inner interval objects with the input.

    Assumptions:
        The input follows the problem constraints and therefore contains at
        least one valid interval. Intervals touching at an endpoint are treated
        as overlapping.

    Time Complexity:
        O(n log n), where n is the number of intervals. Sorting costs
        O(n log n), and the single sweep through the sorted intervals costs
        O(n).

    Space Complexity:
        O(n) including the returned result. Python's in-place Timsort may also
        use O(n) temporary memory. Apart from the output and sorting, the sweep
        uses O(1) additional variables.
    """
    # 1. Sort the intervals and initialize an empty result.
    size: int = len(intervals)
    intervals.sort()

    result: list[list[int]] = []

    # 2. Check whether two intervals overlap or touch at an endpoint.
    def is_overlap(first_interval: list[int], second_interval: list[int]) -> bool:
        return first_interval[1] >= second_interval[0]

    # 2. Extend the first interval through the farther ending position.
    def merge_intervals(first_interval: list[int], second_interval: list[int]):
        first_interval[1] = max(first_interval[1], second_interval[1])

    # 3. Sweep through every sorted interval once.
    for index in range(size):
        # 4. Begin a new group when the result is empty or there is no overlap.
        if len(result) == 0 or not is_overlap(result[-1], intervals[index]):
            result.append(intervals[index])
        else:
            # 5. Merge overlaps, including completely contained intervals.
            merge_intervals(result[-1], intervals[index])

    # 6. Return all merged, non-overlapping intervals.
    return result


def solve() -> None:
    intervals: list[list[int]] = [[1, 5], [3, 6], [8, 10], [15, 18]]

    expected: list[list[int]] = [[1, 6], [8, 10], [15, 18]]
    result: list[list[int]] = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals: list[list[int]] = [[5, 7], [1, 3], [4, 6], [8, 10]]

    expected: list[list[int]] = [[1, 3], [4, 7], [8, 10]]
    result: list[list[int]] = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[2, 5]]

    expected = [[2, 5]]
    result = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[1, 2], [4, 5], [7, 8]]

    expected = [[1, 2], [4, 5], [7, 8]]
    result = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[1, 4], [4, 5]]

    expected = [[1, 5]]
    result = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[1, 10], [2, 3], [4, 8]]

    expected = [[1, 10]]
    result = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[1, 3], [2, 6], [5, 8], [7, 10]]

    expected = [[1, 10]]
    result = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[3, 5], [3, 5], [3, 5]]

    expected = [[3, 5]]
    result = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[0, 0], [0, 0]]

    expected = [[0, 0]]
    result = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[0, 100_000], [50_000, 100_000], [100_000, 100_000]]

    expected = [[0, 100_000]]
    result = merge_overlapping_subintervals_brute_force(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals: list[list[int]] = [[1, 5], [3, 6], [8, 10], [15, 18]]

    expected: list[list[int]] = [[1, 6], [8, 10], [15, 18]]
    result: list[list[int]] = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals: list[list[int]] = [[5, 7], [1, 3], [4, 6], [8, 10]]

    expected: list[list[int]] = [[1, 3], [4, 7], [8, 10]]
    result: list[list[int]] = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[2, 5]]

    expected = [[2, 5]]
    result = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[1, 2], [4, 5], [7, 8]]

    expected = [[1, 2], [4, 5], [7, 8]]
    result = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[1, 4], [4, 5]]

    expected = [[1, 5]]
    result = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[1, 10], [2, 3], [4, 8]]

    expected = [[1, 10]]
    result = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[1, 3], [1, 5], [2, 6]]

    expected = [[1, 6]]
    result = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[3, 5], [3, 5], [3, 5]]

    expected = [[3, 5]]
    result = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[0, 0], [0, 0]]

    expected = [[0, 0]]
    result = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[0, 100_000], [50_000, 100_000], [100_000, 100_000]]

    expected = [[0, 100_000]]
    result = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals = [[0, 0] for _ in range(100_000)]

    expected = [[0, 0]]
    result = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    intervals: list[list[int]] = [[1, 3], [1, 5]]

    expected: list[list[int]] = [[1, 5]]
    result: list[list[int]] = merge_overlapping_subintervals_optimized(intervals)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
