from bounden.points import Point2
from bounden.points.types import XAxisT, YAxisT
from bounden.regions.region import Region
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
