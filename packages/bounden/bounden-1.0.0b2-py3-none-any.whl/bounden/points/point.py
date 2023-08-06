from bounden.points.types import AxesT, PointABC


class Point(PointABC[AxesT]):
    """
    A point in n-dimensional space.

    `coordinates` describes the coordinates of the point.
    """

    def __init__(self, coordinates: AxesT) -> None:
        self._coordinates = coordinates

    def __len__(self) -> int:
        return len(self._coordinates)

    @property
    def coordinates(self) -> AxesT:
        """
        Coordinates.
        """

        return self._coordinates
