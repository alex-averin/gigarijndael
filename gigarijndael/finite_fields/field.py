from __future__ import annotations

import functools
import operator


class FiniteField:
    """
    Representation of a Finite Field GF(2^n).
    """

    general_polynomials: dict[int, int] = {
        3: 0b1011,
        4: 0b10011,
        5: 0b100101,
        7: 0b10011101,
        8: 0b100011011,
        32: 0b100000000000000000000000010001101,
    }

    def __init__(self, n: int, general_polynomial: int | None = None) -> None:
        """
        Initialize Finite Field.

        Args:
            n: Power of 2 (exponent).
            general_polynomial: Irreducible polynomial. If None, uses a default one for n.
        """
        self.p: int = 2
        self.n: int = n
        self.q: int = self.p**self.n
        self.general_polynomial: int = general_polynomial or self.general_polynomials[n]

    def add(self, *polynomials: int) -> int:
        """Addition in Finite Field (XOR)."""
        return functools.reduce(operator.xor, polynomials)

    def subtract(self, *polynomials: int) -> int:
        """Subtraction in Finite Field (same as addition)."""
        return self.add(*polynomials)

    def multiply(self, first: int, second: int) -> int:
        """Multiplication in Finite Field using Russian Peasant Multiplication."""
        product = 0
        while first and second:
            if second & 1:
                product = self.add(product, first)
            if first & (self.q >> 1):
                first = self.add(first << 1, self.general_polynomial)
            else:
                first <<= 1
            second >>= 1
        return product

    def divide(self, dividend: int, divisor: int) -> int:
        """Division in Finite Field."""
        inverse_divisor = self.inverse(divisor)
        return self.multiply(dividend, inverse_divisor)

    def inverse(self, polynomial: int) -> int:
        """Multiplicative inverse in Finite Field."""
        if polynomial == 0:
            raise ZeroDivisionError("Cannot find inverse of zero")
        _, inverse, _ = self.egcd(polynomial, self.general_polynomial)
        return inverse

    def divmod(self, dividend: int, divisor: int) -> tuple[int, int]:
        """Division with remainder for polynomials."""
        floor = 0
        divisor_length = divisor.bit_length()
        while (shift := dividend.bit_length() - divisor_length) >= 0:
            floor = self.add(floor, 1 << shift)
            dividend = self.add(dividend, divisor << shift)
        return floor, dividend

    def egcd(self, first: int, second: int) -> tuple[int, int, int]:
        """Extended Euclidean Algorithm for polynomials."""
        if first == 0:
            return second, 0, 1
        floor, mod = self.divmod(second, first)
        gcd, x, y = self.egcd(mod, first)
        return gcd, self.subtract(y, self.multiply(floor, x)), x

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FiniteField):
            return NotImplemented
        return self.q == other.q
