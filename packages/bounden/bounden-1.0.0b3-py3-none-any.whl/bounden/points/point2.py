from bounden.coordinates.types import XAxisT, YAxisT
from bounden.points.point import Point


class Point2(Point[tuple[XAxisT, YAxisT]]):
    """
    A point in two-dimensional space.

    `x` and `y` are the x and y coordinates respectively.
    """

    def __init__(self, x: XAxisT, y: YAxisT) -> None:
        super().__init__((x, y))

    @property
    def x(self) -> XAxisT:
        """
        X coordinate.
        """

        return self.coordinates[0]

    @property
    def y(self) -> YAxisT:
        """
        Y coordinate.
        """

        return self.coordinates[1]
