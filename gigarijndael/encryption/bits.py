import functools
import operator


def left_rotate(integer: int, *, size: int = 32, shift: int = 1) -> int:
    return ((integer << shift) | (integer >> (size - shift))) & (2**size - 1)


def right_rotate(integer: int, *, size: int = 32, shift: int = 1) -> int:
    return (integer >> shift) | (integer << (size - shift)) & (2**size - 1)


def is_bit_set(number: int, index: int) -> bool:
    """
    Check if the bit with the specified index is set.
    Indexing is performed starting from the least significant bit.
    """
    return (number >> index) & 1 == 1


def reduce_bits(number: int, size: int = 8) -> int:
    bits = (is_bit_set(number, index=i) for i in range(size))
    return int(functools.reduce(operator.xor, bits))
