from gigarijndael.encryption.matrix import affine_transformation
from gigarijndael.finite_fields.field import FiniteField


class SBox:
    AFFINE_ROW: int = 0b11110001
    AFFINE_CONST: int = 0x63
    finite_field = FiniteField(8)

    def _multiplicative_inverse(self, item: int) -> int:
        if item == 0:
            return 0
        return self.finite_field.inverse(item)

    def __getitem__(self, item: int) -> int:
        return affine_transformation(
            self._multiplicative_inverse(item), affine=self.AFFINE_ROW, const=self.AFFINE_CONST
        )


class InvSBox(SBox):
    AFFINE_ROW: int = 0b10100100
    AFFINE_CONST: int = 0x5

    def __getitem__(self, item: int) -> int:
        return self._multiplicative_inverse(
            affine_transformation(item, affine=self.AFFINE_ROW, const=self.AFFINE_CONST)
        )
