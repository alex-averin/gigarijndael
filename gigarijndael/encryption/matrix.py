import typing

from gigarijndael.encryption.bits import reverse_bits, right_rotate_bits, xor_bits


def affine_transformation(number: int, affine: int, const: int, size: int = 8) -> int:
    """
    Apply affine transformation to a number.

    Used in S-Box generation.
    """
    number = reverse_bits(number, size=size)
    result = 0
    for i in range(size):
        row = right_rotate_bits(affine, size=size, shift=i)
        result |= xor_bits(row & number) << i

    return result ^ const


def left_shift(items: list[typing.Any], shift: int) -> list[typing.Any]:
    """Cyclic left shift of a list."""
    if not items:
        return items
    shift %= len(items)
    return items[shift:] + items[:shift]


def right_shift(items: list[typing.Any], shift: int) -> list[typing.Any]:
    """Cyclic right shift of a list."""
    if not items:
        return items
    shift %= len(items)
    return items[-shift:] + items[:-shift]
