import pytest

from gigarijndael.finite_fields.field import FiniteField
from gigarijndael.finite_fields.polynomial import Polynomial


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
def test_polynomial_multiply(first_multiplier: int, second_multiplier: int, expected_product: int, field_n: int):
    finite_field = FiniteField(n=field_n)
    first_polynomial = Polynomial(value=first_multiplier, finite_field=finite_field)
    second_polynomial = Polynomial(value=second_multiplier, finite_field=finite_field)
    expected_polynomial = Polynomial(value=expected_product, finite_field=finite_field)

    result_polynomial = first_polynomial * second_polynomial

    assert result_polynomial == expected_polynomial


@pytest.mark.parametrize(
    ("field_n", "dividend", "divisor", "expected_divmod"),
    [
        (3, 3, 283, (0, 3)),
        (3, 283, 3, (246, 1)),
        (3, 10, 3, (6, 0)),
        (3, 100, 33, (3, 7)),
    ],
)
def test_polynomial_divmod(field_n: int, dividend: int, divisor: int, expected_divmod: tuple[int, int]):
    finite_field = FiniteField(n=field_n)
    quotient_value, remainder_value = expected_divmod
    expected_quotient = Polynomial(value=quotient_value, finite_field=finite_field)
    expected_remainder = Polynomial(value=remainder_value, finite_field=finite_field)
    dividend_polynomial = Polynomial(value=dividend, finite_field=finite_field)
    divisor_polynomial = Polynomial(value=dividend, finite_field=finite_field)

    quotient, remainder = divmod(dividend_polynomial, divisor_polynomial)

    assert quotient, remainder == (expected_quotient, expected_remainder)


@pytest.mark.parametrize(
    ("first_value", "first_field_order", "second_value", "second_field_order", "expected_is_equals"),
    [(100, 5, 100, 5, True), (2, 3, 2, 3, True), (15, 4, 15, 5, False), (255, 8, 254, 8, False)],
)
def test_polynomial_equals(
    first_value: int, first_field_order: int, second_value: int, second_field_order: int, expected_is_equals: bool
):
    first_polynomial = Polynomial(value=first_value, finite_field=FiniteField(n=first_field_order))
    second_polynomial = Polynomial(value=second_value, finite_field=FiniteField(n=second_field_order))

    assert (first_polynomial == second_polynomial) is expected_is_equals


@pytest.mark.parametrize(
    ("value", "expected_bits"),
    [
        (0, ()),
        (1, (1,)),
        (2, (1, 0)),
        (3, (1, 1)),
        (80, (1, 0, 1, 0, 0, 0, 0)),
        (81, (1, 0, 1, 0, 0, 0, 1)),
        (255, (1, 1, 1, 1, 1, 1, 1, 1)),
    ],
)
def test_polynomial_bits(value, expected_bits):
    finite_field = FiniteField(n=8)
    polynomial = Polynomial(value=value, finite_field=finite_field)

    assert polynomial._bits == expected_bits


@pytest.mark.parametrize(
    ("value", "expected_degrees"),
    [
        (0, ()),
        (1, (0,)),
        (2, (1,)),
        (3, (1, 0)),
        (80, (6, 4)),
        (81, (6, 4, 0)),
        (255, (7, 6, 5, 4, 3, 2, 1, 0)),
    ],
)
def test_polynomial_degrees(value, expected_degrees):
    finite_field = FiniteField(n=8)
    polynomial = Polynomial(value=value, finite_field=finite_field)

    assert polynomial._degrees == expected_degrees


@pytest.mark.parametrize(
    ("value", "expected_polynomial_str"),
    [
        (0, "0"),
        (1, "1"),
        (2, "x^1"),
        (3, "x^1+1"),
        (80, "x^6+x^4"),
        (81, "x^6+x^4+1"),
        (255, "x^7+x^6+x^5+x^4+x^3+x^2+x^1+1"),
    ],
)
def test_polynomial_str(value, expected_polynomial_str):
    finite_field = FiniteField(n=8)
    polynomial = Polynomial(value=value, finite_field=finite_field)

    assert str(polynomial) == expected_polynomial_str
