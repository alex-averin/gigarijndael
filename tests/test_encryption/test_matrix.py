import pytest

from gigarijndael.encryption.matrix import affine_transformation
from gigarijndael.encryption.sbox import InvSBox, SBox


@pytest.mark.parametrize(
    ("number", "expected_number"),
    [
        (0x00, 0x63),
        (0x01, 0x7C),
        (0x8D, 0x77),
        (0xF6, 0x7B),
        (0xCD, 0xB0),
        (0x1A, 0x54),
        (0x41, 0xBB),
        (0x1C, 0x16),
    ],
)
def test_affine_transform(number, expected_number):
    transform_number = affine_transformation(number, SBox.AFFINE_ROW, SBox.AFFINE_CONST)

    assert transform_number == expected_number


@pytest.mark.parametrize(
    ("number", "expected_number"),
    [
        (0x63, 0x00),
        (0x7C, 0x01),
        (0x77, 0x8D),
        (0x7B, 0xF6),
        (0xB0, 0xCD),
        (0x54, 0x1A),
        (0xBB, 0x41),
        (0x16, 0x1C),
    ],
)
def test_inverse_affine_transform(number, expected_number):
    transform_number = affine_transformation(number, InvSBox.AFFINE_ROW, InvSBox.AFFINE_CONST)

    assert transform_number == expected_number


@pytest.mark.parametrize("number", [0, 1, 2, 100500, 9999999, 0x12345678, 0xFFFFFFFF, 0xDEADBEEF])
def test_affine_transformation_inverse(number: int):
    affine_row = 0xD1016880
    affine_const = 0xB4E969D2

    inv_affine_row = 0xFC76DEE1
    inv_affine_const = 0xA38D0057

    transform_number = affine_transformation(number, affine_row, affine_const, size=32)
    inverse_number = affine_transformation(
        transform_number, inv_affine_row, inv_affine_const, size=32
    )

    assert inverse_number == number
