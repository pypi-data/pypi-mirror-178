from bounden.coordinates import XAxisT, YAxisT
from bounden.points import Point2
from bounden.regions import Region
from bounden.vectors import Vector2
from bounden.volumes import Volume2


class Region2(Region[Point2[XAxisT, YAxisT], Volume2]):
    """
    A region of two-dimensional space.

    `x` and `y` describe the region's origin.

    `width` and `height` describe the region's dimensions.
    """

    def __init__(
        self,
        x: XAxisT,
        y: YAxisT,
        width: float,
        height: float,
    ) -> None:
        super().__init__(Point2(x, y), Volume2(width, height))

    @property
    def bottom(self) -> YAxisT:
        """
        Bottom.
        """

        return self.bottom_right[1]

    @property
    def bottom_right(self) -> tuple[XAxisT, YAxisT]:
        """
        Bottom right.
        """

        vector = Vector2(self.volume.width, self.volume.height)
        return (self.position + vector).coordinates

    @property
    def left(self) -> XAxisT:
        """
        Left.
        """

        return self.position.x

    @property
    def right(self) -> XAxisT:
        """
        Right.
        """

        return self.bottom_right[0]

    @property
    def top(self) -> YAxisT:
        """
        Top.
        """

        return self.position.y
