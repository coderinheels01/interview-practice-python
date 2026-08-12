"""238. Product of Array Except Self

Difficulty: Medium

Given an integer array ``nums``, return an array ``answer`` such that
``answer[i]`` is equal to the product of all the elements of ``nums`` except
``nums[i]``.

The product of any prefix or suffix of ``nums`` is guaranteed to fit in a
32-bit integer.

The algorithm must run in O(n) time without using division.

Example 1:
    Input: nums = [1, 2, 3, 4]
    Output: [24, 12, 8, 6]

Example 2:
    Input: nums = [-1, 1, 0, -3, 3]
    Output: [0, 0, 9, 0, 0]
"""


def product_except_self(nums: list[int]) -> list[int]:
    n: int = len(nums)
    result: list[int] = [0] * n

    result[n - 1] = 1

    prefix_product: int = 1
    suffix_product: int = 1

    for i in range(n - 2, -1, -1):
        suffix_product *= nums[i + 1]
        result[i] = suffix_product

    for i in range(n):
        result[i] *= prefix_product
        prefix_product *= nums[i]

    return result


def solve() -> None:
    nums = [1, 2, 3, 4]
    expected = [24, 12, 8, 6]
    result = product_except_self(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 3, 4, 5]
    expected = [60, 40, 30, 24]
    result = product_except_self(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, 1, 0, -3, 3]
    expected = [0, 0, 9, 0, 0]
    result = product_except_self(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 2, 3, 4]
    expected = [24, 0, 0, 0]
    result = product_except_self(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 3, 4]
    expected = [0, 0, 0, 0]
    result = product_except_self(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -3, -4]
    expected = [-24, -12, -8, -6]
    result = product_except_self(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, 5, 5]
    expected = [25, 25, 25]
    result = product_except_self(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 3]
    expected = [3, 2]
    result = product_except_self(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
