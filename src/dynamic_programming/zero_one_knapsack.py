"""0/1 Knapsack

Problem Statement:
    Given N items with weights and values, choose items for a bag whose
    weight capacity is W. Return the maximum total value obtainable
    without exceeding that capacity.

    Each item may be selected at most once and must be taken whole.
    weights[i] and values[i] describe the same item.

Constraints:
    1 <= N <= 100
    1 <= weights[i] <= 50
    1 <= values[i] <= 100
    1 <= W <= 1000
    Time limit: 1 second.

Sample:
    weights = [1, 2, 4, 5]
    values  = [5, 4, 8, 6]
    W = 5

    Output: 13

    Choose the items at indexes 0 and 2. Their weights are 1 and 4,
    so the total weight is 5, which fits W. Their values are 5 and 8,
    giving a total value of 13. No other selection within weight 5
    gives a greater total value.

Additional Examples (added for practice):
    1. No item fits:
        Input: weights = [4, 5], values = [10, 20], capacity = 3
        Output: 0
        Neither item fits, so choose nothing.

    2. All items fit:
        Input: weights = [1, 2, 3], values = [4, 5, 6], capacity = 6
        Output: 15
        Taking all three items gives total weight 6 and value 15.

    3. One item cannot be reused:
        Input: weights = [2], values = [7], capacity = 4
        Output: 7
        The sole item can be chosen once, even though capacity remains.

    4. Combining items beats the highest-value individual item:
        Input: weights = [2, 3, 5], values = [6, 8, 13], capacity = 5
        Output: 14
        The first two items together give value 14 at weight 5.

Sources:
    https://www.naukri.com/code360/problems/0-1-knapsack_920542
    https://www.youtube.com/watch?v=GqOmJHQZivw

Function Interface:
    Accept the weights, values, and capacity directly. Their shared array
    length provides N; solve() demonstrates one sample.
"""


def zero_one_knapsack_recursion(
    weights: list[int], values: list[int], capacity: int
) -> int:
    """Return the maximum item value that fits within the bag's capacity.

    Args:
        weights: A nonempty list of positive integer item weights.
        values: A list of positive integer values, with the same length
            as weights. Matching indexes describe the same item.
        capacity: The bag's maximum allowed total weight.

    Returns:
        The highest total value obtainable without exceeding capacity.
        Each item is used at most once; unused capacity is allowed.
        Return zero when no item fits, including when capacity is zero.

    Mutation and assumptions:
        Neither input list is modified. Equal, nonzero list lengths,
        positive weights and values, and nonnegative capacity are assumed
        and are not validated. Empty lists, mismatched lengths, and negative
        inputs are unsupported. The zero-capacity shortcut relies on positive
        weights. Long inputs may exceed Python's recursion-depth limit.

    Approach:
        Depth-First Search (DFS), using include/exclude recursion.
        1. Read the item count. The helper considers items from index zero
           through index, with weight representing the remaining capacity.
           It returns the best additional value from those available items.
        2. If weight is zero, return zero immediately. The bag is full and
           every item has positive weight, so nothing else can be added.
           Any value from items already chosen is added by earlier calls.
        3. If index is zero, only the first item remains. Return its value
           if it fits; otherwise return zero. Because its value is positive,
           taking it when possible is better than skipping it.
        4. Calculate not_pick by skipping the current item. Search earlier
           indexes with the same remaining capacity to find their best value.
        5. Initialize pick to -10**9 to mark an unavailable take choice.
           If the item fits, add its value to the best value from earlier
           indexes with its weight subtracted from the remaining capacity.
           For example, taking an item of weight 4 and value 8 from capacity
           5 leaves capacity 1; its branch returns 8 plus the best value
           that fits in that remaining capacity. Decreasing index in both
           branches ensures each item can be used at most once.
        6. Return max(pick, not_pick), selecting the more valuable valid
           choice rather than adding mutually exclusive alternatives.
           The skip branch always permits taking nothing, so its result
           is nonnegative and beats the sentinel for an invalid take.
        7. Begin with the last index and the full capacity, then return
           the best value. The recursion tracks indexes and remaining
           capacity without constructing item selections or sorting inputs.

    Time Complexity:
        O(2**N) in the worst case, where N is the item count. Each item
        can create a skip and take branch; fit checks and the zero-capacity
        shortcut reduce actual work. This can be too slow for N == 100
        under the stated one-second limit.

    Space Complexity:
        O(N) extra space, excluding the input lists. The recursive stack
        holds at most N helper calls with constant local storage per call;
        no collection of item combinations is stored.
    """
    # Step 1: Set up the number of available items.
    size: int = len(weights)

    def choose_item(index: int, weight: int) -> int:
        # Step 2: A full bag cannot accept any positive-weight item.
        if weight == 0:
            return 0
        # Step 3: With only the first item left, take it if it fits.
        if index == 0:
            if weights[index] <= weight:
                return values[index]
            else:
                return 0

        # Step 4: Skip this item and search with the same capacity.
        not_pick: int = choose_item(index=index - 1, weight=weight)

        # Step 5: If it fits, add its value and search with reduced capacity.
        pick: int = -(10**9)
        if weights[index] <= weight:
            pick = values[index] + choose_item(
                index=index - 1, weight=weight - weights[index]
            )
        # Step 6: Select the better of taking and skipping this item.
        return max(pick, not_pick)

    # Step 7: Start with every item available and the full bag capacity.
    return choose_item(index=size - 1, weight=capacity)


def zero_one_knapsack_memoization(
    weights: list[int], values: list[int], capacity: int
) -> int:
    """Return the maximum value fitting the capacity using cached recursion.

    Args:
        weights: A nonempty list of positive integer item weights.
        values: Positive integer item values, matching weights by index
            and length. Each item can be selected at most once.
        capacity: A nonnegative integer maximum total weight.

    Returns:
        The highest obtainable total value without exceeding capacity.
        Unused capacity is allowed. Return zero if no item fits or the
        capacity is zero.

    Mutation and assumptions:
        Neither input list is modified. Equal nonzero list lengths,
        positive weights and values, and nonnegative capacity are assumed
        and are not validated. Empty or mismatched lists and negative
        inputs are unsupported. The zero-capacity shortcut relies on
        positive weights. Long inputs may exceed Python's recursion limit.

    Approach:
        Top-down Dynamic Programming (Memoization), using Depth-First
        Search (DFS) with include/exclude recursion.
        1. Read size and create max_value_dp with one independent row per
           item and capacity + 1 columns. Its entry at index and weight
           stores the best value using items 0 through index with that
           remaining capacity. Initialize entries to -10**9 to mean
           uncomputed; zero is a valid computed answer. Columns use capacity,
           not the total item weight, because the bag can be larger than
           all available items combined.
        2. In choose_item, return zero when weight is zero. No positive
           weight fits in a full bag, so no additional value can be gained.
           Values of items already chosen are added by the calling frames.
        3. When index is zero, only the first item remains. Return its
           value if it fits, otherwise zero. Its positive value makes
           taking it worthwhile whenever it fits. These base cases return
           directly without caching their constant-time answers.
        4. Check max_value_dp[index][weight]. If it differs from -10**9,
           return the stored value immediately, including a cached zero.
           This avoids exploring the same item prefix and capacity again.
        5. Calculate not_pick by skipping this item and searching earlier
           indexes with unchanged capacity.
        6. Initialize pick to -10**9 for an unavailable take choice. If
           the item fits, add its value to the best result from earlier
           indexes with its weight subtracted. An item weighing 4 with
           value 8, taken from capacity 5, contributes 8 plus the best
           value fitting capacity 1. Decreasing index prevents item reuse.
        7. Store max(pick, not_pick) in the current cache entry, then
           return that entry. These are alternative selections, so choose
           their maximum rather than adding them. A valid skip result is
           nonnegative and therefore beats an invalid take sentinel.
        8. Start at the final index with the full capacity and return
           the best value. No item combinations are constructed or stored.

    Time Complexity:
        O(N * (W + 1)), where N is the item count and W is capacity.
        Initializing the cache takes this time, and each non-base state
        is computed once with at most two recursive choices.

    Space Complexity:
        O(N * (W + 1)) extra space, excluding the input lists. The cache
        contains N rows of W + 1 entries, and the recursive stack adds
        O(N) space.
    """
    # Step 1: Allocate independent cache rows indexed by remaining capacity.
    size: int = len(weights)
    max_value_dp: list[list[int]] = [[-(10**9)] * (capacity + 1) for _ in range(size)]

    def choose_item(index: int, weight: int) -> int:
        # Step 2: A full bag permits no additional positive-weight items.
        if weight == 0:
            return 0

        # Step 3: With one item left, take its positive value if it fits.
        if index == 0:
            if weights[index] <= weight:
                return values[index]
            else:
                return 0

        # Step 4: Reuse a computed answer, including zero.
        if max_value_dp[index][weight] != -(10**9):
            return max_value_dp[index][weight]

        # Step 5: Skip the current item without reducing remaining capacity.
        not_pick: int = choose_item(index=index - 1, weight=weight)

        # Step 6: If it fits, add its value and search with reduced capacity.
        pick: int = -(10**9)
        if weights[index] <= weight:
            pick = values[index] + choose_item(
                index=index - 1, weight=weight - weights[index]
            )
        # Step 7: Cache and return the better choice.
        max_value_dp[index][weight] = max(pick, not_pick)

        return max_value_dp[index][weight]

    # Step 8: Begin with all items available and the full bag capacity.
    return choose_item(index=size - 1, weight=capacity)


def zero_one_knapsack_tabulation(
    weights: list[int], values: list[int], capacity: int
) -> int:
    """Return the maximum value fitting the capacity using a 2D table.

    Args:
        weights: A nonempty list of positive integer item weights.
        values: Positive integer item values, matching weights by index
            and length. Each item can be used at most once.
        capacity: A nonnegative integer maximum allowed total weight.

    Returns:
        The highest obtainable value without exceeding capacity. Unused
        space is allowed. Return zero if no item fits or capacity is zero.

    Mutation and assumptions:
        Neither list is modified or sorted. Equal nonzero list lengths,
        positive weights and values, and nonnegative capacity are assumed
        and are not validated. Empty or mismatched lists and negative
        inputs are unsupported. Zero-weight items are outside the stated
        constraints; column zero is left at zero for positive-weight items.

    Approach:
        Bottom-up Dynamic Programming (Tabulation).
        1. Read size and create max_value_dp with size independent rows
           and capacity + 1 columns, initially zero. The entry at index
           and weight is the best value using items 0 through index within
           that allowed capacity. Columns represent weight limits, not
           weights that must be filled exactly. Choosing nothing gives zero.
        2. Initialize row zero, where only the first item is available.
           Starting at weights[0], put values[0] into every column through
           capacity. The item fits at all these limits, even when space
           remains unused, and may be taken only once. For first weight 2,
           value 4, and capacity 5, the row is [0, 0, 4, 4, 4, 4].
           Sorting is unnecessary: if the first weight exceeds capacity,
           this loop does not run and later items are still processed.
        3. Process indexes from 1 onward and allowed weights from 1
           through capacity. Earlier rows are complete before they are
           read. Column zero stays zero because no positive-weight item
           can fit into a bag with zero capacity.
        4. Read not_pick from the previous row at the same allowed weight.
           This preserves the best earlier selection while skipping the
           current item.
        5. Start picked at zero. If the item fits, add its value to the
           previous row's best value at weight - weights[index]. This
           subtraction is the space left after choosing the item. Reading
           the previous row prevents reusing it. An invalid picked value
           of zero is safe because not_pick is always nonnegative.
        6. Store max(not_pick, picked) in the current entry. These are
           alternative selections, so choose the greater value rather than
           adding them. With weights [2, 3, 4], values [4, 5, 7], and
           capacity 5, row 1 at capacity 5 compares skipping item 1 for
           value 4 against taking it for 5 + row 0 at capacity 2 = 9.
           Row 2 then compares skipping item 2 for 9 against taking it
           for 7 + row 1 at capacity 1 = 7, preserving the answer 9.
        7. Return the last row at the full capacity. It considers every
           item without constructing or storing the selected combinations.

    Time Complexity:
        O(N * (W + 1)), where N is the item count and W is capacity.
        Initializing and filling the table take constant work per cell;
        the first-row initialization takes at most O(W) additional work.

    Space Complexity:
        O(N * (W + 1)) extra space, excluding the input lists. The table
        stores N rows of W + 1 values; other variables take constant space
        and no recursive call stack is needed.
    """
    # Step 1: Create independent rows of best values for each capacity limit.
    size: int = len(weights)
    max_value_dp: list[list[int]] = [[0] * (capacity + 1) for _ in range(size)]

    # Step 2: The first item gives its value at every capacity where it fits.
    for weight in range(weights[0], capacity + 1):
        max_value_dp[0][weight] = values[0]

    # Step 3: Fill later item rows for every positive capacity through the limit.
    for index in range(1, size):
        for weight in range(1, (capacity + 1)):
            # Step 4: Skip this item and preserve the previous row's value.
            not_pick: int = max_value_dp[index - 1][weight]
            # Step 5: Taking it adds its value to the best use of the space left.
            picked: int = 0
            if weights[index] <= weight:
                picked = (
                    values[index] + max_value_dp[index - 1][weight - weights[index]]
                )
            # Step 6: Store the better of the two alternative selections.
            max_value_dp[index][weight] = max(not_pick, picked)

    # Step 7: Read the best value using all items at the full capacity.
    return max_value_dp[size - 1][capacity]


def zero_one_knapsack_tabulation_space_optimized(
    weights: list[int], values: list[int], capacity: int
) -> int:
    """Return the maximum value fitting the capacity using two DP rows.

    Args:
        weights: A nonempty list of positive integer item weights.
        values: Positive integer item values, with the same length as
            weights. Matching indexes describe one item, usable at most once.
        capacity: A nonnegative integer maximum allowed total weight.

    Returns:
        The highest obtainable value without exceeding capacity. Unused
        capacity is allowed. Return zero if no item fits or capacity is zero.
        A single item contributes its value if it fits, otherwise zero.

    Mutation and assumptions:
        Neither input list is modified or sorted. Equal nonzero list lengths,
        positive weights and values, and nonnegative capacity are assumed
        and are not validated. Empty or mismatched lists and negative
        inputs are unsupported. Zero-weight items are outside the stated
        constraints; the zero-capacity entry stays zero for positive weights.

    Approach:
        Bottom-up Dynamic Programming (Tabulation) with rolling arrays.
        1. Read size and create prev_max_value_dp with capacity + 1 zeros.
           Its weight entry represents the best value fitting that allowed
           capacity using the items processed so far. The actual bag has
           the given capacity; smaller columns record answers needed when
           choosing an item leaves less space. Choosing nothing gives zero.
        2. Initialize the first item separately. For every allowed capacity
           from weights[0] through capacity, store values[0]. Smaller limits
           cannot fit it and stay zero. For weight 2, value 7, and capacity
           5, the row becomes [0, 0, 7, 7, 7, 7]. Each entry describes a
           different capacity limit, not another copy of the item. If the
           first item is too heavy, the loop does not run; no sorting is needed.
        3. Process the remaining items from index 1 onward. Create a fresh
           max_value_dp for each item and visit capacities 1 through the
           full limit. Leave capacity zero at zero. Keep prev_max_value_dp
           unchanged throughout this item so every read uses earlier items.
        4. Read not_pick from the previous row at the same capacity. This
           skips the current item while preserving the best earlier choice.
        5. Start picked at zero. If the item fits, add its value to the
           previous row at weight - weights[index], the remaining space.
           For weight 3, value 5, and allowed capacity 5, add 5 to the best
           earlier value fitting capacity 2. Using the previous row prevents
           taking the current item repeatedly, even with ascending capacities.
        6. Store max(not_pick, picked) in the current row. Choose between
           alternative selections rather than adding them. An invalid take
           value of zero is safe because skipping gives a nonnegative value.
        7. After every capacity is calculated, assign max_value_dp to
           prev_max_value_dp. This shares the completed list rather than
           copying it. The next iteration creates a fresh current row, so
           its writes cannot change the previous row; only two rows are needed.
        8. Return prev_max_value_dp[capacity]. If there is only one item,
           the outer loop never runs, but this initialized previous row
           still contains the answer. Do not rely on the current row existing.

    Time Complexity:
        O(N * (W + 1)), where N is the item count and W is capacity.
        Each item creates and fills a row of W + 1 entries with constant
        work per entry; first-item initialization takes at most O(W) work.

    Space Complexity:
        O(W + 1) extra space, excluding the input lists. At most two rows
        of W + 1 values are needed at once; other variables take constant
        space and no recursive call stack is used.
    """
    # Step 1: Store best values for every capacity limit in the previous row.
    size: int = len(weights)
    prev_max_value_dp: list[int] = [0] * (capacity + 1)

    # Step 2: The first item contributes its value at every limit where it fits.
    for weight in range(weights[0], capacity + 1):
        prev_max_value_dp[weight] = values[0]

    # Step 3: Build a fresh row per later item, keeping the previous row intact.
    for index in range(1, size):
        max_value_dp: list[int] = [0] * (capacity + 1)
        for weight in range(1, (capacity + 1)):
            # Step 4: Skip this item and reuse the best earlier value.
            not_pick: int = prev_max_value_dp[weight]
            # Step 5: Taking it adds its value to the best use of the space left.
            picked: int = 0
            if weights[index] <= weight:
                picked = values[index] + prev_max_value_dp[weight - weights[index]]
            # Step 6: Keep the better of taking and skipping this item.
            max_value_dp[weight] = max(not_pick, picked)
        # Step 7: Publish this item's row only after all capacities are complete.
        prev_max_value_dp = max_value_dp

    # Step 8: This row also exists when the input contains just one item.
    return prev_max_value_dp[capacity]


def solve() -> None:
    # Sample from the question.
    weights = [1, 2, 4, 5]
    values = [5, 4, 8, 6]
    capacity = 5
    expected = 13
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum size, weight, value, and capacity.
    weights = [1]
    values = [1]
    capacity = 1
    expected = 1
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item exactly fills the bag.
    weights = [5]
    values = [9]
    capacity = 5
    expected = 9
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item is too heavy by one.
    weights = [5]
    values = [9]
    capacity = 4
    expected = 0
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single item leaves unused capacity and cannot be reused.
    weights = [2]
    values = [7]
    capacity = 4
    expected = 7
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No item fits.
    weights = [4, 5]
    values = [10, 20]
    capacity = 3
    expected = 0
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All items fit exactly.
    weights = [1, 2, 3]
    values = [4, 5, 6]
    capacity = 6
    expected = 15
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Capacity exceeds the combined weight.
    weights = [1, 2, 3]
    values = [4, 5, 6]
    capacity = 10
    expected = 15
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Combination beats the highest-value individual item.
    weights = [2, 3, 5]
    values = [6, 8, 13]
    capacity = 5
    expected = 14
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item occurs first.
    weights = [2, 2, 2]
    values = [10, 3, 4]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item occurs in the middle.
    weights = [2, 2, 2]
    values = [3, 10, 4]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best item occurs last.
    weights = [2, 2, 2]
    values = [3, 4, 10]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate items are separate choices.
    weights = [2, 2, 2]
    values = [5, 5, 5]
    capacity = 4
    expected = 10
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal values with different weights.
    weights = [4, 2, 3]
    values = [7, 7, 7]
    capacity = 5
    expected = 14
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Leaving capacity unused gives the best value.
    weights = [3, 5]
    values = [10, 9]
    capacity = 5
    expected = 10
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Nonadjacent items give the best combination.
    weights = [2, 5, 3]
    values = [8, 9, 10]
    capacity = 5
    expected = 18
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An overweight valuable item must be skipped.
    weights = [6, 2, 3]
    values = [100, 4, 5]
    capacity = 5
    expected = 9
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best value-to-weight ratio alone is not sufficient.
    weights = [3, 4, 5]
    values = [7, 9, 10]
    capacity = 9
    expected = 19
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum single weight and value at exact capacity.
    weights = [50]
    values = [100]
    capacity = 50
    expected = 100
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum weight exceeds capacity by one.
    weights = [50]
    values = [100]
    capacity = 49
    expected = 0
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum capacity with a single item.
    weights = [50]
    values = [100]
    capacity = 1000
    expected = 100
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum item count with no fitting item.
    weights = [
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
    ]
    values = [
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
    ]
    capacity = 1
    expected = 0
    result = zero_one_knapsack_recursion(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: sample from the question.
    weights = [1, 2, 4, 5]
    values = [5, 4, 8, 6]
    capacity = 5
    expected = 13
    result = zero_one_knapsack_memoization(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: sample from the question.
    weights = [1, 2, 4, 5]
    values = [5, 4, 8, 6]
    capacity = 5
    expected = 13
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Sample from the question.
    weights = [1, 2, 4, 5]
    values = [5, 4, 8, 6]
    capacity = 5
    expected = 13
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum size, weight, value, and capacity.
    weights = [1]
    values = [1]
    capacity = 1
    expected = 1
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single item exactly fills the bag.
    weights = [5]
    values = [9]
    capacity = 5
    expected = 9
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single item is too heavy by one.
    weights = [5]
    values = [9]
    capacity = 4
    expected = 0
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single item leaves unused capacity and cannot be reused.
    weights = [2]
    values = [7]
    capacity = 4
    expected = 7
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: No item fits.
    weights = [4, 5]
    values = [10, 20]
    capacity = 3
    expected = 0
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All items fit exactly.
    weights = [1, 2, 3]
    values = [4, 5, 6]
    capacity = 6
    expected = 15
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Capacity exceeds the combined weight.
    weights = [1, 2, 3]
    values = [4, 5, 6]
    capacity = 10
    expected = 15
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Combination beats the highest-value individual item.
    weights = [2, 3, 5]
    values = [6, 8, 13]
    capacity = 5
    expected = 14
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Best item occurs first.
    weights = [2, 2, 2]
    values = [10, 3, 4]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Best item occurs in the middle.
    weights = [2, 2, 2]
    values = [3, 10, 4]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Best item occurs last.
    weights = [2, 2, 2]
    values = [3, 4, 10]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Duplicate items are separate choices.
    weights = [2, 2, 2]
    values = [5, 5, 5]
    capacity = 4
    expected = 10
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Equal values with different weights.
    weights = [4, 2, 3]
    values = [7, 7, 7]
    capacity = 5
    expected = 14
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Leaving capacity unused gives the best value.
    weights = [3, 5]
    values = [10, 9]
    capacity = 5
    expected = 10
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Nonadjacent items give the best combination.
    weights = [2, 5, 3]
    values = [8, 9, 10]
    capacity = 5
    expected = 18
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: An overweight valuable item must be skipped.
    weights = [6, 2, 3]
    values = [100, 4, 5]
    capacity = 5
    expected = 9
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Best value-to-weight ratio alone is not sufficient.
    weights = [3, 4, 5]
    values = [7, 9, 10]
    capacity = 9
    expected = 19
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum single weight and value at exact capacity.
    weights = [50]
    values = [100]
    capacity = 50
    expected = 100
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum weight exceeds capacity by one.
    weights = [50]
    values = [100]
    capacity = 49
    expected = 0
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum capacity with a single item.
    weights = [50]
    values = [100]
    capacity = 1000
    expected = 100
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum item count with no fitting item.
    weights = [
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
    ]
    values = [
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
    ]
    capacity = 1
    expected = 0
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: largest first item does not fit but later items do.
    weights = [50, 2, 3]
    values = [100, 7, 8]
    capacity = 5
    expected = 15
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: first item value persists when capacity is larger than its weight.
    weights = [2]
    values = [7]
    capacity = 5
    expected = 7
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: first item uses leftover capacity after taking a later item.
    weights = [2, 3]
    values = [7, 8]
    capacity = 6
    expected = 15
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: maximum item count and value with enough capacity for everything.
    weights = [1] * 100
    values = [100] * 100
    capacity = 1000
    expected = 10000
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: maximum item count, weight, value, and capacity.
    weights = [50] * 100
    values = [100] * 100
    capacity = 1000
    expected = 2000
    result = zero_one_knapsack_tabulation(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: sample from the question.
    weights = [1, 2, 4, 5]
    values = [5, 4, 8, 6]
    capacity = 5
    expected = 13
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: sample from the question.
    weights = [1, 2, 4, 5]
    values = [5, 4, 8, 6]
    capacity = 5
    expected = 13
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Sample from the question.
    weights = [1, 2, 4, 5]
    values = [5, 4, 8, 6]
    capacity = 5
    expected = 13
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum size, weight, value, and capacity.
    weights = [1]
    values = [1]
    capacity = 1
    expected = 1
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single item exactly fills the bag.
    weights = [5]
    values = [9]
    capacity = 5
    expected = 9
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single item is too heavy by one.
    weights = [5]
    values = [9]
    capacity = 4
    expected = 0
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single item leaves unused capacity and cannot be reused.
    weights = [2]
    values = [7]
    capacity = 4
    expected = 7
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: No item fits.
    weights = [4, 5]
    values = [10, 20]
    capacity = 3
    expected = 0
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: All items fit exactly.
    weights = [1, 2, 3]
    values = [4, 5, 6]
    capacity = 6
    expected = 15
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Capacity exceeds the combined weight.
    weights = [1, 2, 3]
    values = [4, 5, 6]
    capacity = 10
    expected = 15
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Combination beats the highest-value individual item.
    weights = [2, 3, 5]
    values = [6, 8, 13]
    capacity = 5
    expected = 14
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Best item occurs first.
    weights = [2, 2, 2]
    values = [10, 3, 4]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Best item occurs in the middle.
    weights = [2, 2, 2]
    values = [3, 10, 4]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Best item occurs last.
    weights = [2, 2, 2]
    values = [3, 4, 10]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Duplicate items are separate choices.
    weights = [2, 2, 2]
    values = [5, 5, 5]
    capacity = 4
    expected = 10
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Equal values with different weights.
    weights = [4, 2, 3]
    values = [7, 7, 7]
    capacity = 5
    expected = 14
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Leaving capacity unused gives the best value.
    weights = [3, 5]
    values = [10, 9]
    capacity = 5
    expected = 10
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Nonadjacent items give the best combination.
    weights = [2, 5, 3]
    values = [8, 9, 10]
    capacity = 5
    expected = 18
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: An overweight valuable item must be skipped.
    weights = [6, 2, 3]
    values = [100, 4, 5]
    capacity = 5
    expected = 9
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Best value-to-weight ratio alone is not sufficient.
    weights = [3, 4, 5]
    values = [7, 9, 10]
    capacity = 9
    expected = 19
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum single weight and value at exact capacity.
    weights = [50]
    values = [100]
    capacity = 50
    expected = 100
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum weight exceeds capacity by one.
    weights = [50]
    values = [100]
    capacity = 49
    expected = 0
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum capacity with a single item.
    weights = [50]
    values = [100]
    capacity = 1000
    expected = 100
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum item count with no fitting item.
    weights = [
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
    ]
    values = [
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
    ]
    capacity = 1
    expected = 0
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: largest first item does not fit but later items do.
    weights = [50, 2, 3]
    values = [100, 7, 8]
    capacity = 5
    expected = 15
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: first item value persists when capacity is larger than its weight.
    weights = [2]
    values = [7]
    capacity = 5
    expected = 7
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: first item uses leftover capacity after taking a later item.
    weights = [2, 3]
    values = [7, 8]
    capacity = 6
    expected = 15
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: maximum item count and value with enough capacity for everything.
    weights = [1] * 100
    values = [100] * 100
    capacity = 1000
    expected = 10000
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: maximum item count, weight, value, and capacity.
    weights = [50] * 100
    values = [100] * 100
    capacity = 1000
    expected = 2000
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: a later item must not be selected twice.
    weights = [5, 2]
    values = [1, 7]
    capacity = 4
    expected = 7
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: a later weight-one item can be selected only once.
    weights = [3, 1]
    values = [4, 3]
    capacity = 2
    expected = 3
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Minimum single item.
    weights = [1]
    values = [1]
    capacity = 1
    expected = 1
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Single item below available capacity.
    weights = [2]
    values = [7]
    capacity = 5
    expected = 7
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Single item exceeds capacity.
    weights = [50]
    values = [100]
    capacity = 49
    expected = 0
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Three-item walkthrough.
    weights = [2, 3, 4]
    values = [4, 5, 7]
    capacity = 5
    expected = 9
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Later item cannot be reused.
    weights = [5, 2]
    values = [1, 7]
    capacity = 4
    expected = 7
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Later weight-one item cannot be reused.
    weights = [3, 1]
    values = [4, 3]
    capacity = 2
    expected = 3
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Largest first item is skipped.
    weights = [50, 2, 3]
    values = [100, 7, 8]
    capacity = 5
    expected = 15
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: All items fit with spare capacity.
    weights = [1, 2, 3]
    values = [4, 5, 6]
    capacity = 10
    expected = 15
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Identical items remain separate choices.
    weights = [2, 2, 2]
    values = [5, 5, 5]
    capacity = 4
    expected = 10
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Best value first.
    weights = [2, 2, 2]
    values = [10, 3, 4]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Best value in middle.
    weights = [2, 2, 2]
    values = [3, 10, 4]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Best value last.
    weights = [2, 2, 2]
    values = [3, 4, 10]
    capacity = 2
    expected = 10
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: No items fit.
    weights = [4, 5]
    values = [10, 20]
    capacity = 3
    expected = 0
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Exact capacity from nonadjacent items.
    weights = [2, 5, 3]
    values = [8, 9, 10]
    capacity = 5
    expected = 18
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Maximum capacity with one item.
    weights = [50]
    values = [100]
    capacity = 1000
    expected = 100
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Maximum count with minimum weights and maximum values.
    weights = [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    ]
    values = [
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
    ]
    capacity = 1000
    expected = 10000
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Maximum count weights values and capacity.
    weights = [
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
    ]
    values = [
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
    ]
    capacity = 1000
    expected = 2000
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-row space optimization: Maximum count with minimum capacity and no fit.
    weights = [
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
    ]
    values = [
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
    ]
    capacity = 1
    expected = 0
    result = zero_one_knapsack_tabulation_space_optimized(weights, values, capacity)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
