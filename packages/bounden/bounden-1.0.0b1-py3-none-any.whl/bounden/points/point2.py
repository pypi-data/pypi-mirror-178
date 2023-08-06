from bounden.points.point import Point
from bounden.points.types import XAxisT, YAxisT


class Point2(Point[tuple[XAxisT, YAxisT]]):
    """
    A point within a two-dimensional volume.

    `x` and `y` are the x and y coordinates respectively.
    """

    def __init__(self, x: XAxisT, y: YAxisT) -> None:
        super().__init__((x, y))

    @property
    def x(self) -> XAxisT:
        """
        X coordinate.
        """

        return self.position[0]

    @property
    def y(self) -> YAxisT:
        """
        Y coordinate.
        """

        return self.position[1]
