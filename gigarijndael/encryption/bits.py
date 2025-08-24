def left_rotate(integer: int, *, size: int = 32, block_size: int = 8, shift: int = 1) -> int:
    shift_size = (block_size * shift) % size
    return ((integer << shift_size) | (integer >> (size - shift_size))) & (2**size - 1)


def right_rotate(integer: int, *, size: int = 32, block_size: int = 8, shift: int = 1) -> int:
    shift_size = (block_size * shift) % size
    return (integer >> shift_size) | (integer << (size - shift_size)) & (2**size - 1)


def left_rotate_bits(integer: int, *, size: int = 32, shift: int = 1) -> int:
    return left_rotate(integer, size=size, block_size=1, shift=shift)


def right_rotate_bits(integer: int, *, size: int = 32, shift: int = 1) -> int:
    return right_rotate(integer, size=size, block_size=1, shift=shift)


def is_bit_set(number: int, index: int) -> bool:
    """
    Check if the bit with the specified index is set.
    Indexing is performed starting from the least significant bit.
    """
    return (number >> index) & 1 == 1


def xor_bits(number: int) -> int:
    """Calculate the parity (XOR of all bits) for a number bit."""
    return number.bit_count() & 1


def reverse_bits(integer: int, *, size: int | None = None) -> int:
    size = size or integer.bit_length()
    result = 0
    for i in range(size):
        if integer & (1 << i):
            result |= 1 << (size - i - 1)
    return result
