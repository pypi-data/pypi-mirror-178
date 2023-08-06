from bounden.volumes.volume import Volume


class Volume2(Volume[tuple[float, float]]):
    """
    A two-dimensional volume.

    `width` and `height` describe the volume's width and height.
    """

    def __init__(self, width: float, height: float) -> None:
        super().__init__((width, height))

    @property
    def height(self) -> float:
        """
        Height.
        """

        return self.lengths[1]

    @property
    def width(self) -> float:
        """
        Width.
        """

        return self.lengths[0]
