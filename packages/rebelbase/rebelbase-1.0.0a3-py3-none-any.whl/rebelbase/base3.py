from rebelbase.number import Number


class Base3(Number):
    """
    A base 3 number.
    """

    @classmethod
    def digits(cls) -> tuple[str, ...]:
        """
        Gets the digits of this numeric system in ascending value.
        """

        return ("0", "1", "2")
