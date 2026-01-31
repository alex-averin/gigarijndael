from __future__ import annotations

import abc

from gigarijndael.rijndael import Rijndael


class AES(abc.ABC, Rijndael):
    """
    Abstract base class for AES encryption and decryption.
    AES is a specific version of Rijndael with a fixed block size of 128 bits (4 words).
    """

    BLOCK_SIZE: int = 4
    KEY_SIZE: int

    def __init__(self) -> None:
        super().__init__(block_size=self.BLOCK_SIZE, key_size=self.KEY_SIZE, experimental=False)


class AES128(AES):
    """AES-128 implementation (128-bit key)."""

    KEY_SIZE = 4


class AES192(AES):
    """AES-192 implementation (192-bit key)."""

    KEY_SIZE = 6


class AES256(AES):
    """AES-256 implementation (256-bit key)."""

    KEY_SIZE = 8
