from bounden.points.types import XAxisT, XLengthT, YAxisT, YLengthT
from bounden.regions.region import Region


class Region2(Region[tuple[XAxisT, YAxisT], tuple[XLengthT, YLengthT]]):
    """
    A region within a two-dimensional volume.

    `x` and `y` describe the region's origin respectively.

    `width` and `height` describe the region's dimensions.
    """

    def __init__(
        self,
        x: XAxisT,
        y: YAxisT,
        width: XLengthT,
        height: YLengthT,
    ) -> None:
        super().__init__((x, y), (width, height))

    @property
    def height(self) -> YLengthT:
        """
        Height.
        """

        return self.lengths[1]

    @property
    def width(self) -> XLengthT:
        """
        Width.
        """

        return self.lengths[0]
