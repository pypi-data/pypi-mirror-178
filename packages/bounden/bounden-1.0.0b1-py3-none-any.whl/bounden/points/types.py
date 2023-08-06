from typing import Any, TypeVar

AxesT = TypeVar("AxesT", bound=tuple[Any, ...])
LengthsT = TypeVar("LengthsT", bound=tuple[float, ...])
"""
The dimensions of a region (e.g. width and height).
"""

XAxisT = TypeVar("XAxisT")
YAxisT = TypeVar("YAxisT")

XLengthT = TypeVar("XLengthT", bound=float)
YLengthT = TypeVar("YLengthT", bound=float)
