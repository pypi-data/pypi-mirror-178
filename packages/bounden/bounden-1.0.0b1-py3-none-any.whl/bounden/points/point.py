from typing import Generic

from bounden.points.types import AxesT


class Point(Generic[AxesT]):
    """
    A point within an n-dimensional volume.

    `position` describes the coordinates of the point.
    """

    def __init__(self, position: AxesT) -> None:
        self._position = position

    @property
    def position(self) -> AxesT:
        """
        Position.
        """

        return self._position
