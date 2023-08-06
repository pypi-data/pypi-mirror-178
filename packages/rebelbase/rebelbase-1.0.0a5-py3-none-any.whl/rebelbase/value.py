from typing import Optional, Sequence, cast

from rebelbase.log import log


class Value:
    """
    A raw numeric value.

    `base` describes the numeric base.

    `positive` indicates whether the value is positive or negative. Zero must
    be considered positive.

    `integral` is a tuple that describes the decimal value of each digit of the
    integral part of the value, from most- to least-significant. For example,
    (1, 0) indicates "10" in base 10.

    `fractional` is a tuple that describes the decimal value of each digit of
    the fractional part of the value, from most- to least-significant. For
    example, (0, 1) indicates "0.25" in base 10.
    """

    def __init__(
        self,
        base: int,
        positive: bool = True,
        integral: Optional[Sequence[int]] = None,
        fractional: Optional[Sequence[int]] = None,
    ) -> None:
        self._base = base
        self._positive = positive
        self._integral = (
            tuple(integral) if integral else cast(tuple[int, ...], ())
        )
        self._fractional = (
            tuple(fractional) if fractional else cast(tuple[int, ...], ())
        )

    def __abs__(self) -> "Value":
        return Value(self.base, True, self.integral, self.fractional)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Value)
            and self.base == other.base
            and self.positive == other.positive
            and self.integral == other.integral
            and self.fractional == other.fractional
        )

    def __repr__(self) -> str:
        sign = "+" if self._positive else "-"
        return f"{sign}{self._integral}.{self._fractional}b{self._base}"

    @property
    def base(self) -> int:
        """
        Numeric base.
        """

        return self._base

    @property
    def float(self) -> float:
        """
        Value as a floating point number.
        """

        result: float = 0

        for index, i in enumerate(reversed(self.integral)):
            power = pow(self._base, index)
            value = power * i
            log.debug(
                "At index %s, power is %s and value is %s",
                index,
                power,
                value,
            )
            result += value

        for index, i in enumerate(self.fractional):
            result += 1 / pow(self._base, index + 1) * i

        return result if self.positive else 0 - result

    @property
    def fractional(self) -> tuple[int, ...]:
        """
        The decimal value of each digit of the fractional part of the value,
        from most- to least-significant.

        For example, (0, 1) indicates "0.25" in base 10.
        """

        return self._fractional

    @property
    def integral(self) -> tuple[int, ...]:
        """
        The decimal value of each digit of the integral part of the value, from
        most- to least-significant.

        For example, (1, 0) indicates "10" in base 10.
        """

        return self._integral

    @property
    def positive(self) -> bool:
        """
        Value is positive or negative.
        """

        return self._positive
