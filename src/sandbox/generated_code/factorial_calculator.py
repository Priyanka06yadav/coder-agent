"""
Factorial Calculator Module

This module provides functions to calculate the factorial of a non-negative integer
using both iterative and recursive approaches, along with robust error handling
and demonstration cases.
"""

import math
import sys


def factorial_iterative(n: int) -> int:
    """
    Calculate the factorial of a non-negative integer iteratively.

    Args:
        n (int): Non-negative integer.

    Returns:
        int: The factorial of n (n!).

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is a negative integer.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"Factorial is only defined for integers, got {type(n).__name__}.")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    """
    Calculate the factorial of a non-negative integer recursively.

    Args:
        n (int): Non-negative integer.

    Returns:
        int: The factorial of n (n!).

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is a negative integer.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"Factorial is only defined for integers, got {type(n).__name__}.")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    if n in (0, 1):
        return 1
    return n * factorial_recursive(n - 1)


def main():
    """Demonstrate the factorial calculation functions and run test cases."""
    print("=" * 50)
    print("Factorial Calculator Demonstration")
    print("=" * 50)

    # Test cases
    test_values = [0, 1, 5, 7, 10]
    for val in test_values:
        iter_res = factorial_iterative(val)
        rec_res = factorial_recursive(val)
        math_res = math.factorial(val)
        assert iter_res == rec_res == math_res, f"Mismatch for {val}!"
        print(f"{val}! = {iter_res}")

    print("\nError handling demonstration:")
    try:
        factorial_iterative(-5)
    except ValueError as e:
        print(f"Negative input handled: {e}")

    try:
        factorial_iterative(3.14)  # type: ignore
    except TypeError as e:
        print(f"Non-integer input handled: {e}")

    print("\nAll checks passed successfully!")


if __name__ == "__main__":
    main()
