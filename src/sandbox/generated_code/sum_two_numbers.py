"""
A Python script to calculate the sum of two numbers.
"""

from typing import Union

Number = Union[int, float]


def add_numbers(num1: Number, num2: Number) -> Number:
    """
    Returns the sum of two numbers.

    Parameters:
        num1 (int | float): The first number.
        num2 (int | float): The second number.

    Returns:
        int | float: The arithmetic sum of num1 and num2.
    """
    return num1 + num2


def main() -> None:
    # Demonstration with test values
    a = 15
    b = 27
    result = add_numbers(a, b)
    print(f"The sum of {a} and {b} is: {result}")

    # Demonstration with floating point numbers
    float_a = 12.5
    float_b = 3.75
    float_result = add_numbers(float_a, float_b)
    print(f"The sum of {float_a} and {float_b} is: {float_result}")

    # Demonstration with negative numbers
    neg_a = -10
    neg_b = 4
    neg_result = add_numbers(neg_a, neg_b)
    print(f"The sum of {neg_a} and {neg_b} is: {neg_result}")


if __name__ == "__main__":
    main()
