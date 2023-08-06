"""
&copy; 2022 Cariad Eccleston and released under the MIT License.

For usage and support, see https://github.com/cariad/bounden.
"""

from importlib.resources import files

from bounden.points import Point, Point2
from bounden.regions import Region, Region2
from bounden.volumes import Volume, Volume2


def version() -> str:
    """
    Gets the package's version.
    """

    with files(__package__).joinpath("VERSION").open("r") as t:
        return t.readline().strip()


__all__ = [
    "Point",
    "Point2",
    "Region",
    "Region2",
    "Volume",
    "Volume2",
    "version",
]
