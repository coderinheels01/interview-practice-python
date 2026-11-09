"""House Robber II (Circular Houses)

A robber plans to rob houses on a street. Each house has security measures
that alert the police if two adjacent houses are robbed.

The houses are arranged in a circle, so the first and last houses are also
adjacent. Given an integer list money, where money[i] is the amount available
in the (i + 1)th house, return the maximum amount the robber can loot without
alerting the police.

Example 1:
    Input: money = [2, 1, 4, 9]
    Output: 10
    Explanation:
        Rob the second and fourth houses: 1 + 9 = 10.
        The first and fourth houses cannot both be robbed because they
        are adjacent in the circle.

Example 2:
    Input: money = [1, 5, 2, 1, 6]
    Output: 11
    Explanation:
        Rob the second and fifth houses: 5 + 6 = 11.
        These houses are not adjacent, including across the circle's ends.

Now Your Turn:
    Input: money = [9, 4, 1, 8]
    Find the maximum amount that can be looted without robbing adjacent houses.

Constraints:
    Numeric constraints were not provided in the supplied question.

https://www.youtube.com/watch?v=3WaxQMELSkw&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=7
"""


def rob(from_index: int, to_index: int, money: list[int]) -> int:
    """Find the maximum loot from a straight, nonempty range of houses.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. Start one_index_back with the first house's money. Start
           two_index_back at 0 because no earlier house has been considered.
        2. Visit the remaining houses in the range. Consider skipping the
           current house: keep the best loot through the previous house.
        3. Consider taking the current house: add its money to the best loot
           from two houses back. This excludes its immediate neighbor.
        4. Move the saved answers forward. Preserve the old one_index_back
           in two_index_back, then save the larger take-or-skip total in
           one_index_back. Neither variable means a house was definitely
           robbed; each holds the best total through an earlier position.
        5. Return one_index_back, the best loot for the entire range.

    Parameters:
        from_index: First included house index.
        to_index: End boundary, excluded from the range.
        money: Nonnegative amounts available in the houses.

    Returns:
        Maximum loot without selecting adjacent houses within the linear
        range. A one-house range returns that house's money.

    Mutation Behavior:
        Reads money without modifying it or creating a slice.

    Time Complexity: O(m)
        Here m is to_index - from_index. Each house in the range is visited
        once, with a fixed amount of work per visit.

    Space Complexity: O(1)
        Only a few variables are kept. The input money list is excluded
        from extra space.

    Assumptions:
        0 <= from_index < to_index <= len(money), so the range is nonempty.
        Houses in this range are treated as a line. Values are nonnegative,
        and arithmetic is treated as constant cost.
    """
    # Step 1: Save the starting answer and the empty earlier total.
    one_index_back: int = money[from_index]
    two_index_back: int = 0

    # Step 2: Visit the remaining houses, considering skipping each one.
    for index in range(from_index + 1, to_index):
        not_take: int = 0 + one_index_back
        # Step 3: Taking this house excludes its immediate neighbor.
        take: int = money[index] + two_index_back

        # Step 4: Preserve the earlier answer, then save the better total.
        two_index_back = one_index_back
        one_index_back = max(take, not_take)

    # Step 5: Return the best loot for this whole range.
    return one_index_back


def house_robber_ii(money: list[int]) -> int:
    """Return the maximum loot from circular houses without adjacent robberies.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. If there is one house, return its money. There is no different
           neighboring house to exclude in this case.
        2. Solve the straight range that excludes the first house. rob(1,
           size, money) includes indexes 1 through size - 1. This allows
           choosing the last house without conflicting with the first.
        3. Solve the straight range that excludes the last house. rob(0,
           size - 1, money) includes indexes 0 through size - 2. This allows
           choosing the first house without conflicting with the last.
        4. Return the larger answer. Every valid circular selection must
           exclude the first house or the last house, possibly both. These
           two cases therefore cover all valid selections. The helper can
           still skip either endpoint; excluding one does not force the other.

        Example: money = [2, 1, 4, 9].
            Exclude first: consider [1, 4, 9], whose best loot is 1 + 9 = 10.
            Exclude last: consider [2, 1, 4], whose best loot is 2 + 4 = 6.
            Return max(10, 6) = 10. These lists illustrate the ranges;
            the implementation passes indexes and does not create slices.

    Parameters:
        money: A nonempty list of nonnegative amounts, in circular order.

    Returns:
        Maximum loot without robbing adjacent houses, including the first
        and last houses together. Returns 0 if all amounts are zero.

    Mutation Behavior:
        Does not modify money or create copies of its ranges.

    Time Complexity: O(n)
        Here n is len(money). Two linear passes take O(n) + O(n) = O(n)
        time. The single-house case takes O(1).

    Space Complexity: O(1)
        The two helper calls run sequentially and use only a few variables.
        No slices or growing tables are created; the input list is excluded.

    Assumptions:
        money is nonempty and contains nonnegative values. Numeric upper
        limits were not provided; arithmetic is treated as constant cost.
    """
    size: int = len(money)
    # Step 1: Handle the single house before creating two nonempty ranges.
    if size == 1:
        return money[0]
    # Step 2: Find the best loot with the first house excluded.
    without_first: int = rob(from_index=1, to_index=size, money=money)
    # Step 3: Find the best loot with the last house excluded.
    without_last: int = rob(from_index=0, to_index=size - 1, money=money)

    # Step 4: Choose the better of the two valid circular cases.
    return max(without_first, without_last)


def solve() -> None:
    money: list[int] = [2, 1, 4, 9]
    expected: int = 10
    result: int = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single house.
    money = [5]
    expected = 5
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single house with no money.
    money = [0]
    expected = 0
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two adjacent houses; choose last.
    money = [2, 9]
    expected = 9
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two adjacent houses; choose first.
    money = [9, 2]
    expected = 9
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two equal houses.
    money = [5, 5]
    expected = 5
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Three houses are all mutually adjacent.
    money = [2, 3, 2]
    expected = 3
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First and last cannot both be robbed.
    money = [10, 1, 1, 10]
    expected = 11
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First question example.
    money = [2, 1, 4, 9]
    expected = 10
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example.
    money = [1, 5, 2, 1, 6]
    expected = 11
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Your turn example.
    money = [9, 4, 1, 8]
    expected = 12
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All zeros.
    money = [0, 0, 0, 0]
    expected = 0
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even number of equal houses.
    money = [5, 5, 5, 5]
    expected = 10
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd number of equal houses.
    money = [5, 5, 5, 5, 5]
    expected = 10
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Increasing values.
    money = [1, 2, 3, 4, 5]
    expected = 8
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Decreasing values.
    money = [5, 4, 3, 2, 1]
    expected = 8
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best selection includes first house.
    money = [1, 10, 1, 1]
    expected = 11
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best selection includes last house.
    money = [1, 1, 10, 1]
    expected = 11
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Best selection excludes both endpoints.
    money = [1, 10, 1, 10, 1]
    expected = 20
    result = house_robber_ii(money)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
