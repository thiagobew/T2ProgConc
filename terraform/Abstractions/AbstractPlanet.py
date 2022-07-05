from abc import ABC, abstractmethod


class AbstractPlanet(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def nukeDetected(self, damage, lock) -> None:
        pass

    @abstractmethod
    def printPlanetInfo(self) -> None:
        pass
