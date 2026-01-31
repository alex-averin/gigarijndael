import itertools
import typing

from more_itertools import grouper

from gigarijndael.encryption.block import Block
from gigarijndael.encryption.encrypter import RijndaelEncrypter
from gigarijndael.encryption.word import Word


class Rijndael:
    """
    Rijndael cipher implementation.
    """

    def __init__(self, *, block_size: int, key_size: int, experimental: bool = False) -> None:
        """
        Initialize Rijndael cipher.

        Args:
            block_size: Block size in 32-bit words (4, 6, or 8).
            key_size: Key size in 32-bit words (4, 6, or 8).
            experimental: Use GF(2^32) "Giga" mode.
        """
        self._encrypter: RijndaelEncrypter = RijndaelEncrypter(
            block_size=block_size, key_size=key_size, experimental=experimental
        )

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        """
        Encrypt data.

        Args:
            data: Data to encrypt.
            key: Encryption key.

        Returns:
            Encrypted data.
        """
        return self._encrypt(data=data, key=key, decrypt=False)

    def decrypt(self, data: bytes, key: bytes) -> bytes:
        """
        Decrypt data.

        Args:
            data: Data to decrypt.
            key: Decryption key.

        Returns:
            Decrypted data.
        """
        return self._encrypt(data=data, key=key, decrypt=True)

    def _encrypt(self, data: bytes, key: bytes, decrypt: bool) -> bytes:
        keys = self._split_key(key=key)
        blocks = list(self._split_blocks(data=data))
        cipher_blocks = self._encrypter.encrypt(blocks=blocks, key=keys, decrypt=decrypt)
        return self._blocks_to_bytes(blocks=cipher_blocks)

    def _split_key(self, key: bytes) -> list[Word]:
        """Split bytes key into Word list. Padds with zeros if necessary."""
        item_size_bytes = self._encrypter.word_cls.ITEM_SIZE
        word_len = self._encrypter.word_cls.LENGTH
        key_size_in_items = self._encrypter.key_size * word_len

        # Padding data with zeros if not enough key bytes
        items = [
            int.from_bytes(item, byteorder="big")
            for item in grouper(key, item_size_bytes, fillvalue=0)
        ]

        if len(items) < key_size_in_items:
            items.extend([0] * (key_size_in_items - len(items)))
        else:
            items = items[:key_size_in_items]

        return [
            self._encrypter.word_cls.from_items(word_items)
            for word_items in itertools.batched(items, word_len)
        ]

    def _split_blocks(self, data: bytes) -> typing.Iterator[Block]:
        """Split bytes data into Blocks."""
        item_size_bytes = self._encrypter.word_cls.ITEM_SIZE
        word_len = self._encrypter.word_cls.LENGTH
        block_size_in_items = word_len * self._encrypter.block_size

        # Padding data with zeros if not multiple of block size
        items = [
            int.from_bytes(item, byteorder="big")
            for item in grouper(data, item_size_bytes, fillvalue=0)
        ]
        return (tuple(block) for block in grouper(items, block_size_in_items, fillvalue=0))

    def _blocks_to_bytes(self, blocks: typing.Iterable[Block]) -> bytes:
        """Convert Blocks back to bytes."""
        item_size = self._encrypter.word_cls.ITEM_SIZE
        result = bytearray()
        for block in blocks:
            for item in block:
                result.extend(item.to_bytes(item_size, byteorder="big"))
        return bytes(result).rstrip(b"\x00")
