from typing import TypeVar

Length = float | int
Lengths = tuple[Length, ...]

LengthsT = TypeVar("LengthsT", bound=Lengths)
"""
The dimensions of a region (e.g. width and height).
"""

XLengthT = TypeVar("XLengthT", bound=Length)
YLengthT = TypeVar("YLengthT", bound=Length)
