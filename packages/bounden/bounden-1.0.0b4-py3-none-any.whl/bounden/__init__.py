"""
&copy; 2022 Cariad Eccleston and released under the MIT License.

For usage and support, see https://github.com/cariad/bounden.
"""

from importlib.resources import files

from bounden.coordinates import (
    Coordinate,
    FloatCoordinate,
    IntegerCoordinate,
    StringCoordinate,
)
from bounden.points import Point, Point2
from bounden.regions import Region, Region2
from bounden.vectors import Vector, Vector2
from bounden.volumes import Length, Lengths, Volume, Volume2


def version() -> str:
    """
    Gets the package's version.
    """

    with files(__package__).joinpath("VERSION").open("r") as t:
        return t.readline().strip()


__all__ = [
    "Coordinate",
    "FloatCoordinate",
    "IntegerCoordinate",
    "Length",
    "Lengths",
    "Point",
    "Point2",
    "Region",
    "Region2",
    "StringCoordinate",
    "Vector",
    "Vector2",
    "Volume",
    "Volume2",
    "version",
]
