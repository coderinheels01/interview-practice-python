"""121. Best Time to Buy and Sell Stock

Difficulty: Easy

You are given an array ``prices`` where ``prices[i]`` is the price of a given
stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and
choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot
achieve any profit, return 0.

Example 1:
    Input: prices = [7, 1, 5, 3, 6, 4]
    Output: 5
    Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6),
    for a profit of 6 - 1 = 5. Buying on day 2 and selling on day 1 is not
    allowed because you must buy before you sell.

Example 2:
    Input: prices = [7, 6, 4, 3, 1]
    Output: 0
    Explanation: No transactions are made, so the maximum profit is 0.

Constraints:
    - 1 <= prices.length <= 10^5
    - 0 <= prices[i] <= 10^4
"""


def max_profit(prices: list[int]) -> int:
    """Return the largest profit from one buy followed by one sale.

    Approach: Two-Pointer Greedy Algorithm
        1. Record the number of prices and return 0 when the list is empty.
        2. Start the buying pointer on the first day, the selling pointer on
           the second day, and the maximum profit at 0.
        3. Calculate the profit for the current buy and sell days while both
           pointers remain within the list.
        4. If the current profit is negative, advance the buying pointer to
           search for a lower buying price. Otherwise, update the maximum
           profit and advance the selling pointer to try a later selling day.
        5. Return the largest profit found. It remains 0 when no profitable
           transaction exists.

    Time Complexity:
        O(n), where n is the number of prices. Every loop iteration advances
        either the buying pointer or the selling pointer, and neither pointer
        advances more than n times.

    Space Complexity:
        O(1), because the algorithm uses a fixed number of integer variables
        regardless of the number of prices.

    https://www.youtube.com/watch?v=1pkOgXD63yU&t=127s
    """
    # 1. Record the input size and handle an empty list.
    n: int = len(prices)

    if n < 1:
        return 0

    # 2. Initialize the buy and sell pointers and the maximum profit.
    buying_price_index: int = 0
    selling_price_index: int = 1
    max_profit: int = 0

    # 3. Compare candidate days while both pointers remain in bounds.
    while buying_price_index < n and selling_price_index < n:
        current_profit: int = prices[selling_price_index] - prices[buying_price_index]

        # 4. Move the buying pointer after a loss; otherwise, record the
        # profit and move the selling pointer forward.
        if current_profit < 0:
            buying_price_index = selling_price_index
        else:
            max_profit = max(max_profit, current_profit)
            selling_price_index += 1

    # 5. Return the best profit, or 0 when no profitable trade exists.
    return max_profit

def max_profit2(prices: list[int]) -> int:
    """Return the largest profit from one buy followed by one later sale.

    The input is expected to contain at least one price, as guaranteed by the
    problem constraints. The function returns 0 when no profitable transaction
    exists and does not modify ``prices``.

    Approach: One-Pass Greedy Algorithm with a Running Minimum
        1. Initialize the maximum profit and current profit to 0. Treat the
           first day's price as the minimum buying price seen so far, and store
           the number of days.
        2. Traverse each day after the first from left to right.
        3. Calculate the profit from selling on the current day after buying at
           the minimum price from an earlier day.
        4. Update the maximum profit when the current transaction is better.
        5. Update the running minimum price so later days can use the cheapest
           buying opportunity seen so far.
        6. Return the maximum profit. It remains 0 if prices never increase
           after a potential buying day.

    Args:
        prices: A non-empty list in which each value is a stock price for one
            consecutive day.

    Returns:
        The greatest profit available from one buy and one later sale, or 0
        when no profitable transaction exists.

    Mutation Behavior:
        The function reads ``prices`` without modifying it.

    Why This Is Better Than ``max_profit``:
        Both functions take O(n) time and O(1) space, but this version has more
        direct control flow. It processes every day after the first exactly once
        while maintaining one running minimum. ``max_profit`` manages separate
        buy and sell pointers and performs an additional equal-index iteration
        after discovering a lower buying price. This version is therefore
        easier to trace and reason about, although ``max_profit`` additionally
        handles an empty list while this function relies on the non-empty-input
        constraint.

    Time Complexity:
        O(n), where n is the number of prices. The loop visits every day after
        the first exactly once and performs constant-time work per day.

    Space Complexity:
        O(1) auxiliary space because only a fixed number of integer variables
        are stored regardless of the number of prices.
    """
    # Step 1: Initialize profit tracking, the running minimum, and input size.
    max_profit: int = 0
    current_profit = 0
    min_price: int = prices[0]
    size: int = len(prices)

    # Step 2: Process every possible selling day after the first day.
    for day in range(1, size):
        # Step 3: Calculate profit using the cheapest earlier buying price.
        current_profit = prices[day] - min_price

        # Step 4: Preserve the best profitable transaction found so far.
        max_profit = max(current_profit, max_profit)

        # Step 5: Track the cheapest price for future selling days.
        min_price = min(min_price, prices[day])

    # Step 6: Return the best profit, or 0 if no profitable trade exists.
    return max_profit


def solve() -> None:
    # prices = [7, 1, 5, 3, 6, 4]
    #
    # expected = 5
    # result = max_profit(prices)
    #
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # prices = [7, 6, 4, 3, 1]
    #
    # expected = 0
    # result = max_profit(prices)
    #
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # prices = [1]
    #
    # expected = 0
    # result = max_profit(prices)
    #
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # prices = [3, 3, 3, 3]
    #
    # expected = 0
    # result = max_profit(prices)
    #
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # prices = [1, 2, 3, 4, 5]
    #
    # expected = 4
    # result = max_profit(prices)
    #
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # prices = [2, 4, 1, 10]
    #
    # expected = 9
    # result = max_profit(prices)
    #
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    prices: list[int] = [7, 1, 5, 3, 6, 4]

    expected: int = 5
    result: int = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [7, 6, 4, 3, 1]

    expected = 0
    result = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [1]

    expected = 0
    result = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [3, 3, 3, 3]

    expected = 0
    result = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [1, 2, 3, 4, 5]

    expected = 4
    result = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [2, 4, 1, 10]

    expected = 9
    result = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [3, 1, 1, 5]

    expected = 4
    result = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [5, 1, 6, 0, 2]

    expected = 5
    result = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [0, 10_000]

    expected = 10_000
    result = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [10_000, 0]

    expected = 0
    result = max_profit2(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [10_000] + [0] * 99_998 + [10_000]

    expected = 10_000
    result = max_profit2(prices)

    assert result == expected
    print("Expected: maximum profit of 10,000 across 100,000 days")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
