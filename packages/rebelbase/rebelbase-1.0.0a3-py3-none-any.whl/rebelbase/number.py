from abc import ABC, abstractmethod
from math import modf
from typing import Any, List

from rebelbase.log import log
from rebelbase.value import Value


class Number(ABC):
    """
    A number.
    """

    def __init__(self, value: float | int | str | Value) -> None:
        if isinstance(value, float | int):
            self._value = value
        elif isinstance(value, str):
            self._value = self.from_string(value).float
        else:
            self._value = value.float

        if self._value == 0 and not self.supports_zero():
            raise ValueError(f"{self.name()} cannot represent zero")

        log.debug("Initialised %s with %s", self.name(), self._value)

    def __abs__(self) -> "Number":
        return self.__class__(abs(self._value))

    def __add__(self, other: Any) -> "Number":
        return self.__class__(self._value + self.parse(other))

    def __eq__(self, other: Any) -> bool:
        return self._value == self.parse(other)

    def __float__(self) -> float:
        return float(self._value)

    def __floordiv__(self, other: Any) -> "Number":
        return self.__class__(self._value // self.parse(other))

    def __int__(self) -> int:
        return int(self._value)

    def __mod__(self, other: Any) -> "Number":
        return self.__class__(self._value % self.parse(other))

    def __mul__(self, other: Any) -> "Number":
        return self.__class__(self._value * self.parse(other))

    def __pow__(self, other: Any) -> "Number":
        return self.__class__(pow(self._value, self.parse(other)))

    def __radd__(self, other: Any) -> "Number":
        return self.__class__(self.parse(other) + self._value)

    def __rfloordiv__(self, other: Any) -> "Number":
        return self.__class__(self.parse(other) // self._value)

    def __rmod__(self, other: Any) -> "Number":
        return self.__class__(self.parse(other) % self._value)

    def __rmul__(self, other: Any) -> "Number":
        return self.__class__(self.parse(other) * self._value)

    def __rpow__(self, other: Any) -> "Number":
        return self.__class__(pow(self.parse(other), self._value))

    def __rsub__(self, other: Any) -> "Number":
        return self.__class__(self.parse(other) - self._value)

    def __rtruediv__(self, other: Any) -> "Number":
        return self.__class__(self.parse(other) / self._value)

    def __str__(self) -> str:
        """
        Converts the value to a string.

        Override to change the format.
        """

        bits: List[str] = []
        v = self.values

        if not v.positive:
            bits.append("-")

        digits = self.digits()
        digit_offset = 0 if self.supports_zero() else -1

        if v.integral:
            bits.extend([str(digits[x + digit_offset]) for x in v.integral])
        else:
            bits.append(str(digits[0]))

        if v.fractional:
            bits.append(".")
            bits.extend([str(digits[x + digit_offset]) for x in v.fractional])

        return "".join(bits)

    def __sub__(self, other: Any) -> "Number":
        return self.__class__(self._value - self.parse(other))

    def __truediv__(self, other: Any) -> "Number":
        return self.__class__(self._value / self.parse(other))

    @classmethod
    def base(cls) -> int:
        """
        Gets the base of this number.
        """

        return len(cls.digits())

    @classmethod
    @abstractmethod
    def digits(cls) -> tuple[str, ...]:
        """
        Gets the digits of this numeric system in ascending value.
        """

    @classmethod
    def from_string(cls, v: str) -> Value:
        """
        Converts the string `v` to a Value.

        Override this function to provide a custom translation.
        """

        positive = True

        if not v:
            return Value(cls.base())

        if v[0] == "-":
            positive = False
            v = v[1:]

        dot_index = v.find(".")

        if dot_index > 0:
            integral_string = v[:dot_index]
            fractional_string = v[dot_index + 1 :]  # noqa: E203
        else:
            integral_string = v
            fractional_string = None

        digits = cls.digits()
        digit_offset = 0 if cls.supports_zero() else 1

        integral_bits: List[int] = []
        for digit in integral_string:
            digit_value = digits.index(digit) + digit_offset
            log.debug("Digit %s has value %s", digit, digit_value)
            integral_bits.append(digit_value)

        log.debug("Integral bits: %s", integral_bits)

        fractional_bits: List[int] = []
        if fractional_string:
            for fv in fractional_string:
                fractional_bits.append(digits.index(fv) + digit_offset)

        return Value(cls.base(), positive, integral_bits, fractional_bits)

    @classmethod
    def name(cls) -> str:
        """
        Gets the name of this number type.
        """

        return cls.__name__

    @classmethod
    def parse(cls, o: Any) -> float | int:
        """
        Attempts to parse `o` as a float or integer.

        Raises `ValueError` if `o` cannot be parsed.
        """

        if isinstance(o, Number):
            return o.value

        if isinstance(o, str):
            return cls(o).value

        if isinstance(o, float | int):
            return o

        raise ValueError(
            f"{cls.name()} cannot parse {repr(o)} ({o.__class__.__name__})"
        )

    @classmethod
    def supports_zero(cls) -> bool:
        """
        Indicates whether or not this numeric system can represent zero.
        """

        return True

    @property
    def value(self) -> float | int:
        """
        Gets this number's value.
        """

        return self._value

    @property
    def values(self) -> "Value":
        """
        Gets this number's value as a Value.
        """

        base = self.base()

        if self._value == 0:
            return Value(base)

        f, i = modf(abs(self._value))

        int_bits: List[int] = []
        quotient = int(i)

        while quotient > 0:
            remainder = quotient % base
            quotient = quotient // base
            if remainder == 0 and not self.supports_zero():
                remainder = base
                quotient -= 1
            int_bits.append(remainder)

        frac_bits: List[int] = []
        frac_remain = f

        fraction_len = 16

        while frac_remain > 0 and len(frac_bits) <= fraction_len:
            frac_remain, i = modf(frac_remain * base)
            frac_bits.append(int(i))

        value = Value(
            base,
            self._value >= 0,
            tuple(reversed(int_bits)),
            tuple(frac_bits),
        )

        log.debug("%s == %s", self._value, value)
        return value
