from rebelbase import Base26C

from bounden.coordinates.coordinate import Coordinate


class StringCoordinate(Coordinate[str]):
    """
    A coordinate on a string axis.

    Values run from "A" to "Z", "AA" to "ZZ", "AAA" to "ZZZ", and so on to
    infinity.
    """

    def translate(self, distance: float) -> "Coordinate[str]":
        """
        Gets a copy of this coordinate translated by the integer value of
        `distance`.
        """

        return StringCoordinate(str(Base26C(self.coordinate) + int(distance)))
