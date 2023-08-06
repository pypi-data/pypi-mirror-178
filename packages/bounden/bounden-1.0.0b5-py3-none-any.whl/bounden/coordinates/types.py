from typing import Any, TypeVar

from bounden.coordinates.coordinate import Coordinate

AxesT = TypeVar("AxesT", bound=tuple[Coordinate[Any], ...])

XAxisT = TypeVar("XAxisT", bound=Coordinate[Any])
YAxisT = TypeVar("YAxisT", bound=Coordinate[Any])
