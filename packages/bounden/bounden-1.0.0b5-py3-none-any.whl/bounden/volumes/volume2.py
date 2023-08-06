from bounden.volumes.types import XLengthT, YLengthT
from bounden.volumes.volume import Volume


class Volume2(Volume[tuple[XLengthT, YLengthT]]):
    """
    A two-dimensional volume.

    `width` and `height` describe the volume's width and height.
    """

    def __init__(self, width: XLengthT, height: YLengthT) -> None:
        super().__init__((width, height))

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
