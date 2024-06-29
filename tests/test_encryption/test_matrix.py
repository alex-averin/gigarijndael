import pytest

from gigarijndael.encryption.matrix import affine_transformation


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
    affine = 0b11110001
    const = 0x63
    transform_number = affine_transformation(number, affine, const)

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
    affine = 0b10100100
    const = 0x5
    transform_number = affine_transformation(number, affine, const)

    assert transform_number == expected_number
