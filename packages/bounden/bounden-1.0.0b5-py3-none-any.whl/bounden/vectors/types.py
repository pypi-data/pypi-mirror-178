from typing import TypeVar

LengthsT = TypeVar("LengthsT", bound=tuple[float, ...])
"""
The index indicates the dimension and the value describes the length.
"""
