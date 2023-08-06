from rebelbase.number import Number


class Base2(Number):
    """
    A base 2 number.
    """

    @classmethod
    def digits(cls) -> tuple[str, ...]:
        """
        Gets the digits of this numeric system in ascending value.
        """

        return ("0", "1")
