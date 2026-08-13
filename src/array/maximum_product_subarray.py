"""152. Maximum Product Subarray

Given an integer array ``nums``, find a subarray that has the largest product,
and return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.

Note:
    The product of an array with a single element is the value of that element.

Example 1:
    Input: nums = [2, 3, -2, 4]
    Output: 6
    Explanation: [2, 3] has the largest product 6.

Example 2:
    Input: nums = [-2, 0, -1]
    Output: 0
    Explanation: The result cannot be 2, because [-2, -1] is not a subarray.

Constraints:
    - 1 <= nums.length <= 2 * 10^4
    - -10 <= nums[i] <= 10
    - The product of any subarray of nums is guaranteed to fit in a 32-bit
      integer.
"""


def max_product_brute_force(nums: list[int]) -> int:
    max_product_brute_force: int = nums[0]

    for left in range(len(nums)):
        current_product: int = 1

        for right in range(left, len(nums)):
            current_product *= nums[right]
            max_product_brute_force = max(max_product_brute_force, current_product)

    return max_product_brute_force


def max_product_prefix_suffix(nums: list[int]) -> int:
    """Find the maximum product by scanning from both ends of the array.

    Approach:
        1. Initialize the best product to negative infinity and create running
           prefix and suffix products that both start at 1.
        2. Traverse the array once, using ``i`` for the left-to-right prefix
           and ``n - i - 1`` for the right-to-left suffix.
        3. Reset the prefix product after it becomes zero. The implementation
           also checks the prefix product before resetting the suffix product,
           so the suffix is reset only when the prefix is zero.
        4. Multiply the running products by the current values from the left
           and right ends.
        5. Compare both running products with the best product found so far.
        6. Return the largest product recorded after the scan.

    Time Complexity:
        O(n), because the function performs one loop over all ``n`` elements
        and does constant-time arithmetic and comparisons per iteration.

    Space Complexity:
        O(1), because only scalar variables for the products, array length,
        index, and current maximum are used regardless of input size.

        https://www.youtube.com/watch?v=hnswaLJvr6g
    """
    # Step 1: Initialize the maximum and both running products.
    max_product: int | float = -float("inf")

    prefix_product: int = 1
    suffix_product: int = 1
    n: int = len(nums)

    # Step 2: Scan the array from the left and right at the same time.
    for i in range(n):
        # Step 3: Reset running products according to the zero checks.
        if prefix_product == 0:
            prefix_product = 1

        if prefix_product == 0:
            suffix_product = 1

        # Step 4: Extend the prefix and suffix products.
        prefix_product *= nums[i]
        suffix_product *= nums[n - i - 1]

        # Step 5: Keep the largest product seen from either direction.
        max_product = max(max_product, prefix_product, suffix_product)

    # Step 6: Return the maximum product found.
    return max_product


def solve() -> None:
    nums: list[int] = [2, 3, -2, 4]
    # Maximum-product subarray: [2, 3]

    expected: int = 6
    result: int = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 3, -2, 4]

    expected = 6
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, -2, -3, 4, -1, 2, 1, -5, 4]

    expected = 960
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, -2, -3, 0, -4, -5, 2, -1]

    expected = 40
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -3, -4, -5, -6]

    expected = 720
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 3, -2, 4, -1, -2, 5]

    expected = 48
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 1, -3, 4, -1, 0, -2, -5, 3]

    expected = 30
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 0, -1]

    expected = 0
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2]

    expected = -2
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 2]

    expected = 2
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, -3]

    expected = 6
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 3, -4]

    expected = 24
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, -5, -2, -4, 3]

    expected = 24
    result = max_product_prefix_suffix(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, -2, -3, 4, -1, 2, 1, -5, 4]
    # Maximum-product subarray: [1, -2, -3, 4, -1, 2, 1, -5, 4]

    expected = 960
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, -2, -3, 0, -4, -5, 2, -1]
    # Maximum-product subarray: [-4, -5, 2]

    expected = 40
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -3, -4, -5, -6]
    # Maximum-product subarray: [-1, -2, -3, -4, -5, -6]

    expected = 720
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 3, -2, 4, -1, -2, 5]
    # Maximum-product subarray: [2, 3, -2, 4, -1]

    expected = 48
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 1, -3, 4, -1, 0, -2, -5, 3]
    # Maximum-product subarray: [-2, -5, 3]

    expected = 30
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 0, -1]
    # Maximum-product subarray: [0]

    expected = 0
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2]
    # Maximum-product subarray: [-2]

    expected = -2
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 2]
    # Maximum-product subarray: [2]

    expected = 2
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, -3]
    # Maximum-product subarray: [-2, -3]

    expected = 6
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 3, -4]
    # Maximum-product subarray: [-2, 3, -4]

    expected = 24
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, -5, -2, -4, 3]
    # Maximum-product subarray: [-2, -4, 3]

    expected = 24
    result = max_product_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
