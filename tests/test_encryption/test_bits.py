import pytest

from gigarijndael.encryption.bits import is_bit_set, left_rotate, reduce_bits, right_rotate


@pytest.mark.parametrize(
    ("integer", "size", "shift", "expected_rotated"),
    [
        (0b1000, 4, 1, 0b0001),
        (0b0001, 4, 1, 0b0010),
        (0b0101, 4, 1, 0b1010),
        (0b1000, 32, 1, 0b010000),
        (0b1000, 32, 3, 0b1000000),
    ],
)
def test__left_rotate(integer: int, size: int, shift: int, expected_rotated: int):
    rotated = left_rotate(integer, size=size, shift=shift)

    assert rotated == expected_rotated


@pytest.mark.parametrize(
    ("integer", "size", "shift", "expected_rotated"),
    [
        (0b1000, 4, 1, 0b0100),
        (0b0001, 4, 1, 0b1000),
        (0b0101, 4, 1, 0b1010),
        (0b1000, 32, 1, 0b0100),
        (0b1000, 32, 3, 0b0001),
    ],
)
def test__right_rotate(integer: int, size: int, shift: int, expected_rotated: int):
    rotated = right_rotate(integer, size=size, shift=shift)

    assert rotated == expected_rotated


@pytest.mark.parametrize(
    ("number", "bit_index", "expected_result"),
    [(0b1, 0, True), (0b1, 1, False), (0b10, 1, True), (0b10, 0, False)],
)
def test__is_bit_set(number: int, bit_index: int, expected_result: bool):
    assert is_bit_set(number=number, index=bit_index) == expected_result


@pytest.mark.parametrize(
    ("number", "size", "expected_result"),
    [(0b00000001, 8, 1), (0b0100001, 8, 0)],
)
def test__reduce_bits(number: int, size: int, expected_result: int):
    assert reduce_bits(number, size=size) == expected_result
