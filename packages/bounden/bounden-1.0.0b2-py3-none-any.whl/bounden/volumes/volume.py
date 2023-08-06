from bounden.volumes.types import LengthsT, VolumeABC


class Volume(VolumeABC[LengthsT]):
    """
    An n-dimensional volume.

    `lengths` describes the length of each dimension.
    """

    def __init__(self, lengths: LengthsT) -> None:
        self._lengths = lengths

    def __len__(self) -> int:
        return len(self._lengths)

    @property
    def lengths(self) -> LengthsT:
        """
        Dimension lengths.
        """

        return self._lengths
