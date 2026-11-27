"""Unbounded Knapsack

Problem Statement:
    Given item weights, item values, and a bag capacity, return the maximum
    total value you can carry without exceeding the capacity.

    weights[i] and values[i] describe the same item type. You have an
    unlimited supply of every item type, so you may choose each type any
    number of times, including zero. Items cannot be split into fractions.
    You do not need to fill the bag exactly. Return the maximum value,
    rather than the selected items or the number of selections.

Input Assumptions:
    weights and values are nonempty lists of equal length.
    Weights and values are positive integers; capacity is a nonnegative integer.
    The item types are not necessarily sorted.

Sample (practice example):
    weights = [2, 4, 6]
    values = [5, 11, 13]
    capacity = 10
    Output: 27
    Choose two copies of the weight-4 item and one weight-2 item.
    Their total weight is 4 + 4 + 2 = 10 and value is 11 + 11 + 5 = 27.
    No other selection within capacity has a larger value.

Additional Examples (added for practice):
    1. Reuse a single item type with space left over:
        weights = [3]
        values = [7]
        capacity = 10
        Output: 21
        Three copies weigh 9 and give value 21. A fourth copy would exceed
        capacity; leaving one unit of unused space is allowed.

    2. No item fits:
        weights = [4, 6, 9]
        values = [8, 15, 20]
        capacity = 3
        Output: 0
        Every item is too heavy, so choose no items.

    3. Unsorted weights and a combination of item types:
        weights = [5, 2, 3]
        values = [12, 5, 8]
        capacity = 7
        Output: 18
        Choose one weight-3 item and two weight-2 items.
        Their weight is 3 + 2 + 2 = 7 and value is 8 + 5 + 5 = 18.

    4. Zero capacity:
        weights = [1, 3, 4]
        values = [2, 7, 9]
        capacity = 0
        Output: 0
        No positive-weight item fits in a bag with zero capacity.

Sources:
    https://www.youtube.com/watch?v=OgvOZ6OrJoY
    https://takeuforward.org/data-structure/unbounded-knapsack-dp-23
    Examples above are added for practice; they are not video transcriptions.
"""


def unbounded_knapsack_recursion(
    weights: list[int], values: list[int], capacity: int
) -> int:
    """Return the maximum value obtainable with unlimited item copies.

    Parameters:
        weights: Nonempty list of positive integer item weights.
        values: Positive integer item values, paired with weights by index.
            Both lists must have the same length; sorting is not required.
        capacity: Nonnegative integer maximum total weight allowed.

    Returns:
        The greatest total value without exceeding capacity. Items cannot
        be split, but each type can be used any number of times. Unused
        capacity is allowed. Return 0 if no item fits or capacity is zero.
        Neither input list is modified.

    Approach:
        Recursive Include/Exclude (Pick/Not Pick) Enumeration.

        1. Start at the last item with the full capacity. Each recursive
           call finds the best value using item types from 0 through index
           within remaining_capacity.
        2. At index 0, only the first item type remains. Take as many copies
           as fit: remaining_capacity // weights[index]. Multiply by its
           value to get the total. For weight 3, value 7, and capacity 10,
           three copies fit, giving 21 with one unit of capacity left.
           Positive values make taking the maximum number optimal here.
           If no copy fits, integer division gives 0.
        3. Calculate not_take by moving to index - 1 without changing the
           remaining capacity. This finds the best value when the current
           item type is excluded entirely.
        4. Start take at 0. If the current item fits, add its value and
           recurse with its weight subtracted from remaining_capacity.
           Keep the same index because unlimited copies are available.
           For weight 4 and capacity 10, taking one leaves capacity 6,
           where another copy of that same item can still be chosen.
        5. Return max(take, not_take): choose the more valuable of including
           or excluding the current item. These are alternative choices,
           so their values are compared rather than added together.
           For weights [2, 4, 6], values [5, 11, 13], and capacity 10, the
           best selection is weights 4 + 4 + 2, with value 11 + 11 + 5 = 27.

    Time Complexity:
        O(2 ** (n + capacity // m)) is a loose upper bound, where n is the
        item count and m is the smallest weight. Each call branches up to
        twice, reducing either the index or the remaining capacity.

    Space Complexity:
        O(n + capacity // m) for the recursive stack, excluding the inputs.
        Large inputs can exceed Python's default recursion depth.
    """

    def find_combination(index: int, remaining_capacity: int) -> int:

        # Step 2: Fill the remaining capacity with copies of the first item.
        if index == 0:
            return (remaining_capacity // weights[index]) * values[index]
        # Step 3: Exclude the current item type.
        not_take: int = find_combination(
            index=index - 1, remaining_capacity=remaining_capacity
        )
        # Step 4: Include one copy if it fits, allowing this item again.
        take: int = 0

        if weights[index] <= remaining_capacity:
            take = values[index] + find_combination(
                index=index, remaining_capacity=remaining_capacity - weights[index]
            )
        # Step 5: Choose the more valuable option.
        return max(take, not_take)

    # Step 1: Begin with all item types and the full capacity.
    return find_combination(index=len(weights) - 1, remaining_capacity=capacity)


def unbounded_knapsack_memoization(
    weights: list[int], values: list[int], capacity: int
) -> int:
    """Return the greatest value obtainable with unlimited item copies.

    Parameters:
        weights: Nonempty list of positive integer item weights.
        values: Positive integer values paired with weights by index.
            Both lists must have equal length; sorting is not required.
        capacity: Nonnegative integer maximum total weight allowed.

    Returns:
        The maximum total value without exceeding capacity. Each item type
        can be reused, but items cannot be split. Unused space is allowed.
        Return 0 for zero capacity or when no item fits.
        Neither input list is modified.

    Approach:
        Top-Down Dynamic Programming (Memoization).

        1. Create max_value_dp with one row per item type and columns for
           capacities 0 through capacity. max_value_dp[index][remaining_capacity]
           stores the best value using types 0 through index within that
           capacity. Initialize cells to -1 to mean uncomputed; 0 is a
           valid answer when no item fits.
        2. Start the recursion with the last item and the full capacity.
           Each call finds the best value for its index and remaining space.
        3. At index 0, only the first item type remains. Take as many copies
           as fit using remaining_capacity // weights[index], then multiply
           by its value. For weight 3, value 7, and capacity 10, three copies
           give 21, leaving one unit unused. Positive values make the maximum
           number of copies optimal here. Store and return this answer.
        4. For later indexes, return the stored answer if it is not -1.
           Reaching the same index and capacity again cannot change the
           best value, so this avoids repeating the recursive work.
        5. Calculate not_take by moving to index - 1 with unchanged capacity.
           This excludes the current item type entirely.
        6. Start take at 0. If the current item fits, add its value and
           recurse with its weight subtracted. Keep the same index because
           another copy of this item is allowed. For a weight-4 item and
           capacity 10, taking one leaves capacity 6, which can hold another.
        7. Store and return max(not_take, take). These are alternative
           selections, so compare their values rather than add them.
           For weights [2, 4, 6], values [5, 11, 13], and capacity 10, the
           best choice is weights 4 + 4 + 2, with value 11 + 11 + 5 = 27.
           The stored answer can be reused by later recursive calls.

    Time Complexity:
        O(n * (capacity + 1)), where n is the number of item types.
        Initializing the table and computing each state take constant work
        per cell, apart from recursive calls whose answers are saved.

    Space Complexity:
        O(n * (capacity + 1) + n + capacity // m), where m is the smallest
        weight, for the table and recursive stack, excluding the inputs.
        Large inputs can exceed Python's default recursion depth.
    """
    # Step 1: Allocate a table of uncomputed maximum values.
    size: int = len(weights)
    max_value_dp: list[list[int]] = [[-1] * (capacity + 1) for _ in range(size)]

    def find_combination(index: int, remaining_capacity: int) -> int:
        # Step 3: Use as many copies of the first item as fit.
        if index == 0:
            max_value_dp[index][remaining_capacity] = (
                remaining_capacity // weights[index]
            ) * values[index]
            return max_value_dp[index][remaining_capacity]

        # Step 4: Reuse a previously computed answer.
        if max_value_dp[index][remaining_capacity] != -1:
            return max_value_dp[index][remaining_capacity]

        # Step 5: Exclude this item type.
        not_take: int = find_combination(
            index=index - 1, remaining_capacity=remaining_capacity
        )

        # Step 6: Include one copy if it fits, allowing this item again.
        take: int = 0

        if weights[index] <= remaining_capacity:
            take = values[index] + find_combination(
                index=index, remaining_capacity=remaining_capacity - weights[index]
            )
        # Step 7: Save and return the more valuable choice.
        max_value_dp[index][remaining_capacity] = max(not_take, take)

        return max_value_dp[index][remaining_capacity]

    # Step 2: Start with all item types and the full capacity.
    return find_combination(index=size - 1, remaining_capacity=capacity)


def unbounded_knapsack_tabulation(
    weights: list[int], values: list[int], capacity: int
) -> int:
    """Return the maximum value obtainable with unlimited item copies.

    Parameters:
        weights: Nonempty list of positive integer item weights.
        values: Positive integer values paired with weights by index.
            Both lists must have equal length; sorting is not required.
        capacity: Nonnegative integer maximum total weight allowed.

    Returns:
        The greatest total value without exceeding capacity. Item types
        can be reused, but individual items cannot be split. Unused space
        is allowed. Return 0 for zero capacity or when no item fits.
        Neither input list is modified.

    Approach:
        Bottom-Up Dynamic Programming (Tabulation).

        1. Create max_value_dp with one row per item type and columns for
           capacities 0 through capacity. max_value_dp[index][remaining_capacity]
           stores the best value using types 0 through index within that
           capacity. Start every cell at 0, representing choosing no items.
        2. Fill the first row using only the first item type. The number of
           copies that fit is remaining_capacity // weights[0]. Multiply
           this by values[0]. For weight 3, value 7, and capacity 10, three
           copies give 21 with one unit unused. If no copy fits, the value
           is 0. Positive values make taking as many as fit optimal here.
        3. Process each later item type and each capacity in increasing
           order. Smaller capacities in the current row are ready before
           larger capacities need them; every row also includes capacity 0.
        4. Set not_take to the previous row at the same capacity. This is
           the best value when the current item type is excluded entirely.
        5. Start take at 0. If the item fits, add values[index] to the
           current row at remaining_capacity - weights[index]. Reading the
           current row allows another copy of this item to be included.
           For weight 4 and capacity 10, taking one leaves capacity 6,
           whose current-row answer can already include a weight-4 item.
        6. Store max(take, not_take), choosing the more valuable alternative.
           Do not add these values together: they describe separate choices
           for the same available capacity. For weights [2, 4, 6], values
           [5, 11, 13], and capacity 10, weights 4 + 4 + 2 give the best
           value, 11 + 11 + 5 = 27.
        7. Return the last row at capacity. This includes all item types
           and gives the best value within the full bag capacity.

    Time Complexity:
        O(n * (capacity + 1)), where n is the number of item types.
        Initializing and filling the table takes constant work per cell.

    Space Complexity:
        O(n * (capacity + 1)) for max_value_dp, excluding the inputs.
        The other variables use constant additional space.
    """
    # Step 1: Allocate maximum values for every item prefix and capacity.
    size: int = len(weights)
    max_value_dp: list[list[int]] = [[0] * (capacity + 1) for _ in range(size)]

    # Step 2: Fill the first row with repeated copies of the first item.
    for remaining_capacity in range(capacity + 1):
        max_value_dp[0][remaining_capacity] = (
            remaining_capacity // weights[0]
        ) * values[0]

    # Step 3: Build later rows in increasing capacity order.
    for index in range(1, size):
        for remaining_capacity in range(capacity + 1):
            # Step 4: Exclude this item type using the previous row.
            not_take: int = max_value_dp[index - 1][remaining_capacity]
            # Step 5: Include one copy; the current row permits reuse.
            take: int = 0
            if weights[index] <= remaining_capacity:
                take = (
                    values[index]
                    + max_value_dp[index][remaining_capacity - weights[index]]
                )
            # Step 6: Save the more valuable choice.
            max_value_dp[index][remaining_capacity] = max(take, not_take)

    # Step 7: Read the answer using every item type and the full capacity.
    return max_value_dp[size - 1][capacity]


def unbounded_knapsack_tabulation_space_optimized(
    weights: list[int], values: list[int], capacity: int
) -> int:
    """Return the maximum value of unlimited items using two rows of storage.

    Parameters:
        weights: Nonempty list of positive integer item weights.
        values: Positive integer values paired with weights by index.
            Both lists must have equal length; sorting is not required.
        capacity: Nonnegative integer maximum total weight allowed.

    Returns:
        The greatest total value without exceeding capacity. Each item type
        can be reused, but items cannot be split. Unused space is allowed.
        Return 0 for zero capacity or when no item fits.
        Neither input list is modified.

    Approach:
        Bottom-Up Dynamic Programming (Tabulation) with Space Optimization.

        1. Create prev_max_value_dp for capacities 0 through capacity. Each
           position stores a maximum value within that capacity. Only the
           previous and current rows are needed instead of the full table.
        2. Initialize the previous row using only the first item type.
           Multiply remaining_capacity // weights[0] by values[0]. For
           weight 3, value 7, and capacity 10, three copies give 21 with one
           unit unused. Positive values make taking as many as fit optimal.
           When no copy fits, the result is 0.
        3. For each later item type, allocate a fresh current_max_value_dp.
           Process capacities in increasing order so smaller capacities in
           the current row are ready before larger capacities need them.
        4. Set not_take to the previous row at the same capacity. This
           excludes the current item type and uses only earlier types.
        5. Start take at 0. If the item fits, add its value to the current
           row at remaining_capacity - weights[index]. Reading the current
           row permits repeated copies of this item. For weight 4 and
           capacity 10, taking one leaves 6, whose answer may include
           another weight-4 item.
        6. Store max(not_take, take) in the current row. The choices are
           alternatives for the same capacity, so compare rather than add
           them. For weights [2, 4, 6], values [5, 11, 13], and capacity 10,
           weights 4 + 4 + 2 give the best value, 11 + 11 + 5 = 27.
        7. After completing the row, assign it to prev_max_value_dp. Python
           assignment shares the list rather than copying it. Allocating a
           fresh current row on the next iteration keeps the previous row
           separate while the next row is built.
        8. Return prev_max_value_dp[capacity] after processing all item
           types. For a single type, this reads the initialized first row.

    Time Complexity:
        O(n * (capacity + 1)), where n is the number of item types.
        Each row is initialized and filled with constant work per capacity.

    Space Complexity:
        O(capacity + 1) for the previous and current rows, excluding inputs.
        At most two rows are needed regardless of the number of item types.
    """
    # Step 1: Allocate one row of maximum values.
    size: int = len(weights)
    prev_max_value_dp: list[int] = [0] * (capacity + 1)

    # Step 2: Initialize values using copies of the first item.
    for remaining_capacity in range(capacity + 1):
        prev_max_value_dp[remaining_capacity] = (
            remaining_capacity // weights[0]
        ) * values[0]

    # Step 3: Build a fresh row for each later item type.
    for index in range(1, size):
        current_max_value_dp: list[int] = [0] * (capacity + 1)
        for remaining_capacity in range(capacity + 1):
            # Step 4: Exclude this item type using the previous row.
            not_take: int = prev_max_value_dp[remaining_capacity]
            # Step 5: Include one copy; the current row allows reuse.
            take: int = 0
            if weights[index] <= remaining_capacity:
                take = (
                    values[index]
                    + current_max_value_dp[remaining_capacity - weights[index]]
                )

            # Step 6: Save the more valuable alternative.
            current_max_value_dp[remaining_capacity] = max(not_take, take)

        # Step 7: Keep this completed row for the next item type.
        prev_max_value_dp = current_max_value_dp

    # Step 8: Return the best value within the full capacity.
    return prev_max_value_dp[capacity]


def solve() -> None:
    # Sample from the question.
    weights = [2, 4, 6]
    values = [5, 11, 13]
    capacity = 10
    expected = 27
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero capacity.
    weights = [1, 3, 4]
    values = [2, 7, 9]
    capacity = 0
    expected = 0
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest positive inputs.
    weights = [1]
    values = [1]
    capacity = 1
    expected = 1
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item fits exactly.
    weights = [3]
    values = [7]
    capacity = 3
    expected = 7
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item does not fit.
    weights = [3]
    values = [7]
    capacity = 2
    expected = 0
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item reused exactly.
    weights = [3]
    values = [7]
    capacity = 9
    expected = 21
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item reused with unused capacity.
    weights = [3]
    values = [7]
    capacity = 10
    expected = 21
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No item fits.
    weights = [4, 6, 9]
    values = [8, 15, 20]
    capacity = 3
    expected = 0
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted weights with mixed choices.
    weights = [5, 2, 3]
    values = [12, 5, 8]
    capacity = 7
    expected = 18
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item at beginning.
    weights = [2, 3, 5]
    values = [10, 4, 6]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item in middle.
    weights = [3, 2, 5]
    values = [4, 10, 6]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item at end.
    weights = [3, 5, 2]
    values = [4, 6, 10]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate weights with different values.
    weights = [2, 2, 3]
    values = [3, 5, 4]
    capacity = 4
    expected = 10
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical item types.
    weights = [2, 2, 2]
    values = [5, 5, 5]
    capacity = 6
    expected = 15
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values with different weights.
    weights = [4, 2, 3]
    values = [5, 5, 5]
    capacity = 6
    expected = 15
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact filling is not required.
    weights = [3, 5]
    values = [10, 11]
    capacity = 7
    expected = 20
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixing items beats either type alone.
    weights = [3, 5]
    values = [5, 9]
    capacity = 8
    expected = 14
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best ratio alone does not give best packing.
    weights = [3, 4]
    values = [5, 7]
    capacity = 6
    expected = 10
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # High value item exceeds capacity.
    weights = [2, 9, 3]
    values = [4, 100, 5]
    capacity = 6
    expected = 12
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Capacity equals an available weight.
    weights = [5, 2, 3]
    values = [20, 5, 6]
    capacity = 5
    expected = 20
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Capacity just above an available weight.
    weights = [5, 2, 3]
    values = [20, 5, 6]
    capacity = 6
    expected = 20
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several copies of weight one.
    weights = [1, 4, 6]
    values = [3, 10, 15]
    capacity = 8
    expected = 24
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # More item types with shallow recursion.
    weights = [9, 7, 5, 3, 2]
    values = [10, 9, 7, 5, 3]
    capacity = 10
    expected = 16
    result = unbounded_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: maximize value with unlimited copies of each item.
    weights = [2, 4, 6]
    values = [5, 11, 13]
    capacity = 10
    expected = 27
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero capacity.
    weights = [1, 3, 4]
    values = [2, 7, 9]
    capacity = 0
    expected = 0
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest positive inputs.
    weights = [1]
    values = [1]
    capacity = 1
    expected = 1
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item fits exactly.
    weights = [3]
    values = [7]
    capacity = 3
    expected = 7
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item does not fit.
    weights = [3]
    values = [7]
    capacity = 2
    expected = 0
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item reused exactly.
    weights = [3]
    values = [7]
    capacity = 9
    expected = 21
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item reused with space left.
    weights = [3]
    values = [7]
    capacity = 10
    expected = 21
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No item fits.
    weights = [4, 6, 9]
    values = [8, 15, 20]
    capacity = 3
    expected = 0
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted weights with mixed choices.
    weights = [5, 2, 3]
    values = [12, 5, 8]
    capacity = 7
    expected = 18
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item at beginning.
    weights = [2, 3, 5]
    values = [10, 4, 6]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item in middle.
    weights = [3, 2, 5]
    values = [4, 10, 6]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item at end.
    weights = [3, 5, 2]
    values = [4, 6, 10]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate weights with different values.
    weights = [2, 2, 3]
    values = [3, 5, 4]
    capacity = 4
    expected = 10
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical item types.
    weights = [2, 2, 2]
    values = [5, 5, 5]
    capacity = 6
    expected = 15
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values with different weights.
    weights = [4, 2, 3]
    values = [5, 5, 5]
    capacity = 6
    expected = 15
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact filling is not required.
    weights = [3, 5]
    values = [10, 11]
    capacity = 7
    expected = 20
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixing types beats either alone.
    weights = [3, 5]
    values = [5, 9]
    capacity = 8
    expected = 14
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best ratio alone does not give best packing.
    weights = [3, 4]
    values = [5, 7]
    capacity = 6
    expected = 10
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # High value item exceeds capacity.
    weights = [2, 9, 3]
    values = [4, 100, 5]
    capacity = 6
    expected = 12
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Capacity equals an available weight.
    weights = [5, 2, 3]
    values = [20, 5, 6]
    capacity = 5
    expected = 20
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Capacity just above an available weight.
    weights = [5, 2, 3]
    values = [20, 5, 6]
    capacity = 6
    expected = 20
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated weight one.
    weights = [1, 4, 6]
    values = [3, 10, 15]
    capacity = 8
    expected = 24
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several item types.
    weights = [9, 7, 5, 3, 2]
    values = [10, 9, 7, 5, 3]
    capacity = 10
    expected = 16
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal value alternatives.
    weights = [2, 3]
    values = [4, 6]
    capacity = 6
    expected = 12
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated subproblems.
    weights = [2, 3, 5, 7]
    values = [3, 5, 8, 12]
    capacity = 60
    expected = 102
    result = unbounded_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: maximize value with unlimited copies of each item.
    weights = [2, 4, 6]
    values = [5, 11, 13]
    capacity = 10
    expected = 27
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero capacity.
    weights = [1, 3, 4]
    values = [2, 7, 9]
    capacity = 0
    expected = 0
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest positive inputs.
    weights = [1]
    values = [1]
    capacity = 1
    expected = 1
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item fits exactly.
    weights = [3]
    values = [7]
    capacity = 3
    expected = 7
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item does not fit.
    weights = [3]
    values = [7]
    capacity = 2
    expected = 0
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item reused exactly.
    weights = [3]
    values = [7]
    capacity = 9
    expected = 21
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item reused with unused space.
    weights = [3]
    values = [7]
    capacity = 10
    expected = 21
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No item fits.
    weights = [4, 6, 9]
    values = [8, 15, 20]
    capacity = 3
    expected = 0
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted weights with mixed choices.
    weights = [5, 2, 3]
    values = [12, 5, 8]
    capacity = 7
    expected = 18
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item at beginning.
    weights = [2, 3, 5]
    values = [10, 4, 6]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item in middle.
    weights = [3, 2, 5]
    values = [4, 10, 6]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item at end.
    weights = [3, 5, 2]
    values = [4, 6, 10]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate weights with different values.
    weights = [2, 2, 3]
    values = [3, 5, 4]
    capacity = 4
    expected = 10
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical item types.
    weights = [2, 2, 2]
    values = [5, 5, 5]
    capacity = 6
    expected = 15
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values with different weights.
    weights = [4, 2, 3]
    values = [5, 5, 5]
    capacity = 6
    expected = 15
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact filling is not required.
    weights = [3, 5]
    values = [10, 11]
    capacity = 7
    expected = 20
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixing types beats either alone.
    weights = [3, 5]
    values = [5, 9]
    capacity = 8
    expected = 14
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best ratio alone does not give best packing.
    weights = [3, 4]
    values = [5, 7]
    capacity = 6
    expected = 10
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # High value item exceeds capacity.
    weights = [2, 9, 3]
    values = [4, 100, 5]
    capacity = 6
    expected = 12
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Capacity equals an available weight.
    weights = [5, 2, 3]
    values = [20, 5, 6]
    capacity = 5
    expected = 20
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Capacity just above an available weight.
    weights = [5, 2, 3]
    values = [20, 5, 6]
    capacity = 6
    expected = 20
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated weight one.
    weights = [1, 4, 6]
    values = [3, 10, 15]
    capacity = 8
    expected = 24
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several item types.
    weights = [9, 7, 5, 3, 2]
    values = [10, 9, 7, 5, 3]
    capacity = 10
    expected = 16
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal value alternatives.
    weights = [2, 3]
    values = [4, 6]
    capacity = 6
    expected = 12
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger capacity with repeated choices.
    weights = [2, 3, 5, 7]
    values = [3, 5, 8, 12]
    capacity = 60
    expected = 102
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Large capacity without recursion.
    weights = [1, 4]
    values = [3, 10]
    capacity = 5000
    expected = 15000
    result = unbounded_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimized tabulation: unlimited copies of each item.
    weights = [2, 4, 6]
    values = [5, 11, 13]
    capacity = 10
    expected = 27
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero capacity.
    weights = [1, 3, 4]
    values = [2, 7, 9]
    capacity = 0
    expected = 0
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest positive inputs.
    weights = [1]
    values = [1]
    capacity = 1
    expected = 1
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item fits exactly.
    weights = [3]
    values = [7]
    capacity = 3
    expected = 7
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item does not fit.
    weights = [3]
    values = [7]
    capacity = 2
    expected = 0
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item reused exactly.
    weights = [3]
    values = [7]
    capacity = 9
    expected = 21
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item reused with unused space.
    weights = [3]
    values = [7]
    capacity = 10
    expected = 21
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No item fits.
    weights = [4, 6, 9]
    values = [8, 15, 20]
    capacity = 3
    expected = 0
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted weights with mixed choices.
    weights = [5, 2, 3]
    values = [12, 5, 8]
    capacity = 7
    expected = 18
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item at beginning.
    weights = [2, 3, 5]
    values = [10, 4, 6]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item in middle.
    weights = [3, 2, 5]
    values = [4, 10, 6]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item at end.
    weights = [3, 5, 2]
    values = [4, 6, 10]
    capacity = 6
    expected = 30
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate weights with different values.
    weights = [2, 2, 3]
    values = [3, 5, 4]
    capacity = 4
    expected = 10
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical item types.
    weights = [2, 2, 2]
    values = [5, 5, 5]
    capacity = 6
    expected = 15
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values with different weights.
    weights = [4, 2, 3]
    values = [5, 5, 5]
    capacity = 6
    expected = 15
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact filling is not required.
    weights = [3, 5]
    values = [10, 11]
    capacity = 7
    expected = 20
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixing types beats either alone.
    weights = [3, 5]
    values = [5, 9]
    capacity = 8
    expected = 14
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best ratio alone does not give best packing.
    weights = [3, 4]
    values = [5, 7]
    capacity = 6
    expected = 10
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # High value item exceeds capacity.
    weights = [2, 9, 3]
    values = [4, 100, 5]
    capacity = 6
    expected = 12
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Capacity equals an available weight.
    weights = [5, 2, 3]
    values = [20, 5, 6]
    capacity = 5
    expected = 20
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Capacity just above an available weight.
    weights = [5, 2, 3]
    values = [20, 5, 6]
    capacity = 6
    expected = 20
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated weight one.
    weights = [1, 4, 6]
    values = [3, 10, 15]
    capacity = 8
    expected = 24
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several item types.
    weights = [9, 7, 5, 3, 2]
    values = [10, 9, 7, 5, 3]
    capacity = 10
    expected = 16
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal value alternatives.
    weights = [2, 3]
    values = [4, 6]
    capacity = 6
    expected = 12
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Many repeated choices.
    weights = [2, 3, 5, 7]
    values = [3, 5, 8, 12]
    capacity = 60
    expected = 102
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Large capacity.
    weights = [1, 4]
    values = [3, 10]
    capacity = 5000
    expected = 15000
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Previous and current rows remain separate.
    weights = [4, 3, 2]
    values = [5, 7, 6]
    capacity = 8
    expected = 24
    result = unbounded_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
