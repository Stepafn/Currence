# my_math.py

def add_numbers(num1: int | float, num2: int | float) -> int | float:
    num1_floating_length = 0
    num2_floating_length = 0
    if isinstance(num1, float):
        num1_floating_length = len(str(num1).split('.')[-1])
    if isinstance(num2, float):
        num2_floating_length = len(str(num2).split('.')[-1])
    return round(num1 + num2, max(num1_floating_length, num2_floating_length))
    
