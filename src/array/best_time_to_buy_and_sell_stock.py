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


def solve() -> None:
    prices = [7, 1, 5, 3, 6, 4]

    expected = 5
    result = max_profit(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [7, 6, 4, 3, 1]

    expected = 0
    result = max_profit(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [1]

    expected = 0
    result = max_profit(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [3, 3, 3, 3]

    expected = 0
    result = max_profit(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [1, 2, 3, 4, 5]

    expected = 4
    result = max_profit(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    prices = [2, 4, 1, 10]

    expected = 9
    result = max_profit(prices)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
