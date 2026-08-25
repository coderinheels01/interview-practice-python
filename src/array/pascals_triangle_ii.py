"""Pascal's Triangle II

Given an integer ``row``, return the complete ``row``-th row of Pascal's
Triangle. The row number is 1-indexed.

In Pascal's Triangle:

- The first row contains a single element, 1.
- Each row has one more element than the previous row.
- Every row starts and ends with 1.
- Every interior value is the sum of the two values directly above it in the
  previous row.

Example 1:
    Input: row = 4
    Output: [1, 3, 3, 1]

    Explanation: Pascal's Triangle begins as follows:

        1
        1 1
        1 2 1
        1 3 3 1

    Therefore, the fourth row is [1, 3, 3, 1].

Example 2:
    Input: row = 5
    Output: [1, 4, 6, 4, 1]

Constraints:
    - 1 <= row <= 30
    - All values fit inside a 32-bit integer.

    https://www.youtube.com/watch?v=bR7mQgwQ_o8&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=19
"""


def get_pascals_triangle_print_row(row: int) -> list[int]:
    """Return the complete 1-indexed row of Pascal's Triangle.

    Approach:
        Generate the row using consecutive Binomial Coefficients. Pascal row
        ``row`` contains the following values:

            (row - 1)C0, (row - 1)C1, ..., (row - 1)C(row - 1)

        The first value is always 1. Each following value can be calculated
        from the previous value without computing factorials:

            next_value = current_value * (row - position) // position

        For example, row 5 begins with 1. Its following values are:

            1 * 4 // 1 = 4
            4 * 3 // 2 = 6
            6 * 2 // 3 = 4
            4 * 1 // 4 = 1

        1. Store the requested row length in ``col``.
        2. Initialize the current coefficient to 1 and place that first value
           in the result list.
        3. Iterate through the remaining positions from 1 through ``row - 1``.
        4. Calculate the coefficient at each position from the previous one by
           multiplying by the next decreasing numerator and dividing by the
           current position.
        5. Append each completed coefficient to the result list.
        6. Return the complete row.

    Parameters:
        row: The 1-indexed row of Pascal's Triangle to generate.

    Returns:
        A new list containing every integer in the requested row from left to
        right.

    Mutation:
        The integer argument is not mutated. A new result list is created.

    Time Complexity:
        O(row), because the function calculates and appends exactly ``row``
        coefficients.

    Space Complexity:
        O(row) for the returned list. Excluding the required output, the
        function uses O(1) auxiliary space for integer variables.

    Assumptions:
        ``1 <= row <= 30``, as guaranteed by the problem constraints. Python
        integers safely handle the intermediate multiplication values.
    """

    # 1. Store the number of values required in the requested row.
    col: int = row

    # 2. Initialize and record the first coefficient, which is always 1.
    answer: int = 1
    result: list[int] = [answer]

    # 3. Visit every remaining position in the row.
    for num in range(1, col):
        # 4. Derive this coefficient from the preceding coefficient.
        answer *= row - num
        answer //= num
        print(f"num + 1 {num + 1}")

        # 5. Add the completed coefficient to the row.
        result.append(answer)

    # 6. Return the complete Pascal row.
    return result


def solve() -> None:
    row: int = 4

    expected: list[int] = [1, 3, 3, 1]
    result: list[int] = get_pascals_triangle_print_row(row)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    row = 1

    expected = [1]
    result = get_pascals_triangle_print_row(row)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    row = 2

    expected = [1, 1]
    result = get_pascals_triangle_print_row(row)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    row = 3

    expected = [1, 2, 1]
    result = get_pascals_triangle_print_row(row)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    row = 5

    expected = [1, 4, 6, 4, 1]
    result = get_pascals_triangle_print_row(row)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    row = 6

    expected = [1, 5, 10, 10, 5, 1]
    result = get_pascals_triangle_print_row(row)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    row = 30

    expected = [
        1,
        29,
        406,
        3654,
        23751,
        118755,
        475020,
        1560780,
        4292145,
        10015005,
        20030010,
        34597290,
        51895935,
        67863915,
        77558760,
        77558760,
        67863915,
        51895935,
        34597290,
        20030010,
        10015005,
        4292145,
        1560780,
        475020,
        118755,
        23751,
        3654,
        406,
        29,
        1,
    ]
    result = get_pascals_triangle_print_row(row)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
