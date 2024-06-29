import typing

from gigarijndael.encryption.bits import is_bit_set, left_rotate, reduce_bits


def affine_transformation(number: int, affine: int, const: int, size: int = 8) -> int:
    result = 0
    for bit_index in range(size):
        bit = reduce_bits(number & left_rotate(affine, size=size, shift=bit_index)) ^ is_bit_set(const, bit_index)
        result |= bit << bit_index
    return result


def left_shift(items: list[typing.Any], shift: int) -> list[typing.Any]:
    shift = shift % len(items)
    return items[shift:] + items[:shift]


def right_shift(items: list[typing.Any], shift: int) -> list[typing.Any]:
    shift = shift % len(items)
    return items[-shift:] + items[:-shift]
