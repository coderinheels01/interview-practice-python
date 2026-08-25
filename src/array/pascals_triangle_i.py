"""Pascal's Triangle I

Given two integers ``r`` and ``c``, return the value at the ``r``-th row and
``c``-th column of Pascal's Triangle. Both row and column positions are
1-indexed.

In Pascal's Triangle:

- The first row contains a single element, 1.
- Each row has one more element than the previous row.
- Every row starts and ends with 1.
- Every interior value is the sum of the two values directly above it in the
  previous row:

      Pascal[r][c] = Pascal[r - 1][c - 1] + Pascal[r - 1][c]

  The formula uses 1-based indexing.

Example 1:
    Input: r = 4, c = 2
    Output: 3

    Explanation: Pascal's Triangle begins as follows:

        1
        1 1
        1 2 1
        1 3 3 1

    The value at row 4 and column 2 is 3.

Example 2:
    Input: r = 5, c = 3
    Output: 6

    Explanation: Pascal's Triangle begins as follows:

        1
        1 1
        1 2 1
        1 3 3 1
        1 4 6 4 1

    The value at row 5 and column 3 is 6.

Constraints:
    - 1 <= r, c <= 30
    - c <= r
    - All values fit inside a 32-bit integer.
"""


def get_pascals_triangle_value(row: int, col: int) -> int:
    """Return the value at a 1-indexed position in Pascal's Triangle.

    Approach:
        Use the Binomial Coefficient formula. The values in Pascal's Triangle
        correspond to combinations:

            Pascal position (row, col) = (row - 1) C (col - 1)

        The subtraction is necessary because the problem numbers rows and
        columns starting at 1, while the combination sequence starts at 0. For
        example, row 5 contains the coefficients for ``4C0`` through ``4C4``,
        so row 5, column 3 is ``4C2 = 6``.

        Rather than calculate three complete factorials, build the combination
        value incrementally:

            nCr = (n / 1) * ((n - 1) / 2) * ... * ((n - r + 1) / r)

        1. Initialize ``result`` to 1, the multiplicative starting value.
        2. Convert the 1-indexed column and row into the zero-indexed
           combination values ``r = col - 1`` and ``n = row - 1``.
        3. Iterate ``r`` times to include each factor required by ``nCr``.
        4. During each iteration, multiply by the next decreasing numerator
           and divide by the next increasing denominator. The intermediate
           result remains an integer for this ordering of the calculation.
        5. Return the completed binomial coefficient.

    Parameters:
        row: The 1-indexed Pascal's Triangle row.
        col: The 1-indexed column within that row.

    Returns:
        The integer value at the requested position.

    Mutation:
        The arguments are integers and are not mutated. ``row`` and ``col``
        are reassigned only inside the function, so the caller is unaffected.

    Time Complexity:
        O(col), because the loop performs ``col - 1`` iterations. Since
        ``col <= row``, this can also be bounded by O(row).

    Space Complexity:
        O(1) additional space because only integer variables are stored.

    Assumptions:
        ``1 <= col <= row <= 30``, as guaranteed by the problem constraints.
        Python integers also avoid fixed-width overflow during intermediate
        multiplication.

    https://www.youtube.com/watch?v=bR7mQgwQ_o8&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=19
    """

    # 1. Initialize the multiplicative result.
    result: int = 1

    # 2. Convert 1-indexed Pascal coordinates to nCr coordinates.
    col = col - 1
    row = row - 1

    # 3. Process each of the r factors in the binomial coefficient.
    for num in range(col):
        # 4. Multiply by the numerator factor, then divide by the denominator.
        result *= row - num
        result //= num + 1

    # 5. Return the value at the requested Pascal position.
    return result


def solve() -> None:
    r: int = 4
    c: int = 2
    expected: int = 3
    result: int = get_pascals_triangle_value(r, c)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    r = 5
    c = 3

    expected = 6
    result = get_pascals_triangle_value(r, c)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    r = 1
    c = 1
    expected = 1
    result = get_pascals_triangle_value(r, c)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    r = 5
    c = 1
    expected = 1
    result = get_pascals_triangle_value(r, c)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    r = 5
    c = 5
    expected = 1
    result = get_pascals_triangle_value(r, c)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    r = 6
    c = 4
    expected = 10
    result = get_pascals_triangle_value(r, c)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    r = 30
    c = 15
    expected = 77_558_760
    result = get_pascals_triangle_value(r, c)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    r = 30
    c = 1
    expected = 1
    result = get_pascals_triangle_value(r, c)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    r = 30
    c = 30
    expected = 1
    result = get_pascals_triangle_value(r, c)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
