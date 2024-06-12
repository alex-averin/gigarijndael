from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from gigarijndael.finite_fields.field import FiniteField


class Polynomial:
    def __init__(self, value: int, *, finite_field: FiniteField):
        self.value: int = value
        self.finite_field: FiniteField = finite_field

    def __add__(self, other: Polynomial) -> Polynomial:
        return self._binary_operation(other=other, func=self.finite_field.add)

    def __sub__(self, other: Polynomial) -> Polynomial:
        return self._binary_operation(other=other, func=self.finite_field.subtract)

    def __mul__(self, other: Polynomial):
        return self._binary_operation(other=other, func=self.finite_field.multiply)

    def __truediv__(self, other: Polynomial) -> Polynomial:
        return self._binary_operation(other=other, func=self.finite_field.divide)

    def __divmod__(self, other: Polynomial) -> tuple[Polynomial, Polynomial]:
        self._validate_finite_field(other=other)
        quotient, remainder = self.finite_field.divmod(self.value, other.value)
        return (
            Polynomial(quotient, finite_field=self.finite_field),
            Polynomial(remainder, finite_field=self.finite_field),
        )

    def __floordiv__(self, other: Polynomial):
        quotient, _ = divmod(self, other)
        return quotient

    def __mod__(self, other: Polynomial) -> Polynomial:
        _, remainder = divmod(self, other)
        return remainder

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polynomial):
            return NotImplemented
        return self.value == other.value and self.finite_field == other.finite_field

    def __str__(self) -> str:
        if elements := self._elements:
            return "+".join(elements)
        return "0"

    def __repr__(self) -> str:
        return f"<FieldElement {self}>"

    @property
    def _bits(self) -> tuple[int, ...]:
        return tuple(self.value >> (i - 1) & 1 for i in range(self.value.bit_length(), 0, -1))

    @property
    def _degrees(self) -> tuple[int, ...]:
        bits = self._bits
        bits_count = len(bits)
        return tuple(bits_count - i - 1 for i, bit in enumerate(self._bits) if bit)

    @property
    def _elements(self) -> tuple[str, ...]:
        return tuple("1" if degree == 0 else f"x^{degree}" for degree in self._degrees)

    def _binary_operation(self, other: Polynomial, func: typing.Callable[[int, int], int]) -> Polynomial:
        self._validate_finite_field(other=other)
        value = func(self.value, other.value)
        return Polynomial(value, finite_field=self.finite_field)

    def _validate_finite_field(self, other: Polynomial):
        if self.finite_field != other.finite_field:
            raise ValueError("Finite fields orders are not equal")
