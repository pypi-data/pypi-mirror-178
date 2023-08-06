from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

ValueT = TypeVar("ValueT")


class Coordinate(ABC, Generic[ValueT]):
    """
    Abstract base coordinate.
    """

    def __init__(self, coordinate: ValueT) -> None:
        self.coordinate = coordinate

    def __add__(self, other: Any) -> "Coordinate[ValueT]":
        if isinstance(other, (float, int)):
            return self.translate(other)

        raise ValueError(
            f"Can translate only by numeric distances, not "
            f"{other.__class__.__name__} ({repr(other)})"
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Coordinate):
            o: Coordinate[Any] = other
            return bool(self.coordinate == o.coordinate)

        return bool(self.coordinate == other)

    def __repr__(self) -> str:
        return str(self.coordinate)

    @abstractmethod
    def translate(self, distance: float) -> "Coordinate[ValueT]":
        """
        Gets a copy of this coordinate translated by `distance`.
        """
