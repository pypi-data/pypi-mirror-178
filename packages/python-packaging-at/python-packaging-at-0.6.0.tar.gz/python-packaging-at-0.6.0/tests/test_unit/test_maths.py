from python_packaging_at.maths import add_numbers


def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(10, 100) == 110
