from typing import Generic

from bounden.points import Point
from bounden.points.types import AxesT, LengthsT


class Region(Point[AxesT], Generic[AxesT, LengthsT]):
    """
    A region within an n-dimensional volume.

    `position` describes the region's origin.

    `lengths` describes the length of each of the region's dimensions.
    """

    def __init__(self, position: AxesT, lengths: LengthsT) -> None:
        if len(position) != len(lengths):
            raise ValueError(
                f"Coordinates count ({len(position)}) "
                f"!= lengths count ({len(lengths)})"
            )

        super().__init__(position)
        self._lengths = lengths

    @property
    def lengths(self) -> LengthsT:
        """
        Dimension lengths.
        """

        return self._lengths
