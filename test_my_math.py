# test_my_math.py
from my_math import add_numbers


def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
    assert add_numbers(-5, -8) == -13
    assert add_numbers(1, 0.36) == 1.36
    assert add_numbers(3.3, 6.7) == 10
    assert add_numbers(0.1, 0.2) == 0.3
    assert add_numbers(0.1111111, 1) == 1.1111111
