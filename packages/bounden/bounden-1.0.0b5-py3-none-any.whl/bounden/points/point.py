from typing import Any, Generic, TypeVar, cast

from bounden.coordinates import AxesT, Coordinate
from bounden.vectors import Vector


class Point(Generic[AxesT]):
    """
    A point in n-dimensional space.
    """

    def __init__(self, coordinates: AxesT) -> None:
        self._coordinates = coordinates

    def __add__(self, other: Any) -> "Point[AxesT]":
        if isinstance(other, Vector):
            v: Vector[Any] = other

            if len(v) != len(self):
                raise ValueError(
                    f"Vector force count ({len(v)}) != "
                    f"point dimension count ({len(self)})"
                )

            cl = [c + v.lengths[i] for i, c in enumerate(self.coordinates)]
            return Point[AxesT](cast(AxesT, tuple(cl)))

        if isinstance(other, (float, int)):
            cl = [c + other for c in self.coordinates]
            return Point[AxesT](cast(AxesT, tuple(cl)))

        raise ValueError(
            f"Cannot add {repr(other)} ({other.__class__.__name__}) to "
            f"{self.__class__.__name__}"
        )

    def __getitem__(self, index: int) -> Coordinate[Any]:
        return self.coordinates[index]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Point):
            o: Point[Any] = other
            return bool(self.coordinates == o.coordinates)

        return bool(self.coordinates == other)

    def __len__(self) -> int:
        return len(self._coordinates)

    def __repr__(self) -> str:
        return str(self._coordinates)

    def __sub__(self, other: Any) -> "Point[AxesT]":
        return self.__add__(other * -1)

    @property
    def coordinates(self) -> AxesT:
        """
        Coordinates.
        """

        return self._coordinates


PointT = TypeVar("PointT", bound=Point[Any])
