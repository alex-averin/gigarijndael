from gigarijndael.encryption.matrix import affine_transformation
from gigarijndael.finite_fields.field import FiniteField


class SBox:
    AFFINE_ROW: int = 0b10001111
    AFFINE_CONST: int = 0x63
    finite_field = FiniteField(8)

    def _multiplicative_inverse(self, item: int) -> int:
        if item == 0:
            return 0
        return self.finite_field.inverse(item)

    def __getitem__(self, item: int) -> int:
        return affine_transformation(
            self._multiplicative_inverse(item),
            affine=self.AFFINE_ROW,
            const=self.AFFINE_CONST,
            size=self.finite_field.n,
        )


class InvSBox(SBox):
    AFFINE_ROW: int = 0b00100101
    AFFINE_CONST: int = 0x5
    finite_field = FiniteField(8)

    def __getitem__(self, item: int) -> int:
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
