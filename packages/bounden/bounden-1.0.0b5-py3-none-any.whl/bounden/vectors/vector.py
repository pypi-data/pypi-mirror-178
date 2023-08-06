from typing import Callable, Generic

from bounden.coordinates.types import AxesT
from bounden.vectors.types import LengthsT

AxisTranslator = Callable[[AxesT, LengthsT], AxesT]


class Vector(Generic[LengthsT]):
    """
    An n-dimensional vector.

    `lengths` describes the length of the vector in each dimension. The index
    indicates the dimension and the value describes the length.
    """

    def __init__(self, lengths: LengthsT) -> None:
        self._lengths = lengths

    def __len__(self) -> int:
        return len(self._lengths)

    @property
    def lengths(self) -> LengthsT:
        """
        Length of the vector in each dimension.

        The index indicates the dimension and the value describes the length.
        """

        return self._lengths
