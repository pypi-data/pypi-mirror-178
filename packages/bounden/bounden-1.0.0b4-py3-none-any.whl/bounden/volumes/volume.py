from typing import Any, Generic, Iterator, List, TypeVar, cast

from bounden.volumes.types import Length, LengthsT


class Volume(Generic[LengthsT]):
    """
    An n-dimensional volume.

    `lengths` describes the length of each dimension.
    """

    def __init__(self, lengths: LengthsT) -> None:
        self._lengths = lengths

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Volume):
            o: Volume[Any] = other
            return bool(self.lengths == o.lengths)

        return bool(self.lengths == other)

    def __iter__(self) -> Iterator[Length]:
        for length in self._lengths:
            yield length

    def __len__(self) -> int:
        return len(self._lengths)

    def __repr__(self) -> str:
        return str(self._lengths)

    def expand(self, distance: Length) -> "Volume[LengthsT]":
        """
        Gets a copy of this volume expanded by `distance`.

        Pass a negative distance to contract.
        """

        ll: List[Length] = [length + distance for length in self]
        lengths = cast(LengthsT, tuple(ll))
        return Volume[LengthsT](lengths)

    @property
    def lengths(self) -> LengthsT:
        """
        Dimension lengths.
        """

        return self._lengths


VolumeT = TypeVar("VolumeT", bound=Volume[Any])
