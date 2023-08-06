from typing import Any, Generic, TypeVar, cast

from bounden.coordinates import AxesT
from bounden.vectors import Vector


class Point(Generic[AxesT]):
    """
    A point in n-dimensional space.
    """

    def __init__(self, coordinates: AxesT) -> None:
        self._coordinates = coordinates

    def __add__(self, other: Any) -> "Point[AxesT]":
        if not isinstance(other, Vector):
            t = other.__class__.__name__
            raise ValueError(f"Can add only vectors (not {t}) to points")

        v: Vector[Any] = other

        if len(v) != len(self):
            raise ValueError(
                f"Vector force count ({len(v)}) != "
                f"point dimension count ({len(self)})"
            )

        cl = [c + v.lengths[i] for i, c in enumerate(self.coordinates)]
        return Point[AxesT](cast(AxesT, tuple(cl)))

    def __len__(self) -> int:
        return len(self._coordinates)

    @property
    def coordinates(self) -> AxesT:
        """
        Coordinates.
        """

        return self._coordinates


PointT = TypeVar("PointT", bound=Point[Any])
