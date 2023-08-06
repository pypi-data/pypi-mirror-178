from bounden.coordinates.coordinate import Coordinate


class FloatCoordinate(Coordinate[float]):
    """
    A coordinate on a floating point axis.
    """

    def translate(self, distance: float) -> "Coordinate[float]":
        """
        Gets a copy of this coordinate translated by `distance`.
        """

        return FloatCoordinate(self.coordinate + distance)
