from abc import ABC, abstractmethod
from Enum.Enum import Polo


class AbstractPlanet(ABC):
    @property
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def nukeDetected(self, damage: float, pole: Polo) -> None:
        pass

    @abstractmethod
    def printPlanetInfo(self) -> None:
        pass
