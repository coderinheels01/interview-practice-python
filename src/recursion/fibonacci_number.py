"""509. Fibonacci Number

Source: https://leetcode.com/problems/fibonacci-number/

The Fibonacci sequence begins with 0 and 1. Every later value equals the sum
of the two values immediately before it. Its definition is:

    F(0) = 0
    F(1) = 1
    F(n) = F(n - 1) + F(n - 2) for n > 1

For an integer n, return the value of F(n).

Example 1:
    Input: n = 2
    Output: 1
    Explanation: Adding F(1) and F(0) gives 1 + 0 = 1.

Example 2:
    Input: n = 3
    Output: 2
    Explanation: Adding F(2) and F(1) gives 1 + 1 = 2.

Example 3:
    Input: n = 4
    Output: 3
    Explanation: Adding F(3) and F(2) gives 2 + 1 = 3.

Constraints:
    - 0 <= n <= 30
"""


def fibonacci_number(n: int) -> int:
    """Return the Fibonacci number at the zero-based index ``n``.

    Approach: Naive Recursion
        1. Check the base cases: when n is 0 or 1, return n directly.
           These values terminate each branch of the recursion.
        2. For n greater than 1, recursively calculate F(n - 1), then
           F(n - 2). Each call applies the same base-case check and
           recurrence to a smaller index until it reaches 0 or 1.
        3. Add the two returned values and return their sum as F(n).
           For example, F(3) combines F(2) = 1 and F(1) = 1 to return 2.
           Results are not cached, so overlapping subproblems such as
           F(2) are calculated repeatedly in different branches.

    Parameters:
        n: An integer index satisfying 0 <= n <= 30.

    Returns:
        The integer F(n), with F(0) = 0 and F(1) = 1.

    Mutation Behavior:
        The function does not modify its input or any external state.

    Time Complexity:
        O(2^n), an exponential upper bound; the tighter bound is
        Theta(phi^n), where phi = (1 + sqrt(5)) / 2. Each non-base call
        makes two recursive calls, giving the recurrence
        T(n) = T(n - 1) + T(n - 2) + O(1). Repeated computation of the
        same subproblems causes the exponential growth. Arithmetic is
        treated as O(1) for the bounded integers in the stated constraints.
        The two base cases take O(1) time.

    Space Complexity:
        O(n) auxiliary space for the recursion stack. The longest active
        path repeatedly decreases the index by 1 until reaching a base
        case. Each frame stores its index, constant bookkeeping, and at
        most one completed child result while the other child runs.
        The branches run sequentially, so the entire recursion tree is
        never stored at once. No cache or additional collection is used.
        The base cases use O(1) space.

    Assumptions:
        Inputs satisfy the stated integer range; no validation is performed.
        Python must have enough available recursion depth for the active
        call chain, which has at most 30 function frames for this range.
    """
    # Step 1: Return the known value for either base case.
    if n <= 1:
        return n
    # Steps 2 and 3: Compute both preceding values and return their sum.
    return fibonacci_number(n - 1) + fibonacci_number(n - 2)


def solve() -> None:
    # n: int = 2
    # expected: int = 1
    # result: int = fibonacci_number(n)

    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum input and zero base case.
    n: int = 0
    expected: int = 0
    result: int = fibonacci_number(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Upper boundary of the base case.
    n: int = 1
    expected: int = 1
    result: int = fibonacci_number(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First recursive case; both calls reach base cases.
    n: int = 2
    expected: int = 1
    result: int = fibonacci_number(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One recursive child and one base-case child.
    n: int = 3
    expected: int = 2
    result: int = fibonacci_number(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Both children use recursion.
    n: int = 4
    expected: int = 3
    result: int = fibonacci_number(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Typical even input.
    n: int = 10
    expected: int = 55
    result: int = fibonacci_number(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Typical odd input near the middle of the range.
    n: int = 15
    expected: int = 610
    result: int = fibonacci_number(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One below the maximum input.
    n: int = 29
    expected: int = 514229
    result: int = fibonacci_number(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum allowed input.
    n: int = 30
    expected: int = 832040
    result: int = fibonacci_number(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
