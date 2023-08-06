from bounden.vectors.vector import Vector


class Vector2(Vector[tuple[float, float]]):
    """
    A two-dimensional vector.

    `x` and `y` describe the lengths of the vector in the x and y dimensions.
    """

    def __init__(self, x: float, y: float) -> None:
        super().__init__((x, y))

    @property
    def x(self) -> float:
        """
        X dimension length.
        """

        return self._lengths[0]

    @property
    def y(self) -> float:
        """
        Y dimension length.
        """

        return self._lengths[1]
