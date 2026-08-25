"""Pascal's Triangle III

Given an integer ``rows``, return the first ``rows`` rows of Pascal's Triangle.

In Pascal's Triangle:

- The first row contains a single element, 1.
- Each row has one more element than the previous row.
- Every row starts and ends with 1.
- Every interior value is the sum of the two values directly above it in the
  previous row.

Example 1:
    Input: rows = 5
    Output: [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1],
             [1, 4, 6, 4, 1]]

    Explanation: The first five rows of Pascal's Triangle are:

            1
           1 1
          1 2 1
         1 3 3 1
        1 4 6 4 1

Example 2:
    Input: rows = 1
    Output: [[1]]

Constraints:
    - 1 <= rows <= 30
    - All values fit inside a 32-bit integer.

https://www.youtube.com/watch?v=bR7mQgwQ_o8&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=19
"""


def generate_row(row: int) -> list[int]:
    # 3a. Start the requested row with its first coefficient, 1.
    answer: int = 1
    row_result: list[int] = [1]

    # 3b. Visit each remaining column in the requested row.
    for col in range(1, row):
        # 3c. Calculate this coefficient from the preceding coefficient.
        answer *= row - col
        answer //= col

        # 3d. Add the calculated coefficient to the requested row.
        row_result.append(answer)

    # 3e. Return the completed row to the triangle-generating function.
    return row_result


def generate_pascals_triangle(rows: int) -> list[list[int]]:
    """Return the first ``rows`` rows of Pascal's Triangle.

    Approach:
        Delegate the construction of each row to ``generate_row``, which uses
        consecutive Binomial Coefficients. A 1-indexed Pascal row ``row``
        contains:

            (row - 1)C0, (row - 1)C1, ..., (row - 1)C(row - 1)

        Each coefficient can be calculated from the preceding coefficient:

            next_value = current_value * (row - col) // col

        This avoids factorial calculations and builds each value in constant
        time once the preceding value is known.

        1. Create the outer result list that will contain every generated row.
        2. Iterate through every requested 1-indexed row number, from 1 through
           ``rows``.
        3. Call ``generate_row`` for the current row number. The helper starts
           a new row with 1, derives every remaining coefficient from the
           preceding coefficient using the formula above, and returns the
           completed row. Because the helper initializes its own ``answer``
           and ``row_result``, each row is generated independently.
        4. Append the completed row returned by the helper to the triangle.
        5. Return the complete triangle after all requested rows are generated.

    Parameters:
        rows: The number of Pascal's Triangle rows to generate, starting with
        the first row.

    Returns:
        A new two-dimensional list containing the first ``rows`` rows of
        Pascal's Triangle.

    Mutation:
        The integer argument is not mutated. The function creates and returns
        a new nested list.

    Time Complexity:
        O(rows^2). ``generate_row`` takes O(row) time for a given row, so the
        total work is ``1 + 2 + ... + rows``, which is O(rows^2).

    Space Complexity:
        O(rows^2) for the returned triangle. Each helper-created ``row_result``
        becomes part of that returned triangle. Excluding the required output,
        the helper and outer function use O(1) auxiliary space.

    Assumptions:
        ``1 <= rows <= 30``, as guaranteed by the problem constraints. Python
        integers safely hold intermediate multiplication results.
    """

    # 1. Create the outer list that will hold every generated row.
    result: list[list[int]] = []

    # 2. Iterate through each requested 1-indexed row number.
    for row in range(1, rows + 1):
        # 3. Delegate construction of the current row to the helper.
        row_result = generate_row(row)

        # 4. Add the completed row to the triangle.
        result.append(row_result)

    # 5. Return the complete Pascal's Triangle.
    return result


def solve() -> None:
    rows: int = 5

    expected: list[list[int]] = [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
    ]
    result: list[list[int]] = generate_pascals_triangle(rows)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    rows = 1

    expected = [[1]]
    result = generate_pascals_triangle(rows)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    rows = 2

    expected = [[1], [1, 1]]
    result = generate_pascals_triangle(rows)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    rows = 3

    expected = [[1], [1, 1], [1, 2, 1]]
    result = generate_pascals_triangle(rows)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    rows = 6

    expected = [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1],
    ]
    result = generate_pascals_triangle(rows)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    rows = 30

    expected = 30
    result = len(generate_pascals_triangle(rows))
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    rows = 30

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
    result = generate_pascals_triangle(rows)[-1]
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
