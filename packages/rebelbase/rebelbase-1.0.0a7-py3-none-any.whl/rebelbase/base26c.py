from rebelbase.number import Number


class Base26C(Number):
    """
    A base 26 number that supports continuous sequences; for example: A, B,
    C...X, Y, Z, AA, AB, AC...ZX, ZY, ZZ, AAA, AAB...

    To facilitate continuous sequences, this number does not support zeros. "A"
    represents the decimal value 1.
    """

    @classmethod
    def digits(cls) -> tuple[str, ...]:
        """
        Gets the digits of this numeric system in ascending value.
        """

        return tuple(chr(n) for n in range(65, 65 + 26))

    @classmethod
    def supports_zero(cls) -> bool:
        """
        Indicates whether or not this numeric system can represent zero.
        """

        return False
