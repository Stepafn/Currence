# my_math.py

def add_numbers(num1: int | float, num2: int | float) -> int | float:
    return round(num1 + num2, max(len(str(num1)), len(str(num2))))
