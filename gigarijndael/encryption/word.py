from __future__ import annotations

import typing

from gigarijndael.encryption.bits import left_rotate, right_rotate

BYTE_SIZE: int = 8


class Word:
    LENGTH: int = 4  # Count of items in one word, constant for all modifications
    ITEM_SIZE: int = 1  # Size of each word item in bytes (8 bits by default)

    __slots__ = ("_value",)

    def __init__(self, value: int = 0) -> None:
        """
        Initialize a Word with a given integer value.

        Args:
            value: The integer value of the word.

        Raises:
            ValueError: If the value exceeds the word's bit size.
        """
        if value.bit_length() > self.size_bits():
            raise ValueError(
                f"Word length cannot be more than {self.size_bits()} "
                f"bits, received {value.bit_length()} bits"
            )
        self._value: int = value

    @classmethod
    def item_size_bits(cls) -> int:
        """Return the size of a single item in bits."""
        return cls.ITEM_SIZE * BYTE_SIZE

    @classmethod
    def size(cls) -> int:
        """Return the total size of the word in default items (bytes)."""
        return cls.LENGTH * cls.ITEM_SIZE

    @classmethod
    def size_bits(cls) -> int:
        """Return the total size of the word in bits."""
        return cls.size() * BYTE_SIZE

    @classmethod
    def from_items(cls, items: typing.Iterable[int]) -> Word:
        """
        Create a word from a sequence of integers.
        The first element is the most significant item of the word.

        Args:
            items: An iterable of integers representing word items.

        Returns:
            A new Word instance.
        """
        word = cls(0)
        for i, item in enumerate(items):
            word[i] = item
        return word

    def __lshift__(self, other: int) -> Word:
        """
        Left cyclic shift of items.

        Args:
            other: Number of items to shift.

        Returns:
            A new Word instance with shifted items.
        """
        return self.__class__(
            left_rotate(
                self._value, size=self.size_bits(), block_size=self.item_size_bits(), shift=other
            )
        )

    def __rshift__(self, other: int) -> Word:
        """
        Right cyclic shift of items.

        Args:
            other: Number of items to shift.

        Returns:
            A new Word instance with shifted items.
        """
        return self.__class__(
            right_rotate(
                self._value, size=self.size_bits(), block_size=self.item_size_bits(), shift=other
            )
        )

    def __xor__(self, other: Word) -> Word:
        """Bitwise XOR with another Word."""
        return self.__class__(int(self) ^ int(other))

    def __repr__(self) -> str:
        hex_width = self.size() * 2
        return f"<{self.__class__.__name__} 0x{self._value:0{hex_width}x}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word) and not isinstance(other, int):
            return NotImplemented
        return int(self) == int(other)

    def __bool__(self) -> bool:
        return self._value != 0

    def __getitem__(self, index: int) -> int:
        if index < 0:
            index += self.LENGTH
        if not 0 <= index < self.LENGTH:
            raise IndexError("Word index out of range")
        shift = (self.LENGTH - index - 1) * self.item_size_bits()
        return (self._value >> shift) & ((1 << self.item_size_bits()) - 1)

    def __setitem__(self, key: int, value: int):
        if key < 0:
            key += self.LENGTH
        if not 0 <= key < self.LENGTH:
            raise IndexError("Word assignment index out of range")
        if value.bit_length() > self.item_size_bits():
            raise ValueError(
                f"Item length cannot be more than {self.item_size_bits()} bits, "
                f"received {value.bit_length()} bits"
            )
        self._value |= value << (self.LENGTH - key - 1) * self.item_size_bits()

    def __iter__(self) -> typing.Iterator[int]:
        return iter(self[i] for i in range(self.LENGTH))

    def __reversed__(self) -> typing.Iterator[int]:
        return iter(self[i - 1] for i in range(self.LENGTH, 0, -1))

    def __len__(self) -> int:
        return self.LENGTH

    def __int__(self) -> int:
        return self._value

    def __bytes__(self) -> bytes:
        return self._value.to_bytes(length=self.size())


class GigaWord(Word):
    ITEM_SIZE = 4
