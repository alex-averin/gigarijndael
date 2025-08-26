import pytest

from gigarijndael.finite_fields.field import FiniteField


@pytest.mark.parametrize(
    ("first_multiplier", "second_multiplier", "expected_product", "field_n"),
    [
        # GF(2^3)
        (5, 7, 6, 3),
        # GF(2^4)
        (9, 5, 11, 4),
        (13, 9, 15, 4),
        # GF(2^5)
        (0, 0, 0, 5),
        (1, 0, 0, 5),
        (2, 1, 2, 5),
        # GF(2^7)
        (6, 21, 126, 7),
        # GF(2^8)
        (83, 202, 1, 8),
        (87, 19, 254, 8),
        (150, 200, 9, 8),
        (212, 2, 179, 8),
    ],
)
def test_field_multiply(
    first_multiplier: int, second_multiplier: int, expected_product: int, field_n: int
):
    field = FiniteField(n=field_n)

    product = field.multiply(first_multiplier, second_multiplier)

    assert product == expected_product


@pytest.mark.parametrize(
    ("dividend", "divisor", "expected_quotient"),
    [
        (3, 283, (0, 3)),
        (283, 3, (246, 1)),
        (10, 3, (6, 0)),
        (100, 33, (3, 7)),
    ],
)
def test_field_divmod(dividend: int, divisor: int, expected_quotient):
    field = FiniteField(n=3)

    quotient = field.divmod(dividend, divisor)

    assert quotient == expected_quotient


@pytest.mark.parametrize(
    ("polynomial_a", "polynomial_b", "expected_gcd"),
    [
        (3, 283, (1, 246, 1)),
    ],
)
def test_field_egcd(polynomial_a: int, polynomial_b: int, expected_gcd: int):
    field = FiniteField(n=3)

    gcd = field.egcd(polynomial_a, polynomial_b)

    assert gcd == expected_gcd


@pytest.mark.parametrize(
    ("polynomial", "expected_inverse"),
    [
        (1, 1),
        (3, 246),
        (246, 3),
        (100, 73),
        (73, 100),
        (255, 28),
        (28, 255),
    ],
)
def test_field_inverse(polynomial: int, expected_inverse: int):
    field = FiniteField(n=8)

    inverse = field.inverse(polynomial)

    assert inverse == expected_inverse
