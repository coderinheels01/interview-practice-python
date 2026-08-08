# Project Conventions

## Problem Description Format

When adding a problem description (e.g. LeetCode question) at the top of a Python file, always use a triple-quoted docstring (`""" """`), not `#` comments.

Example:
```python
"""
Two Sum (LeetCode #1)

Given an array of integers nums and an integer target, return indices of
the two numbers such that they add up to target.
"""
```

## Type Hints

Always add type hints to all function signatures — parameters and return types. This applies to every function written in this project without exception.

Example:
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    ...
```
