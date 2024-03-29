from abc import ABC, abstractmethod
from threading import Condition, Lock, Semaphore
from typing import List
from space.rocket import Rocket


class AbstractSpaceBase(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def printSpaceBaseInfo(self) -> None:
        pass

    @abstractmethod
    def receiveLionRocket(self) -> None:
        pass

    @property
    @abstractmethod
    def receiveLionRocket(self) -> None:
        pass

    @property
    @abstractmethod
    def rocketsStorageMutex(self) -> Lock:
        pass

    @property
    @abstractmethod
    def resourcesMutex(self) -> Lock:
        pass

    @property
    @abstractmethod
    def semSpaceInStorage(self) -> Semaphore:
        pass

    @property
    @abstractmethod
    def semRocketInStorage(self) -> Semaphore:
        pass

    @property
    @abstractmethod
    def resourcesToCreateRockets(self) -> Condition:
        pass

    @property
    @abstractmethod
    def spaceInResourcesStorage(self) -> Condition:
        pass

    @property
    @abstractmethod
    def storage(self) -> List[Rocket]:
        pass

    @property
    @abstractmethod
    def storageLimit(self) -> int:
        pass

    @property
    @abstractmethod
    def uranium(self) -> int:
        pass

    @property
    @abstractmethod
    def fuel(self) -> int:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def fuelLimit(self) -> int:
        pass

    @property
    @abstractmethod
    def uraniumLimit(self) -> int:
        pass
