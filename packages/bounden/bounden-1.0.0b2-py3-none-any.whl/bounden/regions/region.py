from typing import Generic

from bounden.points.types import PointT
from bounden.volumes.types import VolumeT


class Region(Generic[PointT, VolumeT]):
    """
    A region of n-dimensional space.

    `position` describes the region's origin.

    `volume` describes the region's size.
    """

    def __init__(
        self,
        position: PointT,
        volume: VolumeT,
    ) -> None:
        if len(position) != len(volume):
            raise ValueError(
                f"Coordinates count ({len(position)}) "
                f"!= lengths count ({len(volume)})"
            )

        self._position = position
        self._volume = volume

    @property
    def position(self) -> PointT:
        """
        Position.
        """

        return self._position

    @property
    def volume(self) -> VolumeT:
        """
        Volume.
        """

        return self._volume
