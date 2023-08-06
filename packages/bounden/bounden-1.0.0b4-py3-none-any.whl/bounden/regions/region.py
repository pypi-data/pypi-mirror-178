from typing import Any, Generic, cast

from bounden.points import PointT
from bounden.volumes import Length, VolumeT


class Region(Generic[PointT, VolumeT]):
    """
    A region of n-dimensional space.

    `position` describes the region's origin.

    `volume` describes the region's size.
    """

    def __init__(self, position: PointT, volume: VolumeT) -> None:
        if len(position) != len(volume):
            raise ValueError(
                f"Coordinates count ({len(position)}) "
                f"!= lengths count ({len(volume)})"
            )

        self._position = position
        self._volume = volume

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Region):
            o: Region[Any, Any] = other
            return bool(
                self.position == o.position and self.volume == o.volume
            )

        return False

    def __repr__(self) -> str:
        return f"{self.position} x {self.volume}"

    @property
    def center(self) -> PointT:
        """
        Center.
        """

        cl = [self._position[i] + (l / 2) for i, l in enumerate(self.volume)]
        return self._position.__class__(tuple(cl))

    def expand(self, distance: Length) -> "Region[PointT, VolumeT]":
        """
        Gets a copy of this region expanded by `distance` about its centre.

        Pass a negative distance to contract.
        """

        position = self.position - (distance / 2)
        volume = self.volume.expand(distance)
        return self.__class__(cast(PointT, position), cast(VolumeT, volume))

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
