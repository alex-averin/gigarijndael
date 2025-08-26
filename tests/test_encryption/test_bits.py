import random

import pytest

from gigarijndael.encryption.bits import (
    is_bit_set,
    left_rotate,
    left_rotate_bits,
    reverse_bits,
    right_rotate,
    right_rotate_bits,
    xor_bits,
)


@pytest.mark.parametrize(
    ("word", "word_size", "block_size", "shift", "expected_rotated"),
    [
        (0b1000, 4, 1, 1, 0b0001),
        (0b0001, 4, 1, 1, 0b0010),
        (0b0101, 4, 1, 1, 0b1010),
        (0b1000, 32, 1, 1, 0b010000),
        (0b1000, 32, 3, 1, 0b1000000),
        (0b1000, 32, 8, 1, 0b100000000000),
        (0b10000001, 8, 4, 1, 0b00011000),
        (0b0010000001000100, 16, 8, 1, 0b0100010000100000),
        (0b0010000001000100, 16, 8, 2, 0b0010000001000100),
        (0b0010000001000100, 16, 4, 3, 0b0100001000000100),
    ],
)
def test_left_rotate(word: int, word_size: int, block_size: int, shift: int, expected_rotated: int):
    rotated = left_rotate(word, size=word_size, block_size=block_size, shift=shift)

    assert rotated == expected_rotated


@pytest.mark.parametrize(
    ("word", "word_size", "block_size", "shift", "expected_rotated"),
    [
        (0b1000, 4, 1, 1, 0b0100),
        (0b0001, 4, 1, 1, 0b1000),
        (0b0101, 4, 1, 1, 0b1010),
        (0b1000, 32, 1, 1, 0b0100),
        (0b1000, 32, 3, 1, 0b0001),
        (0b1000, 32, 8, 1, 0b00001000000000000000000000000000),
        (0b10000001, 8, 4, 1, 0b00011000),
        (0b0010000001000100, 16, 8, 1, 0b0100010000100000),
        (0b0010000001000100, 16, 8, 2, 0b0010000001000100),
        (0b0010000001000100, 16, 4, 3, 0b0000010001000010),
    ],
)
def test_right_rotate(
    word: int, word_size: int, block_size: int, shift: int, expected_rotated: int
):
    rotated = right_rotate(word, size=word_size, block_size=block_size, shift=shift)

    assert rotated == expected_rotated


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
def test_left_rotate_bits(integer: int, size: int, shift: int, expected_rotated: int):
    rotated = left_rotate_bits(integer, size=size, shift=shift)

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
def test_right_rotate_bits(integer: int, size: int, shift: int, expected_rotated: int):
    rotated = right_rotate_bits(integer, size=size, shift=shift)

    assert rotated == expected_rotated


@pytest.mark.parametrize(
    ("number", "bit_index", "expected_result"),
    [(0b1, 0, True), (0b1, 1, False), (0b10, 1, True), (0b10, 0, False)],
)
def test__is_bit_set(number: int, bit_index: int, expected_result: bool):
    assert is_bit_set(number=number, index=bit_index) == expected_result


@pytest.mark.parametrize(("number", "expected_result"), [(0b00000001, 1), (0b0100001, 0)])
def test__xor_bits(number: int, expected_result: int):
    assert xor_bits(number) == expected_result


@pytest.mark.parametrize(
    ("number", "size", "expected_result"),
    [
        (0b1, 1, 0b1),
        (0b1, 4, 0b1000),
        (0b1, 8, 0b10000000),
        (0b00000001, 8, 0b10000000),
        (0b11110000, 8, 0b00001111),
        (0x12, 8, 0x48),
        (0x1234, 16, 0x2C48),
        (0x12345678, 32, 0x1E6A2C48),
    ],
)
def test__reverse_bits(number, size, expected_result):
    assert reverse_bits(number, size=size) == expected_result


@pytest.mark.parametrize("size", [8, 16, 32])
@pytest.mark.parametrize("iteration", list(range(10)))
def test__reverse_bits__random(size, iteration):
    original_number = random.getrandbits(size)

    reversed_number = reverse_bits(original_number, size=size)
    result_number = reverse_bits(reversed_number, size=size)

    assert result_number == original_number
