from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

AxesT = TypeVar("AxesT", bound=tuple[Any, ...])

XAxisT = TypeVar("XAxisT")
YAxisT = TypeVar("YAxisT")


class PointABC(ABC, Generic[AxesT]):
    """
    Abstract base point.
    """

    @abstractmethod
    def __len__(self) -> int:
        """
        Gets the number of coordinates that describe this position.
        """


PointT = TypeVar("PointT", bound=PointABC[Any])
