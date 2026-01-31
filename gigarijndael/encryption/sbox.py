from functools import lru_cache

from gigarijndael.encryption.matrix import affine_transformation
from gigarijndael.finite_fields.field import FiniteField


class SBox:
    """
    Standard Rijndael S-Box.
    """

    AFFINE_ROW: int = 0b10001111
    AFFINE_CONST: int = 0x63
    finite_field: FiniteField = FiniteField(8)

    def _multiplicative_inverse(self, item: int) -> int:
        """Find multiplicative inverse in GF(2^n)."""
        if item == 0:
            return 0
        return self.finite_field.inverse(item)

    @lru_cache(maxsize=1024)
    def __getitem__(self, item: int) -> int:
        """Substitute a single value."""
        return affine_transformation(
            self._multiplicative_inverse(item),
            affine=self.AFFINE_ROW,
            const=self.AFFINE_CONST,
            size=self.finite_field.n,
        )


class InvSBox(SBox):
    """
    Standard Rijndael Inverse S-Box.
    """

    AFFINE_ROW: int = 0b00100101
    AFFINE_CONST: int = 0x5
    finite_field: FiniteField = FiniteField(8)

    @lru_cache(maxsize=1024)
    def __getitem__(self, item: int) -> int:
        """Substitute a single value using inverse S-Box."""
        return self._multiplicative_inverse(
            affine_transformation(
                item,
                affine=self.AFFINE_ROW,
                const=self.AFFINE_CONST,
                size=self.finite_field.n,
            )
        )


class GigaSBox(SBox):
    finite_field = FiniteField(32)
    AFFINE_ROW: int = 0xD1016880
    AFFINE_CONST: int = 0xB4E969D2


class GigaInvSBox(InvSBox):
    finite_field = FiniteField(32)
    AFFINE_ROW = 0xFC76DEE1
    AFFINE_CONST: int = 0xA38D0057
